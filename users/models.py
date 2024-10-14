from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    '''
        The User model defines the personal information and the role type
        to access specific resources in the library system
    '''

    # defining a custom user schema to avoid clash between default user groups and permissions
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to a custom user set',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Change this as well
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'email'

    class Role(models.TextChoices):
        LIBRARIAN = 'LIBRARIAN', 'librarian'
        MEMBER = 'MEMBER', 'member'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'active'
        INACTIVE = 'INACTIVE', 'inactive'
        DELETED = 'DELETED', 'deleted'

    email = models.EmailField(max_length=255, unique=True, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=128, null=False)
    role = models.CharField(max_length=10, choices=Role.choices, null=False)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    @property
    def is_authenticated(self):
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "status": self.status
        }
