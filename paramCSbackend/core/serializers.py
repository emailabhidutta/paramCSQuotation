from rest_framework import serializers
from .models import Role, Rights, UserRights, CustomUser

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class RightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rights
        fields = '__all__'

class UserRightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRights
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'Password': {'write_only': True}}
