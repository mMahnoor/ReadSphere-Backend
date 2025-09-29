from django.shortcuts import render
from rest_framework import viewsets, status, serializers
from api.permissions import IsAdmin
from users.serializers import GroupSerializer, UserGroupSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Create your views here.
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdmin]

class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = [IsAdmin]
