from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Fields: username, email, first_name, last_name, password, is_active
    """
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class Role(models.Model):
    """
    Role model for RBAC.
    Examples: Admin, Manager, User, Guest
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class Resource(models.Model):
    """
    Resource model represents protected resources in the system.
    Examples: 'documents', 'reports', 'users', 'settings'
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    endpoint_pattern = models.CharField(max_length=255, help_text="URL pattern for the resource, e.g., /api/documents/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resources'
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'

    def __str__(self):
        return self.name


class Permission(models.Model):
    """
    Permission model defines actions that can be performed on resources.
    Examples: view, create, update, delete, approve
    """
    ACTION_CHOICES = [
        ('view', 'View'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('approve', 'Approve'),
        ('export', 'Export'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'permissions'
        unique_together = ['name', 'action', 'resource']
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'

    def __str__(self):
        return f"{self.resource.name}:{self.action}"


class UserRole(models.Model):
    """
    Many-to-Many relationship between Users and Roles.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_roles'
        unique_together = ['user', 'role']
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"


class RolePermission(models.Model):
    """
    Many-to-Many relationship between Roles and Permissions.
    This defines what actions each role can perform on resources.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role_permissions'
        unique_together = ['role', 'permission']
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'

    def __str__(self):
        return f"{self.role.name} - {self.permission}"