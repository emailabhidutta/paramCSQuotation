from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models, connection
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, Name, password=None, **extra_fields):
        if not Name:
            raise ValueError('The Name field must be set')
        user = self.model(Name=Name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Name, password=None, **extra_fields):
        extra_fields.setdefault('IsActive', '1')
        user = self.create_user(Name, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        return user

class Role(models.Model):
    RoleID = models.CharField(max_length=4, primary_key=True)
    RoleName = models.CharField(max_length=50)

    def __str__(self):
        return self.RoleName

    class Meta:
        db_table = 'Role'

class CustomUser(AbstractBaseUser):
    UserID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=50, unique=True)
    EmployeeNo = models.CharField(max_length=10, null=True, blank=True)
    IsActive = models.CharField(max_length=1, default='1')
    RoleID = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, db_column='RoleID')

    USERNAME_FIELD = 'Name'
    REQUIRED_FIELDS = ['RoleID']

    objects = CustomUserManager()

    def __str__(self):
        return self.Name

    @property
    def is_active(self):
        return self.IsActive == '1'

    @property
    def is_staff(self):
        return self.RoleID.RoleName == 'Admin' if self.RoleID else False

    @property
    def is_superuser(self):
        return self.RoleID.RoleName == 'Admin' if self.RoleID else False

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        managed = False
        db_table = 'User'

    def save(self, *args, **kwargs):
        if not self.UserID:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO [User] (Name, EmployeeNo, IsActive, RoleID) VALUES (%s, %s, %s, %s); SELECT SCOPE_IDENTITY();", 
                               [self.Name, self.EmployeeNo, self.IsActive, self.RoleID_id])
                self.UserID = cursor.fetchone()[0]
        else:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE [User] SET Name = %s, EmployeeNo = %s, IsActive = %s, RoleID = %s WHERE UserID = %s", 
                               [self.Name, self.EmployeeNo, self.IsActive, self.RoleID_id, self.UserID])

    def set_password(self, raw_password):
        hashed_password = make_password(raw_password)
        with connection.cursor() as cursor:
            cursor.execute("UPDATE [User] SET Password = %s WHERE UserID = %s", [hashed_password, self.UserID])

    def check_password(self, raw_password):
        with connection.cursor() as cursor:
            cursor.execute("SELECT Password FROM [User] WHERE UserID = %s", [self.UserID])
            row = cursor.fetchone()
            if row:
                return check_password(raw_password, row[0])
        return False

    @property
    def last_login(self):
        return None

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
        self.user.IsActive = '0'
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
