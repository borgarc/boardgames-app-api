"""
Serializers for the user API View.
"""

from typing import cast

from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import UserManager


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'is_active']
        extra_kwargs = {
            'password': {
                'write_only': True, 
                'min_length': 5,
            }
        }

    def create(self, validated_data):
        """Create and return the user object."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, user, validated_data):
        """Update user hashing pass if necesary."""
        manager = cast(UserManager, get_user_model().objects)
        return manager.update_user(user, **validated_data)
