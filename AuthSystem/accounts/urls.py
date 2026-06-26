from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, RegisterView, LogoutView, ProfileView,
    RoleListCreateView, RoleDetailView,
    ResourceListCreateView, ResourceDetailView,
    PermissionListCreateView, PermissionDetailView,
    UserRoleListCreateView, UserRoleDetailView,
    RolePermissionListCreateView, RolePermissionDetailView,
    MockDocumentsView, MockReportsView
)

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    
    # Role management (admin only)
    path('roles/', RoleListCreateView.as_view(), name='role-list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),
    
    # Resource management (admin only)
    path('resources/', ResourceListCreateView.as_view(), name='resource-list'),
    path('resources/<int:pk>/', ResourceDetailView.as_view(), name='resource-detail'),
    
    # Permission management (admin only)
    path('permissions/', PermissionListCreateView.as_view(), name='permission-list'),
    path('permissions/<int:pk>/', PermissionDetailView.as_view(), name='permission-detail'),
    
    # User-Role assignments (admin only)
    path('user-roles/', UserRoleListCreateView.as_view(), name='user-role-list'),
    path('user-roles/<int:pk>/', UserRoleDetailView.as_view(), name='user-role-detail'),
    
    # Role-Permission assignments (admin only)
    path('role-permissions/', RolePermissionListCreateView.as_view(), name='role-permission-list'),
    path('role-permissions/<int:pk>/', RolePermissionDetailView.as_view(), name='role-permission-detail'),
    
    # Mock business object endpoints
    path('documents/', MockDocumentsView.as_view(), name='mock-documents'),
    path('reports/', MockReportsView.as_view(), name='mock-reports'),
]