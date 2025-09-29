from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 
                  'email', 'password', 'address', 
                  'phone_number']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id', 'email', 'first_name',
                  'last_name', 'address', 'phone_number']
        
class UserGroupSerializer(serializers.ModelSerializer):
    """
    Users with assigned groups
    """
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'groups']

class PermissionSerializer(serializers.ModelSerializer):
    """
    This displays permissions available for assigning to groups created
    """
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']

class GroupSerializer(serializers.ModelSerializer):
    """
    This is for admin doing CRUD operations over Groups
    """
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        write_only=True,
        source='permissions'
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'permission_ids']
