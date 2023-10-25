from rest_framework import permissions
from django.contrib.auth import get_user_model

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow update and delete operations if the user is the owner of the post
        return obj.author == request.user

class CustomAuthBackend:
    def authenticate(self, request, username=None, password=None):
        # Perform authentication as usual
        user = get_user_model().objects.get(username=username)
        if user.check_password(password):
            request.session['user_id'] = user.id  # Store the user ID in the session
            return 2
