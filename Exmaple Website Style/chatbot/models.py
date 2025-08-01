from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.user:
            return f"Chat session for {self.user.username}"
        return f"Anonymous chat session {self.id}"

class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('bot', 'Bot Response'),
        ('system', 'System Message'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)  # For storing additional data
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."

class ChatbotKnowledge(models.Model):
    """Store knowledge base for the chatbot"""
    KNOWLEDGE_TYPES = [
        ('asset_info', 'Asset Information'),
        ('faq', 'Frequently Asked Questions'),
        ('category', 'Category Information'),
        ('general', 'General Information'),
    ]
    
    knowledge_type = models.CharField(max_length=20, choices=KNOWLEDGE_TYPES)
    question = models.TextField()
    answer = models.TextField()
    keywords = models.CharField(max_length=500, blank=True, help_text="Comma-separated keywords")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['knowledge_type', 'question']
    
    def __str__(self):
        return f"{self.knowledge_type}: {self.question[:50]}..."
    
    def get_keywords_list(self):
        """Return keywords as a list"""
        if self.keywords:
            return [keyword.strip().lower() for keyword in self.keywords.split(',')]
        return []
