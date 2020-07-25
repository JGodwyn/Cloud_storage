from . import serializers
from rest_framework import generics
from ..models import User, Folder, Files, LoggedIn


class UserCreateList(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset =  User.objects.all()

    def get_queryset(self):
        return User.objects.order_by('-date_joined')


class UserRUDList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    lookup_field = 'id'
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.all()


class FolderCreateList(generics.ListCreateAPIView):
    serializer_class = serializers.FolderSerializer
    queryset = Folder.objects.all()

    def get_queryset(self):
        return Folder.objects.order_by('-date_created')


class FolderRUDList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.FolderSerializer
    lookup_field = 'id'
    queryset = Folder.objects.all()

    def get_queryset(self):
        return Folder.objects.all()
