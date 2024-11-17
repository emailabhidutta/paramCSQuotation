import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Role(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    ParentRoleID = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_roles', db_column='ParentRoleID')
    RoleName = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.RoleName

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        db_table = 'core_role'
        indexes = [
            models.Index(fields=['RoleName']),
        ]

class Rights(TimeStampedModel):
    RightsID = models.CharField(max_length=4, primary_key=True)
    RightName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.RightName

    class Meta:
        verbose_name = "Right"
        verbose_name_plural = "Rights"
        db_table = 'core_rights'
        indexes = [
            models.Index(fields=['RightName']),
        ]

class UserRights(TimeStampedModel):
    UserRightsID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    RoleID = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_rights', db_column='RoleID_id')
    RightsID = models.ForeignKey(Rights, on_delete=models.CASCADE, related_name='user_rights')

    def __str__(self):
        return f"{self.RoleID} - {self.RightsID}"

    class Meta:
        verbose_name = "User Right"
        verbose_name_plural = "User Rights"
        unique_together = ('RoleID', 'RightsID')
        db_table = 'core_userrights'
        indexes = [
            models.Index(fields=['RoleID', 'RightsID']),
        ]

class CustomUser(AbstractUser):
    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('SALES', 'Sales'),
        ('FINANCE', 'Finance'),
        ('OPERATIONS', 'Operations'),
        ('MARKETING', 'Marketing'),
        ('OTHER', 'Other'),
    ]

    EmployeeNo = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    IsActive = models.BooleanField(default=True)
    RoleID = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users', db_column='RoleID')
    PhoneNumber = models.CharField(max_length=15, null=True, blank=True)
    Department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, null=True, blank=True)
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
        while current_role.ParentRoleID:  # Traverse up the role hierarchy
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
        self.is_active = False
        self.save()

    def clean(self):
        super().clean()
        if self.EmployeeNo and not self.EmployeeNo.isalnum():
            raise ValidationError({'EmployeeNo': 'Employee number must be alphanumeric.'})
        if self.PhoneNumber and not self.PhoneNumber.isdigit():
            raise ValidationError({'PhoneNumber': 'Phone number must contain only digits.'})

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = 'auth_user'
        constraints = [
            models.CheckConstraint(check=models.Q(is_active=True) | models.Q(is_deleted=True), name='active_or_deleted'),
        ]
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['EmployeeNo']),
            models.Index(fields=['Department']),
        ]
