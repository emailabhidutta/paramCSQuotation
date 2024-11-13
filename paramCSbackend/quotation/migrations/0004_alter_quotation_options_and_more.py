# Generated by Django 4.2.7 on 2024-11-13 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0003_quotation_rejection_reason_quotation_total_value'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quotation',
            options={'ordering': ['-Date', 'QuotationNo'], 'verbose_name': 'Quotation', 'verbose_name_plural': 'Quotations'},
        ),
        migrations.AlterModelOptions(
            name='quotationdetails',
            options={'verbose_name': 'Quotation Detail', 'verbose_name_plural': 'Quotation Details'},
        ),
        migrations.AlterModelOptions(
            name='quotationitemdetails',
            options={'verbose_name': 'Quotation Item Detail', 'verbose_name_plural': 'Quotation Item Details'},
        ),
        migrations.AlterModelOptions(
            name='quotationstatus',
            options={'verbose_name': 'Quotation Status', 'verbose_name_plural': 'Quotation Statuses'},
        ),
        migrations.RemoveField(
            model_name='quotationdetails',
            name='QuoteValidFrom',
        ),
        migrations.RemoveField(
            model_name='quotationdetails',
            name='QuoteValidUntil',
        ),
        migrations.AddField(
            model_name='quotation',
            name='CustomerEmail',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='QuoteValidFrom',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='QuoteValidUntil',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='Version',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='quotationdetails',
            name='Version',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='QStatusID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='quotations', to='quotation.quotationstatus'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='QuotationNo',
            field=models.CharField(max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='quotationdetails',
            name='QuoteId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='quotation.quotation'),
        ),
        migrations.AlterField(
            model_name='quotationitemdetails',
            name='QuotationDetailsId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='quotation.quotationdetails'),
        ),
        migrations.AlterField(
            model_name='quotationstatus',
            name='QStatusName',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]