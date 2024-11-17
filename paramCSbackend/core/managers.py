from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger(__name__)

class CustomUserManager(BaseUserManager):
    def create_user(self, Name, Email, EmployeeNo, password=None, **extra_fields):
        if not Name:
            raise ValueError(_('The Name field must be set'))
        if not Email:
            raise ValueError(_('The Email field must be set'))
        if not password:
            raise ValueError(_('The password must be set'))
        
        email = self.normalize_email(Email)
        user = self.model(Name=Name, Email=email, EmployeeNo=EmployeeNo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        logger.debug(f"User created successfully: {user}")
        return user

    def create_superuser(self, Name, Email, EmployeeNo, password=None, **extra_fields):
        extra_fields.setdefault('IsActive', '1')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('RoleID'):
            from .models import Role
            try:
                admin_role, created = Role.objects.get_or_create(
                    RoleID='ADMN',
                    defaults={'RoleName': 'Administrator'}
                )
                extra_fields['RoleID'] = admin_role
            except Exception as e:
                logger.error(f"Error creating admin role: {str(e)}")
                raise

        logger.info(f"Creating superuser with Name: {Name}, Email: {Email}, EmployeeNo: {EmployeeNo}")
        return self.create_user(Name, Email, EmployeeNo, password, **extra_fields)
