from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSignupSerializer, LoginSerializer
import logging
# Create your views here.

logger = logging.getLogger(__name__)


@api_view(['POST'])
def register_user(request):
    try:
        logging.info("starting to extract user data in serializer..")

        user_serializer = UserSignupSerializer(data=request.data)

        if user_serializer.is_valid():
            logging.info("user data validated successfully")
            user = user_serializer.save()

            logging.info(f"user created successfully: {user}")
            return Response({"message": "User created successfully", "user": user.to_dict()}, status=status.HTTP_201_CREATED)

    except Exception as error:
        logging.error(f"Error while creating user: {error}")
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    try:
        # Instantiate the serializer with the request data
        serializer = LoginSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as error:
        logging.error(f"Error while authenticating user: {error}")
        return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
