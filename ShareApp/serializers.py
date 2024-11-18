from rest_framework import serializers
from rest_framework import serializers
from FilesApp.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import Group

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This email is already in use.")]
    )
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)


    class Meta:
        model = User
        fields = ['username', 'password', 'email','is_superuser','is_staff','group']

    def create(self, validated_data):
        group = validated_data.pop('group', None)

        validated_data['password'] = make_password(validated_data['password'])
        validated_data['date_joined'] = timezone.now()
        validated_data['is_active'] = False
        
        user = User.objects.create(**validated_data)
        
        if group:
            user.groups.add(group)
        return user