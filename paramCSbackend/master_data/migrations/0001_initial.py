# Generated by Django 5.0.9 on 2024-11-18 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerMaster',
            fields=[
                ('Customer', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('SalesOrganization', models.CharField(max_length=4)),
                ('AccountGroup', models.CharField(blank=True, max_length=4, null=True)),
                ('Name', models.CharField(blank=True, max_length=35, null=True)),
                ('Name2', models.CharField(blank=True, max_length=35, null=True)),
                ('SearchTerm', models.CharField(blank=True, max_length=20, null=True)),
                ('Street', models.CharField(blank=True, max_length=60, null=True)),
                ('City', models.CharField(blank=True, max_length=40, null=True)),
                ('Country', models.CharField(blank=True, max_length=3, null=True)),
                ('CustomerClassification', models.CharField(blank=True, max_length=2, null=True)),
                ('IndustryCode1', models.CharField(blank=True, max_length=4, null=True)),
                ('SalesGroup', models.CharField(blank=True, max_length=3, null=True)),
                ('CustPriceProcedure', models.CharField(blank=True, max_length=1, null=True)),
                ('TermsOfPayment', models.CharField(blank=True, max_length=4, null=True)),
                ('Incoterms', models.CharField(blank=True, max_length=3, null=True)),
                ('IncotermsPart2', models.CharField(blank=True, max_length=28, null=True)),
                ('Currency', models.CharField(blank=True, max_length=5, null=True)),
                ('OrderBlockForSalesArea', models.CharField(blank=True, max_length=2, null=True)),
                ('CentralDelBlock', models.CharField(blank=True, max_length=2, null=True)),
                ('Status', models.CharField(blank=True, max_length=1, null=True)),
                ('CreatedOn', models.DateField(blank=True, null=True)),
                ('CreatedSource', models.CharField(blank=True, max_length=50, null=True)),
                ('LastUpdate', models.DateField(blank=True, null=True)),
                ('UpdatedSource', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeMaster',
            fields=[
                ('EmployeeNo', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('LastName', models.CharField(blank=True, max_length=50, null=True)),
                ('FirstName', models.CharField(blank=True, max_length=50, null=True)),
                ('CoCd', models.CharField(blank=True, max_length=4, null=True)),
                ('Status', models.CharField(blank=True, max_length=1, null=True)),
                ('OntrackID', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialMaster',
            fields=[
                ('Material', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('Plant', models.CharField(blank=True, max_length=4, null=True)),
                ('MaterialDescription', models.CharField(blank=True, max_length=255, null=True)),
                ('XPlantMatlStatus', models.CharField(blank=True, max_length=50, null=True)),
                ('DrawingNo', models.CharField(blank=True, max_length=35, null=True)),
                ('Description', models.CharField(blank=True, max_length=255, null=True)),
                ('DescriptionText', models.TextField(blank=True, null=True)),
                ('BasicMaterial', models.CharField(blank=True, max_length=50, null=True)),
                ('BasicMaterialDesc', models.CharField(blank=True, max_length=255, null=True)),
                ('MachineType', models.CharField(blank=True, max_length=50, null=True)),
                ('ProductGroup', models.CharField(blank=True, max_length=50, null=True)),
                ('ProductType', models.CharField(blank=True, max_length=50, null=True)),
                ('Lifecycle', models.CharField(blank=True, max_length=50, null=True)),
                ('OldMaterialNumber', models.CharField(blank=True, max_length=18, null=True)),
                ('ProductHierarchy', models.CharField(blank=True, max_length=50, null=True)),
                ('BaseUnitOfMeasure', models.CharField(blank=True, max_length=3, null=True)),
                ('Status', models.CharField(blank=True, max_length=1, null=True)),
                ('CreatedOn', models.DateField(blank=True, null=True)),
                ('CreatedSource', models.CharField(blank=True, max_length=50, null=True)),
                ('LastUpdate', models.DateField(blank=True, null=True)),
                ('UpdatedSource', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EbauPriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ConditionType', models.CharField(max_length=4)),
                ('SalesOrganization', models.CharField(max_length=4)),
                ('DistributionChannel', models.CharField(max_length=2)),
                ('SalesGroup', models.CharField(max_length=3)),
                ('Material', models.CharField(max_length=18)),
                ('Customer', models.CharField(max_length=10)),
                ('ValidTo', models.DateField(blank=True, null=True)),
                ('ValidFrom', models.DateField()),
                ('Rate', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('ConditionCurrency', models.CharField(blank=True, max_length=5, null=True)),
                ('PricingUnit', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('UnitOfMeasure', models.CharField(blank=True, max_length=3, null=True)),
                ('ScaleBasis', models.CharField(blank=True, max_length=50, null=True)),
                ('DeletionIndicator', models.CharField(blank=True, max_length=1, null=True)),
                ('Status', models.CharField(blank=True, max_length=1, null=True)),
                ('CreatedOn', models.DateField(blank=True, null=True)),
                ('CreatedSource', models.CharField(blank=True, max_length=50, null=True)),
                ('LastUpdate', models.DateField(blank=True, null=True)),
                ('UpdatedSource', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'unique_together': {('ConditionType', 'SalesOrganization', 'DistributionChannel', 'SalesGroup', 'Material', 'Customer', 'ValidFrom')},
            },
        ),
    ]
