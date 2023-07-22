# authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.utils import timezone
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class CustomJWTAuthentication(JWTAuthentication):
#     def get_user(self, validated_token):
#         user = super().get_user(validated_token)
#         # print("validated token", validated_token, user)
#         # user_role = validated_token['user']['roles']
#         # user.roles = user_role
#         return user


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        
        # print("user in jwt class", user)
        # # Update last_login field after successful authentication
        # user.last_login = timezone.now()
        
        # user.save()

        return user
