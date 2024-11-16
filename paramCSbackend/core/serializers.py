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
    role_name = serializers.CharField(source='RoleID.RoleName', read_only=True)
    right_name = serializers.CharField(source='RightsID.RightName', read_only=True)

    class Meta:
        model = UserRights
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='RoleID.RoleName', read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)
