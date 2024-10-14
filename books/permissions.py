
from rest_framework.permissions import BasePermission
from users.models import User


class IsLibrarian(BasePermission):
    """
    Custom Permissions to only allow the librarian to perform specific actions
    """

    def has_permission(self, request, view):
        if isinstance(request.user, tuple) and len(request.user) == 2:
            user, token_data = request.user

            # Ensure the token_data contains 'user_id'
            if 'user_id' in token_data:
                # Fetch the user from the database
                user = User.objects.get(id=token_data['user_id'])
                # Check if the user's role is LIBRARIAN
                return user.role == User.Role.LIBRARIAN

        return False
