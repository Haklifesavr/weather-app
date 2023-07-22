from rest_framework import serializers
from .models import MyUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from django.utils import timezone

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
        username_field = MyUser.EMAIL_FIELD

        def validate(self, attrs):
            data = super().validate(attrs)
            user = self.user  # Access the authenticated user here

            # Add user role to token payload
            data['user'] = {
                'roles': user.roles,
                # Add any other user-related information you want in the token payload
            }

            return data
        

class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(read_only=True)
    print("debug login counts", last_login)
    class Meta:
        model = MyUser
        # fields = ('id', 'username', 'email', 'first_name', 'last_name', 'last_login', 'login_count')
        fields = ('id', 'email', 'first_name', 'last_name', 'roles', 'last_login', 'login_count')


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            )

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = MyUser
        fields = ('password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
    
    def validate_email(self, value):
        """
        Check if a user with the given email already exists.
        """
        if MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = MyUser.objects.create(
            # username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user