from django.urls import path
from .views import UserCreateView, UserListView, UserUpdateView, UserLoginView, ScriptViewSet, RatingViewSet

urlpatterns = [
    # User Management URLs
    path('register/', UserCreateView.as_view(), name='user-register'),  # User registration
    path('users/', UserListView.as_view(), name='user-list'),  # List all users
    path('users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),  # Update user details
    path('login/', UserLoginView.as_view(), name='user-login'),  # User login

    # Script Management URLs
    path('scripts/', ScriptViewSet.as_view({'get': 'list', 'post': 'create'}), name='script-list'),  # List and create scripts
    path('scripts/<int:pk>/', ScriptViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='script-detail'),  # Retrieve, update, delete script

    # Rating Management URLs
    path('ratings/', RatingViewSet.as_view({'get': 'list', 'post': 'create'}), name='rating-list'),  # List and create ratings
    path('ratings/<int:pk>/', RatingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='rating-detail'),  # Retrieve, update, delete rating
]
