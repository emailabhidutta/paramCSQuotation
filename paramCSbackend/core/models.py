from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password
import logging
from .managers import CustomUserManager

logger = logging.getLogger(__name__)

class Role(models.Model):
    RoleID = models.CharField(max_length=4, primary_key=True)
    RoleName = models.CharField(max_length=50)

    def __str__(self):
        return self.RoleName

    class Meta:
        managed = False
        db_table = 'Role'

class CustomUser(AbstractBaseUser, PermissionsMixin):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(_('name'), max_length=50, unique=True)
    Email = models.EmailField(_('email address'), unique=True)
    EmployeeNo = models.CharField(max_length=10, null=True, blank=True)
    IsActive = models.BooleanField(default=True)
    RoleID = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, db_column='RoleID')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'Name'
    EMAIL_FIELD = 'Email'
    REQUIRED_FIELDS = ['Email', 'EmployeeNo']

    objects = CustomUserManager()

    def __str__(self):
        return self.Name

    @property
    def is_active(self):
        return self.IsActive

    def set_password(self, raw_password):
        logger.debug(f"Setting password for user {self.Name}")
        self.password = make_password(raw_password)
        logger.debug(f"New password hash: {self.password}")

    def check_password(self, raw_password):
        logger.debug(f"Checking password for user {self.Name}")
        logger.debug(f"Stored hash: {self.password}")
        logger.debug(f"Raw password: {raw_password}")
        result = check_password(raw_password, self.password)
        logger.debug(f"Check result: {result}")
        return result

    def save(self, *args, **kwargs):
        logger.debug(f"Saving user {self.Name}")
        super().save(*args, **kwargs)
        logger.debug(f"User saved. Password hash: {self.password}")

    class Meta:
        managed = False
        db_table = 'User'

class Rights(models.Model):
    RightsID = models.CharField(max_length=4, primary_key=True)
    RightName = models.CharField(max_length=50)

    def __str__(self):
        return self.RightName

    class Meta:
        managed = False
        db_table = 'Rights'

class UserRights(models.Model):
    UserRightsID = models.AutoField(primary_key=True)
    RoleID = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_rights')
    RightsID = models.ForeignKey(Rights, on_delete=models.CASCADE, related_name='user_rights')

    def __str__(self):
        return f"{self.RoleID} - {self.RightsID}"

    class Meta:
        managed = False
        db_table = 'UserRights'
        unique_together = ('RoleID', 'RightsID')

class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    PhoneNumber = models.CharField(max_length=15, null=True, blank=True)
    Department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    reset_password_token = models.CharField(max_length=100, null=True, blank=True)
    reset_password_expires = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.Name}"

    def clean(self):
        if self.PhoneNumber and not self.PhoneNumber.isdigit():
            raise ValidationError({'PhoneNumber': 'Phone number must contain only digits.'})

    def soft_delete(self):
        self.is_deleted = True
        self.user.IsActive = False
        self.user.save()
        self.save()

# Signal to create UserProfile when CustomUser is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
