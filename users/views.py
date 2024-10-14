import jwt
import json
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer, UserSignupSerializer, LoginSerializer, UserUpdateSerializer
import logging
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from datetime import datetime, timezone, timedelta
from books.permissions import IsLibrarian
from users.models import User

# Create your views here.

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        print("Starting to extract user data in serializer..")
        print(request.data)

        user_serializer = UserSignupSerializer(data=request.data)
        print(user_serializer)

        if user_serializer.is_valid():
            print("User data validated successfully")
            user = user_serializer.save()

            print(f"User created successfully: {user}")
            return Response({"message": "Successfully created user"}, status=status.HTTP_201_CREATED)

        # In case the data is not valid
        print("User data validation failed")
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as error:
        logging.error(f"Error while creating user: {error}")
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    try:
        print("inside login..", request.data)
        # Instantiate the serializer with the request data
        serializer = LoginSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            user = serializer.validated_data['user']
            print("id: ", user.id)
            # payload = {
            #     'id': user.id,
            #     'exp': datetime.now(timezone.utc) + timedelta(hours=1)
            # }
            # jwt_token = jwt.encode(payload, settings.SECRET_KEY)

            # return Response({
            #     'access_token': jwt_token,
            # }, status=status.HTTP_200_OK)
            refresh = RefreshToken.for_user(user)
            print(user.to_dict()['role'])

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': user.to_dict()['role']
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as error:
        logging.error(f"Error while authenticating user: {error}")
        return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsLibrarian])
def add_member(request):
    try:
        # extract member data from the request object
        data = request.data

        user_data = {
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'password': data['password'],
            'role': 'MEMBER'
        }

        serializer = UserSignupSerializer(data=user_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as error:
        print("error while creating member: ", error)
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsLibrarian])
def update_member(request, id):
    try:
        member = User.objects.get(id=id).to_dict()
        if not member:
            return Response("Member not found", status=status.HTTP_404_NOT_FOUND)

        if member['role'] != User.Role.MEMBER:
            return Response("Only members details can be updated", status=status.HTTP_400_BAD_REQUEST)

        serializer = UserUpdateSerializer(
            member, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as error:
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsLibrarian])
def remove_member(request):
    """
    Function to remove a member from the system.
    Only librarians are allowed to delete members.
    """
    try:
        member = User.objects.get(id=id).to_dict()
        if not member:
            return Response("Member not found", status=status.HTTP_404_NOT_FOUND)

        if member['role'] != User.Role.MEMBER:
            return Response("Only members can be removed", status=status.HTTP_400_BAD_REQUEST)

        # delete the member if all above conditions satisfies
        member.delete()
        return Response({"message": "Member removed successfully."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as error:
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsLibrarian])
def view_all_members():
    try:
        members = User.objects.filter(role=User.Role.MEMBER)
        serializer = UserSerializer(members, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Member related operation


@api_view(['DELETE'])
def delete_account(request):
    try:
        user = request.user[1]['user_id']
        user.delete()

        return Response({"message": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


### Template Views ####

def librarian_signup(request):
    return render(request, 'signup_librarian.html')


def user_login(request):
    return render(request, 'login.html')


def homepage(request):
    return render(request, 'homepage.html')
