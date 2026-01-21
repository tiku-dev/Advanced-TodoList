from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    # path('todos', TodoViewSet, name='todo'),
    # path('comments', CommentViewSet, name='comment')
]