from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Role, Resource, Permission, UserRole, RolePermission
from .serializers import (
    UserSerializer, UserUpdateSerializer, RoleSerializer,
    ResourceSerializer, PermissionSerializer, UserRoleSerializer, RolePermissionSerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view that returns JWT tokens along with user info.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(email=request.data.get('email'))
            response.data['user'] = {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        return response


class RegisterView(APIView):
    """
    User registration endpoint.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Assign default 'User' role if it exists
            try:
                user_role = Role.objects.get(name='User')
                UserRole.objects.create(user=user, role=user_role)
            except Role.DoesNotExist:
                pass
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Logout endpoint - blacklists the refresh token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    Get and update current user profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Soft delete - set is_active to False
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': 'Account deactivated successfully'}, status=status.HTTP_200_OK)


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to check if user is admin.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class RoleListCreateView(APIView):
    """
    List all roles or create a new role (admin only).
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleDetailView(APIView):
    """
    Retrieve, update or delete a role (admin only).
    """
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return None

    def get(self, request, pk):
        role = self.get_object(pk)
        if not role:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role)
        return Response(serializer.data)

    def put(self, request, pk):
        role = self.get_object(pk)
        if not role:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = self.get_object(pk)
        if not role:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResourceListCreateView(APIView):
    """
    List all resources or create a new resource (admin only).
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResourceDetailView(APIView):
    """
    Retrieve, update or delete a resource (admin only).
    """
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Resource.objects.get(pk=pk)
        except Resource.DoesNotExist:
            return None

    def get(self, request, pk):
        resource = self.get_object(pk)
        if not resource:
            return Response({'error': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResourceSerializer(resource)
        return Response(serializer.data)

    def put(self, request, pk):
        resource = self.get_object(pk)
        if not resource:
            return Response({'error': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResourceSerializer(resource, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        resource = self.get_object(pk)
        if not resource:
            return Response({'error': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)
        resource.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PermissionListCreateView(APIView):
    """
    List all permissions or create a new permission (admin only).
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PermissionDetailView(APIView):
    """
    Retrieve, update or delete a permission (admin only).
    """
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Permission.objects.get(pk=pk)
        except Permission.DoesNotExist:
            return None

    def get(self, request, pk):
        permission = self.get_object(pk)
        if not permission:
            return Response({'error': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PermissionSerializer(permission)
        return Response(serializer.data)

    def put(self, request, pk):
        permission = self.get_object(pk)
        if not permission:
            return Response({'error': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PermissionSerializer(permission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        permission = self.get_object(pk)
        if not permission:
            return Response({'error': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)
        permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRoleListCreateView(APIView):
    """
    List all user-role assignments or create a new assignment (admin only).
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        user_roles = UserRole.objects.all()
        serializer = UserRoleSerializer(user_roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRoleDetailView(APIView):
    """
    Retrieve or delete a user-role assignment (admin only).
    """
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return UserRole.objects.get(pk=pk)
        except UserRole.DoesNotExist:
            return None

    def get(self, request, pk):
        user_role = self.get_object(pk)
        if not user_role:
            return Response({'error': 'UserRole not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserRoleSerializer(user_role)
        return Response(serializer.data)

    def delete(self, request, pk):
        user_role = self.get_object(pk)
        if not user_role:
            return Response({'error': 'UserRole not found'}, status=status.HTTP_404_NOT_FOUND)
        user_role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RolePermissionListCreateView(APIView):
    """
    List all role-permission assignments or create a new assignment (admin only).
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        role_permissions = RolePermission.objects.all()
        serializer = RolePermissionSerializer(role_permissions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RolePermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RolePermissionDetailView(APIView):
    """
    Retrieve or delete a role-permission assignment (admin only).
    """
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return RolePermission.objects.get(pk=pk)
        except RolePermission.DoesNotExist:
            return None

    def get(self, request, pk):
        role_permission = self.get_object(pk)
        if not role_permission:
            return Response({'error': 'RolePermission not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RolePermissionSerializer(role_permission)
        return Response(serializer.data)

    def delete(self, request, pk):
        role_permission = self.get_object(pk)
        if not role_permission:
            return Response({'error': 'RolePermission not found'}, status=status.HTTP_404_NOT_FOUND)
        role_permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Mock business object views
class MockDocumentsView(APIView):
    """
    Mock endpoint for documents resource.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Check if user has permission to view documents
        if not check_permission(request.user, 'documents', 'view'):
            return Response({'error': 'Forbidden - you do not have permission to view documents'},
                          status=status.HTTP_403_FORBIDDEN)
        
        # Return mock data
        return Response({
            'resource': 'documents',
            'action': 'view',
            'data': [
                {'id': 1, 'name': 'Document 1', 'type': 'pdf'},
                {'id': 2, 'name': 'Document 2', 'type': 'docx'},
                {'id': 3, 'name': 'Document 3', 'type': 'xlsx'},
            ]
        })

    def post(self, request):
        if not check_permission(request.user, 'documents', 'create'):
            return Response({'error': 'Forbidden - you do not have permission to create documents'},
                          status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            'resource': 'documents',
            'action': 'create',
            'message': 'Document created successfully',
            'data': request.data
        }, status=status.HTTP_201_CREATED)


class MockReportsView(APIView):
    """
    Mock endpoint for reports resource.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not check_permission(request.user, 'reports', 'view'):
            return Response({'error': 'Forbidden - you do not have permission to view reports'},
                          status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            'resource': 'reports',
            'action': 'view',
            'data': [
                {'id': 1, 'name': 'Monthly Report', 'date': '2024-01-01'},
                {'id': 2, 'name': 'Quarterly Report', 'date': '2024-03-31'},
            ]
        })

    def post(self, request):
        if not check_permission(request.user, 'reports', 'create'):
            return Response({'error': 'Forbidden - you do not have permission to create reports'},
                          status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            'resource': 'reports',
            'action': 'create',
            'message': 'Report created successfully',
            'data': request.data
        }, status=status.HTTP_201_CREATED)


def check_permission(user, resource_name, action):
    """
    Helper function to check if a user has permission to perform an action on a resource.
    """
    if not user.is_authenticated:
        return False
    
    # Superusers have all permissions
    if user.is_superuser:
        return True
    
    # Get user's roles
    user_roles = UserRole.objects.filter(user=user).values_list('role_id', flat=True)
    
    if not user_roles:
        return False
    
    # Check if any of the user's roles have the required permission
    has_permission = RolePermission.objects.filter(
        role_id__in=user_roles,
        permission__resource__name=resource_name,
        permission__action=action
    ).exists()
    
    return has_permission