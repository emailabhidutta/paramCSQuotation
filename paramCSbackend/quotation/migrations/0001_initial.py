# Generated by Django 5.0.9 on 2024-11-18 00:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('QuoteID', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('QuotationNo', models.CharField(max_length=8, unique=True)),
                ('CustomerNumber', models.CharField(max_length=10)),
                ('LastRevision', models.CharField(max_length=2)),
                ('CustomerInquiryNo', models.CharField(blank=True, max_length=35, null=True)),
                ('Date', models.DateField(default=django.utils.timezone.now)),
                ('CreationDate', models.DateField(auto_now_add=True)),
                ('total_value', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('QuoteValidFrom', models.DateField(blank=True, null=True)),
                ('QuoteValidUntil', models.DateField(blank=True, null=True)),
                ('CustomerEmail', models.EmailField(blank=True, max_length=254, null=True)),
                ('Version', models.PositiveIntegerField(default=1)),
                ('Remarks', models.TextField(blank=True, null=True)),
                ('GSTVATValue', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('TotalDiscount', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
            ],
            options={
                'verbose_name': 'Quotation',
                'verbose_name_plural': 'Quotations',
                'db_table': 'Quotation',
                'ordering': ['-CreationDate', 'QuotationNo'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QuotationDetails',
            fields=[
                ('QuotationDetailsId', models.AutoField(primary_key=True, serialize=False)),
                ('QuoteRevisionNo', models.CharField(max_length=2)),
                ('QuoteRevisionDate', models.DateField(default=django.utils.timezone.now)),
                ('CustomerInquiryNo', models.CharField(blank=True, max_length=35, null=True)),
                ('SoldToCustomerNumber', models.CharField(max_length=10)),
                ('ShipToCustomerNumber', models.CharField(blank=True, max_length=10, null=True)),
                ('SalesGroup', models.CharField(blank=True, max_length=3, null=True)),
                ('Customer', models.CharField(blank=True, max_length=35, null=True)),
                ('CustomerName', models.CharField(blank=True, max_length=35, null=True)),
                ('CustomerName2', models.CharField(blank=True, max_length=35, null=True)),
                ('IndustryCode1', models.CharField(blank=True, max_length=10, null=True)),
                ('CustPriceProcedure', models.CharField(blank=True, max_length=20, null=True)),
                ('MaterialDisplay', models.CharField(blank=True, max_length=40, null=True)),
                ('TermOfPayment', models.CharField(blank=True, max_length=4, null=True)),
                ('Incoterms', models.CharField(blank=True, max_length=3, null=True)),
                ('IncotermsPart2', models.CharField(blank=True, max_length=28, null=True)),
                ('TradingCurrency', models.CharField(max_length=5)),
                ('QuoteValidFrom', models.DateField()),
                ('QuoteValidUntil', models.DateField()),
                ('SalesEmployeeNo', models.CharField(blank=True, max_length=8, null=True)),
                ('DeliveryDate', models.DateField(blank=True, null=True)),
                ('CustomerPONumber', models.CharField(blank=True, max_length=35, null=True)),
                ('ApprovalStatus', models.CharField(max_length=1)),
                ('Version', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Quotation Detail',
                'verbose_name_plural': 'Quotation Details',
                'db_table': 'QuotationDetails',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QuotationItemDetails',
            fields=[
                ('QuoteItemId', models.AutoField(primary_key=True, serialize=False)),
                ('MaterialNumber', models.CharField(max_length=18)),
                ('CustomerMatNumber', models.CharField(blank=True, max_length=18, null=True)),
                ('FullMaterialDescription', models.CharField(blank=True, max_length=255, null=True)),
                ('MaterialDescription', models.CharField(blank=True, max_length=255, null=True)),
                ('BasicMaterialText', models.CharField(blank=True, max_length=255, null=True)),
                ('DrawingNo', models.CharField(blank=True, max_length=35, null=True)),
                ('PricePer', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Per', models.DecimalField(decimal_places=2, max_digits=5)),
                ('UnitOfMeasure', models.CharField(max_length=3)),
                ('DiscountValue', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('SurchargeValue', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('OrderQuantity', models.DecimalField(decimal_places=3, max_digits=13)),
                ('OrderValue', models.DecimalField(decimal_places=2, max_digits=15)),
                ('ItemText', models.CharField(blank=True, max_length=255, null=True)),
                ('Usage', models.CharField(blank=True, max_length=1, null=True)),
                ('IsDeleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Quotation Item Detail',
                'verbose_name_plural': 'Quotation Item Details',
                'db_table': 'QuotationItemDetails',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QuotationStatus',
            fields=[
                ('QStatusID', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('QStatusName', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Quotation Status',
                'verbose_name_plural': 'Quotation Statuses',
                'db_table': 'QuotationStatus',
                'managed': False,
            },
        ),
    ]
