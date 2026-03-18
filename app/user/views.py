"""
Views for the user API.
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets

from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """User ViewSet."""
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def perform_destroy(self, user):
        """Deactivate the user."""
        get_user_model().objects.deactivate_user(user)
