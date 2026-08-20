"""
Memory Service - Enhanced memory management with vector search capabilities
"""
import asyncio
import logging
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import uuid

from ..config import Settings

logger = logging.getLogger(__name__)

class MemoryService:
    """Enhanced memory service with vector search and intelligent caching"""
    
    def __init__(self, db_manager, settings: Settings):
        self.db_manager = db_manager
        self.settings = settings
        
        # Memory configuration
        self.max_context_length = settings.max_context_length
        self.retention_days = settings.memory_retention_days
        self.summary_threshold = settings.conversation_summary_threshold
        
        # Cache for frequently accessed data
        self.context_cache = {}
        self.cache_ttl = 300  # 5 minutes
        
        # Conversation summarization
        self.summarization_queue = asyncio.Queue()
        self.summarization_task = None
    
    async def initialize(self):
        """Initialize the memory service"""
        # Start background tasks
        self.summarization_task = asyncio.create_task(self._summarization_worker())
        
        # Clean up old data
        await self._cleanup_expired_data()
        
        logger.info("Memory service initialized")
    
    async def shutdown(self):
        """Shutdown the memory service"""
        if self.summarization_task:
            self.summarization_task.cancel()
            try:
                await self.summarization_task
            except asyncio.CancelledError:
                pass
    
    async def health_check(self) -> bool:
        """Check service health"""
        try:
            # Test database connection
            await self.db_manager.health_check()
            return True
        except Exception:
            return False
    
    async def get_cached_response(
        self,
        user_input: str,
        user_id: str,
        similarity_threshold: float = 0.8
    ) -> Optional[Dict[str, Any]]:
        """Get cached response for similar user input"""
        try:
            # Check exact cache first
            cached = await self.db_manager.get_cached_response(user_input)
            if cached and cached.get("confidence_score", 0) >= similarity_threshold:
                return cached
            
            # Check vector similarity if available
            if self.db_manager.vector_collection:
                similar_conversations = await self.search_conversations(
                    query=user_input,
                    user_id=user_id,
                    limit=3,
                    use_vector_search=True
                )
                
                for conv in similar_conversations:
                    if conv.get("search_type") == "vector":
                        # Return the most similar response
                        responses = conv.get("responses", {})
                        if responses:
                            primary_response = next(iter(responses.values()))
                            return {
                                "response": primary_response,
                                "model_used": "cached_similar",
                                "confidence_score": 0.8,
                                "usage_count": 1,
                                "cached": True,
                                "similarity_match": True
                            }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached response: {e}")
            return None
    
    async def cache_response(
        self,
        user_input: str,
        response: str,
        model_used: str,
        user_id: str,
        confidence_score: float = 1.0,
        ttl_hours: int = 24
    ):
        """Cache a response for future use"""
        try:
            await self.db_manager.cache_response(
                input_text=user_input,
                response_text=response,
                model_used=model_used,
                confidence_score=confidence_score,
                ttl_hours=ttl_hours
            )
        except Exception as e:
            logger.error(f"Error caching response: {e}")
    
    async def get_conversation_context(
        self,
        user_id: str,
        session_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get conversation context for a user session"""
        cache_key = f"{user_id}:{session_id}:{limit}"
        
        # Check cache first
        if cache_key in self.context_cache:
            cache_entry = self.context_cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self.cache_ttl:
                return cache_entry["data"]
        
        try:
            # Get recent conversations
            conversations = await self.db_manager.search_conversations(
                query="",  # Empty query gets recent conversations
                user_id=user_id,
                limit=limit,
                use_vector_search=False
            )
            
            # Format for context
            context = []
            for conv in conversations:
                if conv.get("user_input") and conv.get("responses"):
                    primary_response = next(iter(conv["responses"].values()))
                    context.append({
                        "user_input": conv["user_input"],
                        "response": primary_response,
                        "timestamp": conv.get("timestamp"),
                        "context_summary": conv.get("context_summary")
                    })
            
            # Cache the result
            self.context_cache[cache_key] = {
                "data": context,
                "timestamp": time.time()
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Error getting conversation context: {e}")
            return []
    
    async def search_conversations(
        self,
        query: str,
        user_id: str,
        limit: int = 10,
        use_vector_search: bool = True
    ) -> List[Dict[str, Any]]:
        """Search through conversation memory"""
        try:
            return await self.db_manager.search_conversations(
                query=query,
                user_id=user_id,
                limit=limit,
                use_vector_search=use_vector_search
            )
        except Exception as e:
            logger.error(f"Error searching conversations: {e}")
            return []
    
    async def generate_context_summary(
        self,
        user_input: str,
        response: str,
        conversation_context: List[Dict[str, Any]] = None
    ) -> Optional[str]:
        """Generate a summary of the conversation context"""
        try:
            # Simple summarization logic - could be enhanced with LLM
            if not conversation_context or len(conversation_context) < self.summary_threshold:
                return f"User asked: {user_input[:100]}..."
            
            # Create a summary based on recent context
            recent_topics = []
            for ctx in conversation_context[-5:]:  # Last 5 exchanges
                if ctx.get("user_input"):
                    # Extract key topics (simple keyword extraction)
                    words = ctx["user_input"].lower().split()
                    key_words = [w for w in words if len(w) > 4 and w.isalpha()]
                    recent_topics.extend(key_words[:3])
            
            # Remove duplicates and limit
            unique_topics = list(dict.fromkeys(recent_topics))[:10]
            
            if unique_topics:
                return f"Conversation about: {', '.join(unique_topics)}. Latest: {user_input[:100]}..."
            else:
                return f"User asked: {user_input[:100]}..."
                
        except Exception as e:
            logger.error(f"Error generating context summary: {e}")
            return None
    
    async def store_user_preference(
        self,
        user_id: str,
        preference_type: str,
        preference_data: Dict[str, Any]
    ):
        """Store user preference"""
        try:
            profile = await self.db_manager.get_user_profile(user_id)
            
            if "preferences" not in profile["profile_data"]:
                profile["profile_data"]["preferences"] = {}
            
            profile["profile_data"]["preferences"][preference_type] = preference_data
            
            # Update profile in database (would need method in db_manager)
            # For now, we'll store as a conversation
            await self.db_manager.save_conversation(
                session_id=f"preference_{user_id}",
                user_id=user_id,
                user_input_raw=f"Preference update: {preference_type}",
                user_input_cleaned=f"Preference: {preference_type}",
                model_responses={"system": "Preference stored"},
                models_used=["system"],
                context_summary=f"User preference for {preference_type}",
                session_context={"preference": True, "type": preference_type, "data": preference_data}
            )
            
        except Exception as e:
            logger.error(f"Error storing user preference: {e}")
    
    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences"""
        try:
            profile = await self.db_manager.get_user_profile(user_id)
            return profile.get("profile_data", {}).get("preferences", {})
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return {}
    
    async def analyze_conversation_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze conversation patterns for a user"""
        try:
            # Get recent conversations
            conversations = await self.search_conversations(
                query="",
                user_id=user_id,
                limit=100,
                use_vector_search=False
            )
            
            if not conversations:
                return {"patterns": [], "insights": "No conversations found"}
            
            # Analyze patterns
            patterns = {
                "total_conversations": len(conversations),
                "avg_response_length": 0,
                "common_topics": [],
                "conversation_frequency": {},
                "preferred_models": {},
                "time_patterns": {}
            }
            
            total_length = 0
            topic_words = {}
            model_counts = {}
            hour_counts = {}
            
            for conv in conversations:
                # Response length
                responses = conv.get("responses", {})
                if responses:
                    primary_response = next(iter(responses.values()))
                    total_length += len(primary_response)
                
                # Model usage
                for model in responses.keys():
                    model_counts[model] = model_counts.get(model, 0) + 1
                
                # Time patterns
                if conv.get("timestamp"):
                    try:
                        conv_time = datetime.fromisoformat(conv["timestamp"])
                        hour = conv_time.hour
                        hour_counts[hour] = hour_counts.get(hour, 0) + 1
                    except:
                        pass
                
                # Topic extraction
                user_input = conv.get("user_input", "")
                words = user_input.lower().split()
                for word in words:
                    if len(word) > 4 and word.isalpha():
                        topic_words[word] = topic_words.get(word, 0) + 1
            
            # Calculate averages and top items
            if conversations:
                patterns["avg_response_length"] = total_length // len(conversations)
            
            # Top topics
            patterns["common_topics"] = sorted(
                topic_words.items(), key=lambda x: x[1], reverse=True
            )[:10]
            
            # Preferred models
            patterns["preferred_models"] = sorted(
                model_counts.items(), key=lambda x: x[1], reverse=True
            )
            
            # Peak hours
            patterns["time_patterns"] = sorted(
                hour_counts.items(), key=lambda x: x[1], reverse=True
            )[:5]
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing conversation patterns: {e}")
            return {"error": str(e)}
    
    async def _summarization_worker(self):
        """Background worker for conversation summarization"""
        while True:
            try:
                # Wait for summarization tasks
                task = await self.summarization_queue.get()
                
                # Process the task
                await self._process_summarization_task(task)
                
                # Mark task as done
                self.summarization_queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Summarization worker error: {e}")
                await asyncio.sleep(5)
    
    async def _process_summarization_task(self, task: Dict[str, Any]):
        """Process a conversation summarization task"""
        try:
            user_id = task.get("user_id")
            session_id = task.get("session_id")
            
            if not user_id or not session_id:
                return
            
            # Get conversation context
            context = await self.get_conversation_context(user_id, session_id, limit=20)
            
            if len(context) >= self.summary_threshold:
                # Generate summary (simplified - could use LLM)
                summary = await self._generate_conversation_summary(context)
                
                if summary:
                    # Store summary (would need method in db_manager)
                    logger.info(f"Generated conversation summary for {user_id}:{session_id}")
                    
        except Exception as e:
            logger.error(f"Error processing summarization task: {e}")
    
    async def _generate_conversation_summary(self, context: List[Dict[str, Any]]) -> Optional[str]:
        """Generate a conversation summary"""
        try:
            if not context:
                return None
            
            # Simple summarization - extract key themes
            topics = []
            for ctx in context:
                user_input = ctx.get("user_input", "")
                words = user_input.lower().split()
                key_words = [w for w in words if len(w) > 4 and w.isalpha()]
                topics.extend(key_words[:2])
            
            # Get unique topics
            unique_topics = list(dict.fromkeys(topics))[:8]
            
            if unique_topics:
                return f"Conversation covered topics: {', '.join(unique_topics)}"
            else:
                return "General conversation"
                
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return None
    
    async def _cleanup_expired_data(self):
        """Clean up expired memory data"""
        try:
            await self.db_manager.cleanup_expired_data()
            
            # Clean up local cache
            current_time = time.time()
            expired_keys = [
                key for key, value in self.context_cache.items()
                if current_time - value["timestamp"] > self.cache_ttl * 2
            ]
            
            for key in expired_keys:
                del self.context_cache[key]
                
            logger.info("Memory cleanup completed")
            
        except Exception as e:
            logger.error(f"Memory cleanup error: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory service statistics"""
        return {
            "cache_entries": len(self.context_cache),
            "summarization_queue_size": self.summarization_queue.qsize(),
            "max_context_length": self.max_context_length,
            "retention_days": self.retention_days,
            "summary_threshold": self.summary_threshold
        }