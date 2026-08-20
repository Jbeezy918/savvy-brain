"""
Memory Service for Jenny AI Assistant
Handles conversation memory, context management, and intelligent caching 🧠
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, deque
import hashlib

from core.config import settings
from core.logging import get_logger, log_async_function_call

logger = get_logger(__name__)


class MemoryEntry:
    """Individual memory entry"""
    
    def __init__(
        self,
        key: str,
        content: Any,
        entry_type: str = "message",
        metadata: Optional[Dict[str, Any]] = None,
        importance: float = 1.0,
        expiry: Optional[datetime] = None
    ):
        self.key = key
        self.content = content
        self.entry_type = entry_type  # message, context, summary, etc.
        self.metadata = metadata or {}
        self.importance = importance  # 0.0 to 1.0
        self.created_at = datetime.utcnow()
        self.last_accessed = datetime.utcnow()
        self.access_count = 0
        self.expiry = expiry
    
    def access(self):
        """Update access statistics"""
        self.last_accessed = datetime.utcnow()
        self.access_count += 1
    
    def is_expired(self) -> bool:
        """Check if entry is expired"""
        if not self.expiry:
            return False
        return datetime.utcnow() > self.expiry
    
    def calculate_relevance(self, decay_factor: float = 0.9) -> float:
        """Calculate relevance score based on recency, frequency, and importance"""
        # Time-based decay
        time_diff = datetime.utcnow() - self.last_accessed
        time_decay = decay_factor ** (time_diff.total_seconds() / 3600)  # Hourly decay
        
        # Frequency boost
        frequency_boost = min(1.0, self.access_count / 10.0)
        
        # Combine factors
        relevance = self.importance * time_decay * (1.0 + frequency_boost)
        
        return relevance
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "key": self.key,
            "content": self.content,
            "entry_type": self.entry_type,
            "metadata": self.metadata,
            "importance": self.importance,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count,
            "expiry": self.expiry.isoformat() if self.expiry else None
        }


class ConversationMemory:
    """Memory container for a single conversation"""
    
    def __init__(self, conversation_id: str, max_entries: int = 100):
        self.conversation_id = conversation_id
        self.max_entries = max_entries
        self.entries: Dict[str, MemoryEntry] = {}
        self.message_history = deque(maxlen=max_entries)
        self.context_summary = ""
        self.key_topics = set()
        self.created_at = datetime.utcnow()
        self.last_updated = datetime.utcnow()
    
    def add_entry(self, entry: MemoryEntry):
        """Add memory entry"""
        self.entries[entry.key] = entry
        
        # Add to message history if it's a message
        if entry.entry_type == "message":
            self.message_history.append(entry)
        
        self.last_updated = datetime.utcnow()
        
        # Clean up if over limit
        self._cleanup_old_entries()
    
    def get_entry(self, key: str) -> Optional[MemoryEntry]:
        """Get memory entry by key"""
        if key in self.entries and not self.entries[key].is_expired():
            self.entries[key].access()
            return self.entries[key]
        return None
    
    def get_recent_messages(self, limit: int = 10) -> List[MemoryEntry]:
        """Get recent message entries"""
        recent = list(self.message_history)[-limit:]
        
        # Update access statistics
        for entry in recent:
            entry.access()
        
        return recent
    
    def get_context_for_llm(self, limit: int = 20) -> List[Dict[str, str]]:
        """Get conversation context formatted for LLM"""
        recent_messages = self.get_recent_messages(limit)
        
        context = []
        for entry in recent_messages:
            if isinstance(entry.content, dict) and "role" in entry.content:
                context.append({
                    "role": entry.content["role"],
                    "content": entry.content["content"]
                })
            else:
                # Assume it's a message dict with sender and content
                role = "user" if entry.content.get("sender") == "user" else "assistant"
                context.append({
                    "role": role,
                    "content": entry.content.get("content", str(entry.content))
                })
        
        return context
    
    def update_context_summary(self, summary: str):
        """Update conversation context summary"""
        self.context_summary = summary
        self.last_updated = datetime.utcnow()
    
    def add_key_topic(self, topic: str):
        """Add key topic to conversation"""
        self.key_topics.add(topic.lower())
    
    def search_entries(
        self,
        query: str,
        entry_type: Optional[str] = None,
        limit: int = 10
    ) -> List[MemoryEntry]:
        """Search memory entries"""
        query_lower = query.lower()
        matches = []
        
        for entry in self.entries.values():
            if entry.is_expired():
                continue
            
            if entry_type and entry.entry_type != entry_type:
                continue
            
            # Simple text search in content
            content_str = str(entry.content).lower()
            if query_lower in content_str:
                matches.append((entry, entry.calculate_relevance()))
        
        # Sort by relevance and return top results
        matches.sort(key=lambda x: x[1], reverse=True)
        results = [entry for entry, _ in matches[:limit]]
        
        # Update access statistics
        for entry in results:
            entry.access()
        
        return results
    
    def _cleanup_old_entries(self):
        """Clean up old or low-relevance entries"""
        if len(self.entries) <= self.max_entries:
            return
        
        # Calculate relevance for all entries
        entry_relevance = [
            (key, entry.calculate_relevance())
            for key, entry in self.entries.items()
            if not entry.is_expired()
        ]
        
        # Sort by relevance (ascending to remove least relevant first)
        entry_relevance.sort(key=lambda x: x[1])
        
        # Remove least relevant entries
        entries_to_remove = len(self.entries) - self.max_entries
        for i in range(entries_to_remove):
            key_to_remove = entry_relevance[i][0]
            del self.entries[key_to_remove]
        
        logger.debug(f"🧠 Cleaned up {entries_to_remove} memory entries for conversation {self.conversation_id}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        active_entries = sum(1 for entry in self.entries.values() if not entry.is_expired())
        
        entry_types = defaultdict(int)
        total_importance = 0
        
        for entry in self.entries.values():
            if not entry.is_expired():
                entry_types[entry.entry_type] += 1
                total_importance += entry.importance
        
        return {
            "conversation_id": self.conversation_id,
            "total_entries": len(self.entries),
            "active_entries": active_entries,
            "message_history_length": len(self.message_history),
            "entry_types": dict(entry_types),
            "average_importance": total_importance / active_entries if active_entries > 0 else 0,
            "key_topics_count": len(self.key_topics),
            "context_summary_length": len(self.context_summary),
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat()
        }


class MemoryService:
    """Main memory management service"""
    
    def __init__(self):
        self.conversation_memories: Dict[str, ConversationMemory] = {}
        self.global_memory: Dict[str, MemoryEntry] = {}
        self.memory_limit = settings.CONVERSATION_MEMORY_LIMIT
        self.cleanup_interval = 3600  # 1 hour
        self.last_cleanup = datetime.utcnow()
        
        logger.info(f"🧠 Memory service initialized with limit: {self.memory_limit}")
    
    @log_async_function_call(logger)
    async def initialize_conversation(
        self,
        conversation_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ConversationMemory:
        """Initialize memory for a new conversation"""
        if conversation_id in self.conversation_memories:
            logger.warning(f"⚠️ Conversation memory already exists: {conversation_id}")
            return self.conversation_memories[conversation_id]
        
        memory = ConversationMemory(conversation_id, self.memory_limit)
        
        # Add initialization metadata if provided
        if metadata:
            init_entry = MemoryEntry(
                key=f"init_{conversation_id}",
                content=metadata,
                entry_type="initialization",
                importance=0.8
            )
            memory.add_entry(init_entry)
        
        self.conversation_memories[conversation_id] = memory
        
        logger.info(f"🧠 Initialized conversation memory: {conversation_id}")
        return memory
    
    @log_async_function_call(logger)
    async def add_message(
        self,
        conversation_id: str,
        message_data: Dict[str, Any],
        importance: float = 1.0
    ) -> bool:
        """Add message to conversation memory"""
        if conversation_id not in self.conversation_memories:
            await self.initialize_conversation(conversation_id)
        
        memory = self.conversation_memories[conversation_id]
        
        # Create memory entry
        message_id = message_data.get("id", f"msg_{datetime.utcnow().timestamp()}")
        entry = MemoryEntry(
            key=message_id,
            content=message_data,
            entry_type="message",
            importance=importance,
            metadata={
                "sender": message_data.get("sender"),
                "timestamp": message_data.get("timestamp", datetime.utcnow()).isoformat(),
                "tokens": message_data.get("tokens_used"),
                "provider": message_data.get("provider")
            }
        )
        
        memory.add_entry(entry)
        
        # Extract and add key topics from message content
        await self._extract_key_topics(memory, message_data.get("content", ""))
        
        logger.debug(f"🧠 Added message to memory: {conversation_id}/{message_id}")
        return True
    
    @log_async_function_call(logger)
    async def get_conversation_context(
        self,
        conversation_id: str,
        limit: int = 20
    ) -> List[Dict[str, str]]:
        """Get conversation context for LLM"""
        if conversation_id not in self.conversation_memories:
            logger.warning(f"⚠️ No memory found for conversation: {conversation_id}")
            return []
        
        memory = self.conversation_memories[conversation_id]
        context = memory.get_context_for_llm(limit)
        
        logger.debug(f"🧠 Retrieved {len(context)} context messages for: {conversation_id}")
        return context
    
    @log_async_function_call(logger)
    async def search_conversation_memory(
        self,
        conversation_id: str,
        query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search conversation memory"""
        if conversation_id not in self.conversation_memories:
            return []
        
        memory = self.conversation_memories[conversation_id]
        entries = memory.search_entries(query, limit=limit)
        
        results = [entry.to_dict() for entry in entries]
        
        logger.debug(f"🔍 Found {len(results)} memory entries for query '{query}' in {conversation_id}")
        return results
    
    @log_async_function_call(logger)
    async def update_conversation_summary(
        self,
        conversation_id: str,
        summary: str
    ) -> bool:
        """Update conversation summary"""
        if conversation_id not in self.conversation_memories:
            return False
        
        memory = self.conversation_memories[conversation_id]
        memory.update_context_summary(summary)
        
        # Add summary as a memory entry
        summary_entry = MemoryEntry(
            key=f"summary_{conversation_id}_{datetime.utcnow().timestamp()}",
            content={"summary": summary},
            entry_type="summary",
            importance=0.9
        )
        memory.add_entry(summary_entry)
        
        logger.debug(f"🧠 Updated conversation summary: {conversation_id}")
        return True
    
    @log_async_function_call(logger)
    async def add_document_context(
        self,
        conversation_id: str,
        document_data: Dict[str, Any]
    ) -> bool:
        """Add document context to conversation memory"""
        if conversation_id not in self.conversation_memories:
            await self.initialize_conversation(conversation_id)
        
        memory = self.conversation_memories[conversation_id]
        
        # Create document context entry
        doc_id = document_data.get("id", "unknown")
        entry = MemoryEntry(
            key=f"doc_{doc_id}",
            content=document_data,
            entry_type="document",
            importance=0.8,
            metadata={
                "document_id": doc_id,
                "filename": document_data.get("filename"),
                "file_type": document_data.get("file_type"),
                "word_count": document_data.get("word_count")
            }
        )
        
        memory.add_entry(entry)
        
        # Add document topics
        if "extracted_text" in document_data:
            await self._extract_key_topics(memory, document_data["extracted_text"])
        
        logger.debug(f"📄 Added document context to memory: {conversation_id}/{doc_id}")
        return True
    
    @log_async_function_call(logger)
    async def clear_conversation(self, conversation_id: str) -> bool:
        """Clear conversation memory"""
        if conversation_id in self.conversation_memories:
            del self.conversation_memories[conversation_id]
            logger.info(f"🧠 Cleared conversation memory: {conversation_id}")
            return True
        
        logger.warning(f"⚠️ No memory to clear for conversation: {conversation_id}")
        return False
    
    @log_async_function_call(logger)
    async def get_memory_statistics(
        self,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get memory statistics"""
        if conversation_id:
            if conversation_id not in self.conversation_memories:
                return {}
            
            memory = self.conversation_memories[conversation_id]
            return memory.get_memory_stats()
        
        # Global statistics
        total_conversations = len(self.conversation_memories)
        total_entries = sum(
            len(memory.entries)
            for memory in self.conversation_memories.values()
        )
        
        active_conversations = sum(
            1 for memory in self.conversation_memories.values()
            if (datetime.utcnow() - memory.last_updated).total_seconds() < 3600
        )
        
        return {
            "total_conversations": total_conversations,
            "active_conversations": active_conversations,
            "total_memory_entries": total_entries,
            "global_memory_entries": len(self.global_memory),
            "memory_limit_per_conversation": self.memory_limit,
            "last_cleanup": self.last_cleanup.isoformat(),
            "service_uptime": (datetime.utcnow() - datetime.utcnow()).total_seconds()
        }
    
    @log_async_function_call(logger)
    async def compress_old_memories(self, conversation_id: str) -> bool:
        """Compress old memories into summaries"""
        if conversation_id not in self.conversation_memories:
            return False
        
        memory = self.conversation_memories[conversation_id]
        
        # Get old messages (older than 1 hour)
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        old_messages = [
            entry for entry in memory.message_history
            if entry.created_at < cutoff_time
        ]
        
        if len(old_messages) < 10:  # Not enough messages to compress
            return False
        
        # Create summary of old messages (placeholder - would use LLM in production)
        summary_content = self._create_message_summary(old_messages)
        
        # Create compressed summary entry
        summary_entry = MemoryEntry(
            key=f"compressed_{conversation_id}_{datetime.utcnow().timestamp()}",
            content={"compressed_summary": summary_content, "message_count": len(old_messages)},
            entry_type="compressed_summary",
            importance=0.7
        )
        
        memory.add_entry(summary_entry)
        
        # Remove old individual message entries
        for entry in old_messages[:len(old_messages)//2]:  # Remove half
            if entry.key in memory.entries:
                del memory.entries[entry.key]
        
        logger.info(f"🗜️ Compressed {len(old_messages)//2} old memories for: {conversation_id}")
        return True
    
    async def cleanup_expired_memories(self):
        """Clean up expired memories across all conversations"""
        current_time = datetime.utcnow()
        
        # Skip if cleaned up recently
        if (current_time - self.last_cleanup).total_seconds() < self.cleanup_interval:
            return
        
        total_cleaned = 0
        
        for conversation_id, memory in list(self.conversation_memories.items()):
            # Remove expired entries
            expired_keys = [
                key for key, entry in memory.entries.items()
                if entry.is_expired()
            ]
            
            for key in expired_keys:
                del memory.entries[key]
                total_cleaned += 1
            
            # Remove completely inactive conversations (no activity for 7 days)
            if (current_time - memory.last_updated).days > 7:
                del self.conversation_memories[conversation_id]
                logger.info(f"🧠 Removed inactive conversation memory: {conversation_id}")
        
        # Clean up global memory
        global_expired = [
            key for key, entry in self.global_memory.items()
            if entry.is_expired()
        ]
        
        for key in global_expired:
            del self.global_memory[key]
            total_cleaned += 1
        
        self.last_cleanup = current_time
        
        if total_cleaned > 0:
            logger.info(f"🧹 Cleaned up {total_cleaned} expired memory entries")
    
    def _create_message_summary(self, messages: List[MemoryEntry]) -> str:
        """Create summary of message list (placeholder implementation)"""
        # In production, this would use an LLM to create intelligent summaries
        topics = set()
        user_messages = 0
        assistant_messages = 0
        
        for entry in messages:
            if isinstance(entry.content, dict):
                sender = entry.content.get("sender", "unknown")
                if sender == "user":
                    user_messages += 1
                elif sender == "assistant":
                    assistant_messages += 1
                
                # Extract simple keywords from content
                content = entry.content.get("content", "")
                words = content.lower().split()
                # Add words longer than 4 characters as potential topics
                topics.update(word for word in words if len(word) > 4)
        
        # Limit topics to top 10 most common
        topic_list = list(topics)[:10]
        
        return f"Conversation segment with {user_messages} user messages and {assistant_messages} assistant responses. Key topics: {', '.join(topic_list[:5])}."
    
    async def _extract_key_topics(self, memory: ConversationMemory, text: str):
        """Extract key topics from text (simplified implementation)"""
        if not text:
            return
        
        # Simple keyword extraction (in production, use NLP libraries)
        words = text.lower().split()
        
        # Find potential topics (words longer than 4 characters, not common words)
        common_words = {
            "this", "that", "with", "have", "they", "were", "been", "their",
            "said", "each", "which", "what", "where", "when", "there", "would",
            "could", "should", "about", "after", "before", "during", "through"
        }
        
        topics = [
            word for word in words
            if len(word) > 4 and word not in common_words
        ]
        
        # Add unique topics to memory
        for topic in set(topics[:10]):  # Limit to 10 topics
            memory.add_key_topic(topic)
    
    async def add_global_memory(
        self,
        key: str,
        content: Any,
        entry_type: str = "global",
        importance: float = 1.0,
        expiry_hours: Optional[int] = None
    ) -> bool:
        """Add entry to global memory"""
        expiry = None
        if expiry_hours:
            expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
        
        entry = MemoryEntry(
            key=key,
            content=content,
            entry_type=entry_type,
            importance=importance,
            expiry=expiry
        )
        
        self.global_memory[key] = entry
        
        logger.debug(f"🧠 Added global memory entry: {key}")
        return True
    
    async def get_global_memory(self, key: str) -> Optional[Any]:
        """Get global memory entry"""
        if key in self.global_memory and not self.global_memory[key].is_expired():
            entry = self.global_memory[key]
            entry.access()
            return entry.content
        
        return None