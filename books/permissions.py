
from rest_framework.permissions import BasePermission
from users.models import User


class IsLibrarian(BasePermission):
    """
    Custom Permissions to only allow the librarian to perform specific actions
    """

    def has_permission(self, request, view):

        print(f"Request User: {request.user}")

        if isinstance(request.user, tuple) and len(request.user) == 2:
            user, token_data = request.user

            print(f"Token Data: {token_data}")

            # Ensure the token_data contains 'user_id'
            if 'user_id' in token_data:
                # Fetch the user from the database
                user = User.objects.get(id=token_data['user_id'])

        elif isinstance(request.user, User):
            email = request.user
            user = User.objects.get(email=email)
        else:
            return False

        return user.role == User.Role.LIBRARIAN
