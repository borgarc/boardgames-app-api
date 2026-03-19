"""
User databse models.
"""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return user."""
        if not email:
            raise ValueError('Email required.')
        normalized_email = self.normalize_email(email)
        user = self.model(email=normalized_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def update_user(self, user, **extra_fields):
        """Update the user, hashing the pass."""
        password = extra_fields.pop('password', None)

        for attr, value in extra_fields.items():
            setattr(user, attr, value)

        if password:
            user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    def deactivate_user(self, user):
        """Deactivate user."""
        user.is_active = False
        user.save(using=self._db)
    
    def create_superuser(self, email, password):
        """Create, save and return a superuser."""
        superuser = self.create_user(email, password)
        
        superuser.is_staff = True
        superuser.is_superuser = True

        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
