
from users.models import User
from rest_framework.permissions import BasePermission


# User = get_user_model()


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        print(request.user[0])

        user_id = User.objects.get(email=request.user[0]).to_dict()['id']

        print("user_id: ", user_id)

        if user_id == request.user[1]['user_id']:
            return True

        return False
