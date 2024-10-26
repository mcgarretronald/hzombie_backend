from django.urls import path
from .views import UserCreateView, UserListView, UserUpdateView, UserLoginView, ScriptViewSet

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    
    # Script URLs
    path('scripts/', ScriptViewSet.as_view({'get': 'list', 'post': 'create'}), name='script-list'),  # List and create scripts
    path('scripts/<int:pk>/', ScriptViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='script-detail'),  # Retrieve, update, delete script
]
