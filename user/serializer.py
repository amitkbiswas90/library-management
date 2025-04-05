from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import User

class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number']
        ref_name = 'CustomUserCreate' 

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'phone_number']
        ref_name = 'CustomUserDetails'  