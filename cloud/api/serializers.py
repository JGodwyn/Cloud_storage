from rest_framework import serializers
from ..models import User, Folder, Files, LoggedIn
from django.contrib.auth import hashers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'about',
            'date_joined'
        ]

        read_only_fields = ['date_joined']

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact = value)
        if self.instance:
            qs = qs.exclude(id = self.instance.id)
        if qs.exists():
            raise serializers.ValidationError('That name already exists')
        return value

    def validate_password(self, value):
        password = hashers.make_password(value)
        return password


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = [
            'id',
            'user_link',
            'name',
            'description',
            'date_created',
        ]

    read_only_fields = ['date_created']
