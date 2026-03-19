"""
Views for the user API.
"""
from typing import cast

from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from user.models import UserManager
from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """User ViewSet."""
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_permissions(self):
        """We can create a user without permissions,
           for anything else we need to be authenticated.
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        
        return [permissions.IsAuthenticated()]

    def perform_destroy(self, user):
        """Deactivate the user."""
        manager = cast(UserManager, get_user_model().objects)
        manager.deactivate_user(user)
