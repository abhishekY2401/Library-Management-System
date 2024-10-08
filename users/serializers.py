from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from users.models import User


class UserSignupSerializer(serializers.ModelSerializer):

    # define all the user fields to validate the user data
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True, min_length=10)
    role = serializers.ChoiceField(choices=User.Role.choices)
    is_authenticated = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'password', 'role', 'status', 'is_authenticated']

    def create(self, validated_data):

        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(min_length=10)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        # Use check_password to verify the provided password
        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid email or password")

        attrs['user'] = user
        return attrs
