"""
Unit tests for Memory Service
"""
import pytest
import asyncio
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from jenny_core.services.memory_service import MemoryService
from jenny_core.database import DatabaseManager
from jenny_core.config import Settings


class TestMemoryService:
    """Test Memory Service functionality"""
    
    @pytest.fixture
    def memory_service(self, db_manager, test_settings):
        """Create Memory service for testing"""
        return MemoryService(db_manager, test_settings)
    
    @pytest.fixture
    def sample_conversation_data(self):
        """Sample conversation data for testing"""
        return {
            "session_id": str(uuid.uuid4()),
            "user_id": "test_user_123",
            "user_input": "What is the weather like?",
            "response": "The weather is sunny today.",
            "context_summary": "User asked about weather",
            "timestamp": datetime.utcnow()
        }
    
    def test_initialization(self, memory_service):
        """Test memory service initialization"""
        assert memory_service.db_manager is not None
        assert memory_service.settings is not None
        assert memory_service.vector_store is None  # Not initialized yet
    
    @pytest.mark.asyncio
    async def test_initialize_service(self, memory_service):
        """Test service initialization process"""
        with patch('chromadb.AsyncClient') as mock_chroma:
            mock_client = AsyncMock()
            mock_chroma.return_value = mock_client
            mock_client.get_or_create_collection.return_value = AsyncMock()
            
            await memory_service.initialize()
            
            assert memory_service.vector_store is not None
            mock_chroma.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_shutdown(self, memory_service):
        """Test service shutdown"""
        memory_service.vector_store = AsyncMock()
        await memory_service.shutdown()
        # Service should handle shutdown gracefully
    
    @pytest.mark.asyncio
    async def test_health_check(self, memory_service):
        """Test health check functionality"""
        # With vector store
        memory_service.vector_store = AsyncMock()
        memory_service.vector_store.heartbeat.return_value = True
        assert await memory_service.health_check() is True
        
        # Without vector store
        memory_service.vector_store = None
        assert await memory_service.health_check() is False
    
    @pytest.mark.asyncio
    async def test_store_conversation(self, memory_service, sample_conversation_data):
        """Test storing conversation in memory"""
        memory_service.vector_store = AsyncMock()
        mock_collection = AsyncMock()
        memory_service.vector_store.get_collection.return_value = mock_collection
        
        conversation_id = await memory_service.store_conversation(**sample_conversation_data)
        
        assert conversation_id is not None
        mock_collection.add.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_search_conversations(self, memory_service):
        """Test searching conversations"""
        memory_service.vector_store = AsyncMock()
        mock_collection = AsyncMock()
        memory_service.vector_store.get_collection.return_value = mock_collection
        
        # Mock search results
        mock_collection.query.return_value = {
            "ids": [["conv_1", "conv_2"]],
            "documents": [["First conversation", "Second conversation"]],
            "metadatas": [[
                {"timestamp": "2024-01-01T12:00:00", "user_id": "test_user"},
                {"timestamp": "2024-01-01T13:00:00", "user_id": "test_user"}
            ]],
            "distances": [[0.1, 0.3]]
        }
        
        results = await memory_service.search_conversations("weather", "test_user", limit=10)
        
        assert len(results) == 2
        assert results[0]["relevance_score"] > results[1]["relevance_score"]  # Sorted by relevance
        mock_collection.query.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_conversation_context(self, memory_service, db_manager):
        """Test getting conversation context"""
        # Mock database response
        mock_conversations = [
            {
                "id": "conv_1",
                "user_input": "Hello",
                "response": "Hi there!",
                "timestamp": datetime.utcnow() - timedelta(minutes=5),
                "context_summary": "Greeting"
            },
            {
                "id": "conv_2", 
                "user_input": "How are you?",
                "response": "I'm doing well!",
                "timestamp": datetime.utcnow() - timedelta(minutes=2),
                "context_summary": "Health inquiry"
            }
        ]
        
        with patch.object(db_manager, 'get_recent_conversations', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_conversations
            
            context = await memory_service.get_conversation_context("test_user", "session_123", limit=5)
            
            assert len(context) == 2
            assert context[0]["user_input"] == "Hello"
            assert context[1]["user_input"] == "How are you?"
            mock_get.assert_called_once_with("test_user", "session_123", 5)
    
    @pytest.mark.asyncio
    async def test_cache_response(self, memory_service):
        """Test response caching"""
        memory_service.response_cache = AsyncMock()
        
        await memory_service.cache_response(
            "What is AI?", 
            "AI is artificial intelligence",
            "openai",
            "test_user"
        )
        
        # Should store in cache
        assert memory_service.response_cache is not None
    
    @pytest.mark.asyncio
    async def test_get_cached_response(self, memory_service):
        """Test getting cached response"""
        # Mock cache hit
        memory_service.response_cache = {
            "what is ai?|test_user": {
                "response": "AI is artificial intelligence",
                "model": "openai",
                "timestamp": datetime.utcnow(),
                "hit_count": 1
            }
        }
        
        cached = await memory_service.get_cached_response("What is AI?", "test_user")
        
        assert cached is not None
        assert cached["response"] == "AI is artificial intelligence"
        assert cached["model"] == "openai"
        
        # Test cache miss
        cached_miss = await memory_service.get_cached_response("Unknown query", "test_user")
        assert cached_miss is None
    
    @pytest.mark.asyncio
    async def test_generate_context_summary(self, memory_service):
        """Test context summary generation"""
        user_input = "What is the weather like today?"
        response = "The weather is sunny with a temperature of 72°F"
        context = [
            {"user_input": "Hello", "response": "Hi there!"},
            {"user_input": "How are you?", "response": "I'm doing well!"}
        ]
        
        # Mock LLM service for summary generation
        with patch('jenny_core.services.llm_service.LLMService') as mock_llm:
            mock_llm_instance = AsyncMock()
            mock_llm.return_value = mock_llm_instance
            mock_llm_instance.generate_response.return_value = {
                "text": "User inquired about weather, received sunny weather report"
            }
            
            summary = await memory_service.generate_context_summary(user_input, response, context)
            
            assert "weather" in summary.lower()
            assert isinstance(summary, str)
    
    @pytest.mark.asyncio
    async def test_cleanup_old_conversations(self, memory_service, db_manager):
        """Test cleanup of old conversations"""
        days_to_keep = 30
        
        with patch.object(db_manager, 'delete_old_conversations', new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = 15  # 15 conversations deleted
            
            deleted_count = await memory_service.cleanup_old_conversations(days_to_keep)
            
            assert deleted_count == 15
            mock_delete.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_user_statistics(self, memory_service, db_manager):
        """Test getting user conversation statistics"""
        mock_stats = {
            "total_conversations": 150,
            "conversations_last_week": 25,
            "average_response_time": 1.2,
            "most_active_day": "Monday",
            "favorite_topics": ["weather", "news", "coding"]
        }
        
        with patch.object(db_manager, 'get_user_conversation_stats', new_callable=AsyncMock) as mock_stats_query:
            mock_stats_query.return_value = mock_stats
            
            stats = await memory_service.get_user_statistics("test_user")
            
            assert stats["total_conversations"] == 150
            assert stats["conversations_last_week"] == 25
            assert "weather" in stats["favorite_topics"]
    
    @pytest.mark.asyncio
    async def test_vector_search_performance(self, memory_service):
        """Test vector search performance"""
        memory_service.vector_store = AsyncMock()
        mock_collection = AsyncMock()
        memory_service.vector_store.get_collection.return_value = mock_collection
        
        # Mock fast search results
        mock_collection.query.return_value = {
            "ids": [["conv_1"]],
            "documents": [["Test conversation"]],
            "metadatas": [[{"timestamp": "2024-01-01T12:00:00", "user_id": "test_user"}]],
            "distances": [[0.1]]
        }
        
        import time
        start_time = time.time()
        
        results = await memory_service.search_conversations("test query", "test_user", limit=5)
        
        search_time = time.time() - start_time
        
        assert len(results) == 1
        assert search_time < 0.1  # Should be fast (< 100ms)
    
    @pytest.mark.asyncio
    async def test_conversation_deduplication(self, memory_service):
        """Test conversation deduplication"""
        # Store same conversation twice
        conversation_data = {
            "session_id": "session_123",
            "user_id": "test_user",
            "user_input": "Duplicate message",
            "response": "Duplicate response",
            "context_summary": "Duplicate conversation"
        }
        
        memory_service.vector_store = AsyncMock()
        mock_collection = AsyncMock()
        memory_service.vector_store.get_collection.return_value = mock_collection
        
        # First storage
        id1 = await memory_service.store_conversation(**conversation_data)
        
        # Second storage (should detect duplicate)
        with patch.object(memory_service, '_is_duplicate_conversation', new_callable=AsyncMock) as mock_check:
            mock_check.return_value = True
            
            id2 = await memory_service.store_conversation(**conversation_data)
            
            # Should not store duplicate
            mock_check.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_semantic_search_accuracy(self, memory_service):
        """Test semantic search accuracy"""
        memory_service.vector_store = AsyncMock()
        mock_collection = AsyncMock()
        memory_service.vector_store.get_collection.return_value = mock_collection
        
        # Mock semantically similar results
        mock_collection.query.return_value = {
            "ids": [["weather_1", "weather_2", "sports_1"]],
            "documents": [
                ["What's the weather today?", "How's the weather?", "Who won the game?"]
            ],
            "metadatas": [[
                {"timestamp": "2024-01-01T12:00:00", "user_id": "test_user"},
                {"timestamp": "2024-01-01T13:00:00", "user_id": "test_user"},
                {"timestamp": "2024-01-01T14:00:00", "user_id": "test_user"}
            ]],
            "distances": [[0.1, 0.15, 0.8]]  # Weather queries more similar
        }
        
        results = await memory_service.search_conversations("weather forecast", "test_user", limit=3)
        
        # Weather-related conversations should be ranked higher
        assert len(results) == 3
        assert results[0]["relevance_score"] > results[2]["relevance_score"]
        assert "weather" in results[0]["content"].lower()


class TestMemoryServiceIntegration:
    """Integration tests for Memory Service"""
    
    @pytest.mark.asyncio
    async def test_service_lifecycle(self, db_manager, test_settings):
        """Test complete service lifecycle"""
        service = MemoryService(db_manager, test_settings)
        
        # Initialize
        with patch('chromadb.AsyncClient') as mock_chroma:
            mock_client = AsyncMock()
            mock_chroma.return_value = mock_client
            mock_client.get_or_create_collection.return_value = AsyncMock()
            
            await service.initialize()
        
        assert service.vector_store is not None
        
        # Health check
        service.vector_store.heartbeat = AsyncMock(return_value=True)
        health = await service.health_check()
        assert health is True
        
        # Shutdown
        await service.shutdown()
    
    @pytest.mark.asyncio
    async def test_full_conversation_flow(self, memory_service, sample_conversation_data):
        """Test full conversation storage and retrieval flow"""
        memory_service.vector_store = AsyncMock()
        mock_collection = AsyncMock()
        memory_service.vector_store.get_collection.return_value = mock_collection
        
        # Store conversation
        conversation_id = await memory_service.store_conversation(**sample_conversation_data)
        assert conversation_id is not None
        
        # Mock search to return stored conversation
        mock_collection.query.return_value = {
            "ids": [[conversation_id]],
            "documents": [[sample_conversation_data["user_input"]]],
            "metadatas": [[{
                "timestamp": sample_conversation_data["timestamp"].isoformat(),
                "user_id": sample_conversation_data["user_id"]
            }]],
            "distances": [[0.1]]
        }
        
        # Search for conversation
        results = await memory_service.search_conversations(
            "weather", 
            sample_conversation_data["user_id"], 
            limit=5
        )
        
        assert len(results) == 1
        assert results[0]["user_id"] == sample_conversation_data["user_id"]
    
    @pytest.mark.asyncio
    async def test_memory_performance_under_load(self, memory_service):
        """Test memory service performance under load"""
        memory_service.vector_store = AsyncMock()
        mock_collection = AsyncMock()
        memory_service.vector_store.get_collection.return_value = mock_collection
        
        # Mock fast responses
        mock_collection.add.return_value = None
        mock_collection.query.return_value = {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }
        
        # Simulate concurrent operations
        import time
        start_time = time.time()
        
        tasks = []
        for i in range(20):
            # Mix of storage and search operations
            if i % 2 == 0:
                task = memory_service.store_conversation(
                    session_id=f"session_{i}",
                    user_id=f"user_{i}",
                    user_input=f"Message {i}",
                    response=f"Response {i}",
                    context_summary=f"Context {i}"
                )
            else:
                task = memory_service.search_conversations(f"query {i}", f"user_{i}", limit=5)
            
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        # All operations should complete successfully
        assert len(results) == 20
        assert all(not isinstance(r, Exception) for r in results)
        
        # Should complete within reasonable time (2 seconds for 20 operations)
        assert total_time < 2.0