# Generated by Django 5.1.3 on 2024-11-17 10:37

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rights',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('RightsID', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('RightName', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Right',
                'verbose_name_plural': 'Rights',
                'db_table': 'core_rights',
                'indexes': [models.Index(fields=['RightName'], name='core_rights_RightNa_0f0d21_idx')],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('RoleName', models.CharField(max_length=100, unique=True)),
                ('ParentRoleID', models.ForeignKey(blank=True, db_column='ParentRoleID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_roles', to='core.role')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'db_table': 'core_role',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('EmployeeNo', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
                ('IsActive', models.BooleanField(default=True)),
                ('PhoneNumber', models.CharField(blank=True, max_length=15, null=True)),
                ('Department', models.CharField(blank=True, choices=[('HR', 'Human Resources'), ('IT', 'Information Technology'), ('SALES', 'Sales'), ('FINANCE', 'Finance'), ('OPERATIONS', 'Operations'), ('MARKETING', 'Marketing'), ('OTHER', 'Other')], max_length=50, null=True)),
                ('UserID', models.CharField(blank=True, max_length=4, null=True, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('reset_password_token', models.CharField(blank=True, max_length=100, null=True)),
                ('reset_password_expires', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customuser_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('RoleID', models.ForeignKey(db_column='RoleID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='core.role')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserRights',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('UserRightsID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('RightsID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_rights', to='core.rights')),
                ('RoleID', models.ForeignKey(db_column='RoleID_id', on_delete=django.db.models.deletion.CASCADE, related_name='user_rights', to='core.role')),
            ],
            options={
                'verbose_name': 'User Right',
                'verbose_name_plural': 'User Rights',
                'db_table': 'core_userrights',
            },
        ),
        migrations.AddIndex(
            model_name='role',
            index=models.Index(fields=['RoleName'], name='core_role_RoleNam_25e28b_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['username'], name='auth_user_usernam_f2740e_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['email'], name='auth_user_email_ece7f7_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['EmployeeNo'], name='auth_user_Employe_b108d5_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['Department'], name='auth_user_Departm_76d3dd_idx'),
        ),
        migrations.AddConstraint(
            model_name='customuser',
            constraint=models.CheckConstraint(condition=models.Q(('is_active', True), ('is_deleted', True), _connector='OR'), name='active_or_deleted'),
        ),
        migrations.AddIndex(
            model_name='userrights',
            index=models.Index(fields=['RoleID', 'RightsID'], name='core_userri_RoleID__d04436_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='userrights',
            unique_together={('RoleID', 'RightsID')},
        ),
    ]
