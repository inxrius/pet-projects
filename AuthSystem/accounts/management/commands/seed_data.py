from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Role, Resource, Permission, UserRole, RolePermission

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with initial test data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create roles
        admin_role, _ = Role.objects.get_or_create(
            name='Admin',
            defaults={'description': 'Administrator with full access'}
        )
        
        manager_role, _ = Role.objects.get_or_create(
            name='Manager',
            defaults={'description': 'Manager with limited administrative access'}
        )
        
        user_role, _ = Role.objects.get_or_create(
            name='User',
            defaults={'description': 'Regular user with basic access'}
        )
        
        guest_role, _ = Role.objects.get_or_create(
            name='Guest',
            defaults={'description': 'Guest user with read-only access'}
        )
        
        self.stdout.write(self.style.SUCCESS('✓ Roles created'))
        
        # Create resources
        documents_resource, _ = Resource.objects.get_or_create(
            name='documents',
            defaults={
                'description': 'Document management system',
                'endpoint_pattern': '/api/documents/'
            }
        )
        
        reports_resource, _ = Resource.objects.get_or_create(
            name='reports',
            defaults={
                'description': 'Reports system',
                'endpoint_pattern': '/api/reports/'
            }
        )
        
        users_resource, _ = Resource.objects.get_or_create(
            name='users',
            defaults={
                'description': 'User management',
                'endpoint_pattern': '/api/users/'
            }
        )
        
        settings_resource, _ = Resource.objects.get_or_create(
            name='settings',
            defaults={
                'description': 'System settings',
                'endpoint_pattern': '/api/settings/'
            }
        )
        
        self.stdout.write(self.style.SUCCESS('✓ Resources created'))
        
        # Create permissions
        permissions_data = [
            # Documents permissions
            ('view_documents', 'View documents', 'view', documents_resource),
            ('create_documents', 'Create documents', 'create', documents_resource),
            ('update_documents', 'Update documents', 'update', documents_resource),
            ('delete_documents', 'Delete documents', 'delete', documents_resource),
            ('export_documents', 'Export documents', 'export', documents_resource),
            
            # Reports permissions
            ('view_reports', 'View reports', 'view', reports_resource),
            ('create_reports', 'Create reports', 'create', reports_resource),
            ('export_reports', 'Export reports', 'export', reports_resource),
            
            # Users permissions
            ('view_users', 'View users', 'view', users_resource),
            ('create_users', 'Create users', 'create', users_resource),
            ('update_users', 'Update users', 'update', users_resource),
            ('delete_users', 'Delete users', 'delete', users_resource),
            
            # Settings permissions
            ('view_settings', 'View settings', 'view', settings_resource),
            ('update_settings', 'Update settings', 'update', settings_resource),
        ]
        
        for name, description, action, resource in permissions_data:
            Permission.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'action': action,
                    'resource': resource
                }
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Permissions created'))
        
        # Assign permissions to roles
        # Admin - all permissions
        all_permissions = Permission.objects.all()
        for permission in all_permissions:
            RolePermission.objects.get_or_create(
                role=admin_role,
                permission=permission
            )
        
        # Manager - limited permissions
        manager_permissions = Permission.objects.filter(
            resource__name__in=['documents', 'reports']
        )
        for permission in manager_permissions:
            RolePermission.objects.get_or_create(
                role=manager_role,
                permission=permission
            )
        
        # User - basic permissions
        user_permissions = Permission.objects.filter(
            resource__name='documents',
            action__in=['view', 'create']
        )
        for permission in user_permissions:
            RolePermission.objects.get_or_create(
                role=user_role,
                permission=permission
            )
        
        # Guest - view only
        guest_permissions = Permission.objects.filter(
            resource__name__in=['documents', 'reports'],
            action='view'
        )
        for permission in guest_permissions:
            RolePermission.objects.get_or_create(
                role=guest_role,
                permission=permission
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Role permissions assigned'))
        
        # Create test users
        admin_user, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'username': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            UserRole.objects.create(user=admin_user, role=admin_role)
        
        manager_user, created = User.objects.get_or_create(
            email='manager@example.com',
            defaults={
                'username': 'manager',
                'first_name': 'Manager',
                'last_name': 'User',
            }
        )
        if created:
            manager_user.set_password('manager123')
            manager_user.save()
            UserRole.objects.create(user=manager_user, role=manager_role)
        
        regular_user, created = User.objects.get_or_create(
            email='user@example.com',
            defaults={
                'username': 'user',
                'first_name': 'Regular',
                'last_name': 'User',
            }
        )
        if created:
            regular_user.set_password('user123')
            regular_user.save()
            UserRole.objects.create(user=regular_user, role=user_role)
        
        guest_user, created = User.objects.get_or_create(
            email='guest@example.com',
            defaults={
                'username': 'guest',
                'first_name': 'Guest',
                'last_name': 'User',
            }
        )
        if created:
            guest_user.set_password('guest123')
            guest_user.save()
            UserRole.objects.create(user=guest_user, role=guest_role)
        
        self.stdout.write(self.style.SUCCESS('✓ Test users created'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Database seeded successfully!'))
        self.stdout.write('\nTest accounts:')
        self.stdout.write('  Admin:    admin@example.com / admin123')
        self.stdout.write('  Manager:  manager@example.com / manager123')
        self.stdout.write('  User:     user@example.com / user123')
        self.stdout.write('  Guest:    guest@example.com / guest123')