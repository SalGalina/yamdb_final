from enum import Enum

from django.contrib.auth.models import UserManager


class Roles(Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class CreateSuperUserManager(UserManager):

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Roles.ADMIN.value)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') is not Roles.ADMIN.value:
            raise ValueError('Superuser must have role="admin".')

        return self._create_user(username, email, password, **extra_fields)
