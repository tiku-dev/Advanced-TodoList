from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins
from django.utils import timezone
from django.db.models import Q
from .models import Todo, Comment, UserProfile
from .serializers import TodoSerializer, commentSerializer, UserProfileSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

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

class UserProfileViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsownerOrReadOnly]

    def get_object(self):
        return self.request.user.profile
    
    # def list(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def patch(self, request, *args, **kwargs):
    #     return self.partial_update(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)