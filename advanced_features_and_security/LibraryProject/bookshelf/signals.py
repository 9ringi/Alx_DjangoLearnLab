from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Create groups
    editors_group, created = Group.objects.get_or_create(name='Editors')
    viewers_group, created = Group.objects.get_or_create(name='Viewers')

    # Get content type for Book model
    content_type = ContentType.objects.get_for_model(Book)

    # Get or create permissions
    permission_view, created = Permission.objects.get_or_create(
        codename='can_view',
        name='Can view books',
        content_type=content_type
    )
    permission_edit, created = Permission.objects.get_or_create(
        codename='can_edit',
        name='Can edit books',
        content_type=content_type
    )

    # Assign permissions to groups
    editors_group.permissions.add(permission_edit)
    viewers_group.permissions.add(permission_view)
