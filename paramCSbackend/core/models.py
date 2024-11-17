import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError

class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    ParentRoleID = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_roles', db_column='ParentRoleID')
    RoleName = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.RoleName

    class Meta:
        db_table = 'core_role'

class Rights(models.Model):
    RightsID = models.CharField(max_length=4, primary_key=True)
    RightName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.RightName

    class Meta:
        db_table = 'core_rights'

class UserRights(models.Model):
    UserRightsID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    RoleID = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_rights', db_column='RoleID_id')
    RightsID = models.ForeignKey(Rights, on_delete=models.CASCADE, related_name='user_rights')

    def __str__(self):
        return f"{self.RoleID} - {self.RightsID}"

    class Meta:
        db_table = 'core_userrights'
        unique_together = ('RoleID', 'RightsID')

class CustomUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    EmployeeNo = models.CharField(max_length=10, null=True, blank=True)
    IsActive = models.BooleanField(default=True)
    RoleID = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users', db_column='RoleID')
    PhoneNumber = models.CharField(max_length=15, null=True, blank=True)
    Department = models.CharField(max_length=50, null=True, blank=True)
    UserID = models.CharField(max_length=4, unique=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    reset_password_token = models.CharField(max_length=100, null=True, blank=True)
    reset_password_expires = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.get_full_name() or self.username

    def get_user_rights(self):
        if self.RoleID:
            return UserRights.objects.filter(RoleID=self.RoleID)
        return UserRights.objects.none()

    def get_all_rights(self):
        if not self.RoleID:
            return set()
        
        rights = set(self.get_user_rights().values_list('RightsID__RightName', flat=True))
        current_role = self.RoleID
        while current_role.ParentRoleID:
            parent_rights = UserRights.objects.filter(RoleID=current_role.ParentRoleID).values_list('RightsID__RightName', flat=True)
            rights.update(parent_rights)
            current_role = current_role.ParentRoleID
        return rights

    def has_right(self, right_name):
        return right_name in self.get_all_rights()

    def has_role(self, role_name):
        return self.RoleID and self.RoleID.RoleName == role_name

    def soft_delete(self):
        self.is_deleted = True
        self.IsActive = False
        self.save()

    def clean(self):
        super().clean()
        if self.EmployeeNo and not self.EmployeeNo.isalnum():
            raise ValidationError({'EmployeeNo': 'Employee number must be alphanumeric.'})
        if self.PhoneNumber and not self.PhoneNumber.isdigit():
            raise ValidationError({'PhoneNumber': 'Phone number must contain only digits.'})

    class Meta:
        db_table = 'auth_user'