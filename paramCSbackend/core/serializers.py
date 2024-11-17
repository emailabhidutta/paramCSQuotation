from rest_framework import serializers
from .models import Role, Rights, UserRights, CustomUser

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'RoleID', 'RoleName', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class RightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rights
        fields = ['RightsID', 'RightName', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class UserRightsSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='RoleID.RoleName', read_only=True)
    right_name = serializers.CharField(source='RightsID.RightName', read_only=True)

    class Meta:
        model = UserRights
        fields = ['UserRightsID', 'RoleID', 'RightsID', 'role_name', 'right_name', 'created_at', 'updated_at']
        read_only_fields = ['UserRightsID', 'created_at', 'updated_at']

class CustomUserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='RoleID.RoleName', read_only=True)
    full_name = serializers.SerializerMethodField()
    user_rights = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'UserID', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'EmployeeNo', 'IsActive', 'RoleID', 'role_name', 'PhoneNumber', 'Department',
            'is_deleted', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login',
            'user_rights'
        ]
        read_only_fields = ['id', 'UserID', 'date_joined', 'last_login', 'is_superuser', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
            'reset_password_token': {'write_only': True},
            'reset_password_expires': {'write_only': True},
        }

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_user_rights(self, obj):
        return list(obj.get_all_rights())

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

class CustomUserListSerializer(CustomUserSerializer):
    class Meta(CustomUserSerializer.Meta):
        fields = ['id', 'UserID', 'username', 'full_name', 'EmployeeNo', 'IsActive', 'role_name', 'Department']

class CustomUserDetailSerializer(CustomUserSerializer):
    class Meta(CustomUserSerializer.Meta):
        pass  # Uses all fields from CustomUserSerializer

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Add any password validation logic here
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Add any password validation logic here
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
