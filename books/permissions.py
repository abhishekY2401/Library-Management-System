
from rest_framework.permissions import BasePermission
from users.models import User


class IsLibrarian(BasePermission):
    """
    Custom Permissions to only allow the librarian to perform specific actions
    """

    def has_permission(self, request, view):

        if request.user == None:
            return False
        # Check if the user is a librarian
        user = User.objects.get(id=request.user[1]['user_id']).to_dict()
        return user['role'] == User.Role.LIBRARIAN
