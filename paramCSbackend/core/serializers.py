from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import Role, Rights, UserRights, CustomUser

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['RoleID', 'RoleName']

class RightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rights
        fields = ['RightsID', 'RightName']

class UserRightsSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='RoleID.RoleName', read_only=True)
    right_name = serializers.CharField(source='RightsID.RightName', read_only=True)

    class Meta:
        model = UserRights
        fields = ['UserRightsID', 'RoleID', 'RightsID', 'role_name', 'right_name']

class CustomUserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='RoleID.RoleName', read_only=True)
    full_name = serializers.SerializerMethodField()
    user_rights = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'UserID', 'Name', 'username', 'email', 'EmployeeNo', 'IsActive', 'RoleID', 
            'role_name', 'PhoneNumber', 'Department', 'full_name', 'user_rights',
            'is_superuser', 'is_staff', 'date_joined', 'last_login'
        ]
        read_only_fields = ['UserID', 'date_joined', 'last_login', 'is_superuser', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
            'reset_password_token': {'write_only': True},
            'reset_password_expires': {'write_only': True},
        }

    def get_full_name(self, obj):
        return obj.Name

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
        fields = ['UserID', 'Name', 'username', 'EmployeeNo', 'IsActive', 'role_name', 'Department']

class CustomUserDetailSerializer(CustomUserSerializer):
    class Meta(CustomUserSerializer.Meta):
        pass  # Uses all fields from CustomUserSerializer

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'username': user.username,
            'token': user.token
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['UserID', 'Name', 'email', 'PhoneNumber', 'Department', 'EmployeeNo']
        read_only_fields = ['UserID', 'EmployeeNo']

class RoleWithRightsSerializer(serializers.ModelSerializer):
    rights = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['RoleID', 'RoleName', 'rights']

    def get_rights(self, obj):
        user_rights = UserRights.objects.filter(RoleID=obj)
        return RightsSerializer(Rights.objects.filter(userrights__in=user_rights), many=True).data

class UserActivityLogSerializer(serializers.Serializer):
    user = serializers.CharField()
    action = serializers.CharField()
    timestamp = serializers.DateTimeField()
    details = serializers.JSONField()

class BulkUserCreateSerializer(serializers.Serializer):
    users = CustomUserSerializer(many=True)

    def create(self, validated_data):
        users_data = validated_data.pop('users')
        users = []
        for user_data in users_data:
            user = CustomUser.objects.create(**user_data)
            users.append(user)
        return users

class UserStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    inactive_users = serializers.IntegerField()
    users_by_role = serializers.DictField(child=serializers.IntegerField())

def get_user_stats():
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(IsActive='1').count()
    inactive_users = total_users - active_users
    users_by_role = CustomUser.objects.values('RoleID__RoleName').annotate(count=serializers.Count('UserID'))
    
    return {
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'users_by_role': {item['RoleID__RoleName']: item['count'] for item in users_by_role}
    }
