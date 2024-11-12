from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    RoleID = models.CharField(max_length=10, primary_key=True)
    RoleName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.RoleName

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

class Rights(models.Model):
    RightsID = models.CharField(max_length=4, primary_key=True)
    RightName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.RightName

    class Meta:
        verbose_name = "Right"
        verbose_name_plural = "Rights"

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

class CustomUser(AbstractUser):
    EmployeeNo = models.CharField(max_length=10, null=True, blank=True)
    IsActive = models.BooleanField(default=True)
    RoleID = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')
    PhoneNumber = models.CharField(max_length=15, null=True, blank=True)
    Department = models.CharField(max_length=50, null=True, blank=True)
    UserID = models.CharField(max_length=4, unique=True, null=True, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username

    def get_user_rights(self):
        if self.RoleID:
            return UserRights.objects.filter(RoleID=self.RoleID)
        return UserRights.objects.none()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
