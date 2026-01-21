from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.utils import timezone
from django.db.models import Q
from .models import Todo, Comment
from .serializers import TodoSerializer, commentSerializer

class IsownerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the object has an 'owner' or 'author' attribute
        
        owner = getattr(obj, 'owner', None) or getattr(obj, 'author', None)
        return owner == request.user
    
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsownerOrReadOnly]

    def get_queryset(self):
        # Filter out expired todos for general viewing
        now = timezone.now()
        filtered = Todo.objects.filter(
            Q(expires_at__gt=now) |
            Q(expires_at__isnull=True)
        ).order_by('-created_at')
        return filtered
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = commentSerializer
    permission_classes = [permissions.IsAuthenticated, IsownerOrReadOnly]

    def get_queryset(self):
        filtered = Comment.objects.all().order_by('-created_at')
        return filtered
        
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
