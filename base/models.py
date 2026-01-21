from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, help_text='Time for todo to disappear')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')

    def __str__(self):
        return self.title
    
    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'commented by {self.author.username} on {self.todo.title}'
