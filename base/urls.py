from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, CommentViewSet, UserProfileViewset, RegisterView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'comments', CommentViewSet, basename='comment')
# router.register(r'profile', UserProfileViewset, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    # Manually map the profile endpoint to handle GET and PUT/PATCH without a PK
    path('profile/', UserProfileViewset.as_view({
        'get': 'list',
        'put': 'update',
        'patch': 'partial_update'
    }), name='profile-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]