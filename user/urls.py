"""
URL mapping for the user API.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')

app_name = 'user'

urlpatterns = [
    path('', include(router.urls)),
]
