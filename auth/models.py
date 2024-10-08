from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.


class User(models.Model):
    '''
        The User model defines the personal information and the role type
        to access specific resources in the library system
    '''

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

    def save(self, *args):
        # hashing the user password
        self.password = make_password(self.password)
        super(User, self).save(*args)

    @property
    def is_authenticated(self):
        return self.status == self.Status.ACTIVE

    def __str__(self):
        return self.first_name + " " + self.last_name
