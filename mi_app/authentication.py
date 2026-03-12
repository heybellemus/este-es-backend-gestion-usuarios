# mi_app/authentication.py
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Usuarios

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            user = Usuarios.objects.get(usuarioid=user_id)
            return user
        except (Usuarios.DoesNotExist, KeyError):
            return None
