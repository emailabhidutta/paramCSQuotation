# Generated by Django 5.0.9 on 2024-11-18 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountGroup',
            fields=[
                ('AccountGroupID', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Account Group ID')),
                ('AccountGroupName', models.CharField(max_length=50, verbose_name='Account Group Name')),
            ],
            options={
                'verbose_name': 'Account Group',
                'verbose_name_plural': 'Account Groups',
                'db_table': 'AccountGroup',
                'ordering': ['AccountGroupName'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('CompanyID', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Company ID')),
                ('CompanyName', models.CharField(max_length=50, verbose_name='Company Name')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'db_table': 'Company',
                'ordering': ['CompanyName'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('CountryID', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Country ID')),
                ('CountryName', models.CharField(max_length=50, verbose_name='Country Name')),
                ('SalesOrganizationID', models.CharField(blank=True, max_length=10, null=True, verbose_name='Sales Organization ID')),
                ('CountryCode', models.CharField(max_length=3, verbose_name='Country Code')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'db_table': 'Country',
                'ordering': ['CountryName'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SalesOrganization',
            fields=[
                ('SalesOrganizationID', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Sales Organization ID')),
                ('SalesOrganizationName', models.CharField(max_length=50, verbose_name='Sales Organization Name')),
            ],
            options={
                'verbose_name': 'Sales Organization',
                'verbose_name_plural': 'Sales Organizations',
                'db_table': 'SalesOrganization',
                'ordering': ['SalesOrganizationName'],
                'managed': False,
            },
        ),
    ]
