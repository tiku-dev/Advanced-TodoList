from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo, Comment, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class commentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'todo', 'author', 'author_username', 'text', 'created_at']
        read_only_fields = ['author', 'created_at']

class TodoSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner_username = serializers.ReadOnlyField(source='owner.ownername')
    comment = commentSerializer(many=True, read_only=True)
    created_date = serializers.DateTimeField(source='created_at', format='%Y:%m:%d', read_only=True)
    created_time = serializers.DateTimeField(source='created_at', format='%H:%M:%S', read_only=True)

    class Meta:
        model = Todo
        fields = [
            'id', 'title', 'description', 'owner', 'owner_username', 
            'created_at', 'created_date', 'created_time', 
            'expires_at', 'comment'
        ]
        read_only_fields = ['owner', 'created_at']

