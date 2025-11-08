from django.contrib import admin
from .models import Message, ActiveUser


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for Message model.
    """
    list_display = ['id', 'username', 'message_preview', 'timestamp']
    list_filter = ['timestamp', 'username']
    search_fields = ['username', 'message_text']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def message_preview(self, obj):
        """
        Display first 50 characters of message.
        """
        return obj.message_text[:50] + '...' if len(obj.message_text) > 50 else obj.message_text
    
    message_preview.short_description = 'Message Preview'


@admin.register(ActiveUser)
class ActiveUserAdmin(admin.ModelAdmin):
    """
    Admin interface for ActiveUser model.
    """
    list_display = ['username', 'session_id_preview', 'last_activity', 'is_online']
    list_filter = ['last_activity']
    search_fields = ['username', 'session_id']
    readonly_fields = ['last_activity']
    ordering = ['-last_activity']
    
    def session_id_preview(self, obj):
        """
        Display first 20 characters of session_id.
        """
        return obj.session_id[:20] + '...' if len(obj.session_id) > 20 else obj.session_id
    
    session_id_preview.short_description = 'Session ID'
    
    def is_online(self, obj):
        """
        Check if user is online (active in last 5 minutes).
        """
        from django.utils import timezone
        from datetime import timedelta
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        return obj.last_activity >= five_minutes_ago
    
    is_online.boolean = True
    is_online.short_description = 'Online'
