from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError

class Role(models.Model):
    RoleID = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users', db_column='RoleID')
    RoleName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.RoleName

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        db_table = 'core_role'  # Specify the exact table name

class Rights(models.Model):
    RightsID = models.CharField(max_length=4, primary_key=True)
    RightName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.RightName

    class Meta:
        verbose_name = "Right"
        verbose_name_plural = "Rights"
        db_table = 'core_rights'  # Specify the exact table name

class UserRights(models.Model):
    UserRightsID = models.CharField(max_length=4, primary_key=True)
    RoleID = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_rights')
    RightsID = models.ForeignKey(Rights, on_delete=models.CASCADE, related_name='user_rights')

    def __str__(self):
        return f"{self.RoleID} - {self.RightsID}"

    class Meta:
        verbose_name = "User Right"
        verbose_name_plural = "User Rights"
        unique_together = ('RoleID', 'RightsID')
        db_table = 'core_userrights'  # Specify the exact table name

class CustomUser(AbstractUser):
    EmployeeNo = models.CharField(max_length=10, null=True, blank=True)
    IsActive = models.BooleanField(default=True)
    RoleID = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')
    PhoneNumber = models.CharField(max_length=15, null=True, blank=True)
    Department = models.CharField(max_length=50, null=True, blank=True)
    UserID = models.CharField(max_length=4, unique=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    reset_password_token = models.CharField(max_length=100, null=True, blank=True)
    reset_password_expires = models.DateTimeField(null=True, blank=True)

    # Override the default fields to match your database
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

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

    def has_right(self, right_name):
        return self.get_user_rights().filter(RightsID__RightName=right_name).exists()

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
        db_table = 'auth_user'  # Specify the exact table name
