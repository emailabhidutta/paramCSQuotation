from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

class Country(models.Model):
    CountryID = models.CharField(_("Country ID"), max_length=10, primary_key=True)
    CountryName = models.CharField(_("Country Name"), max_length=50)
    SalesOrganizationID = models.CharField(_("Sales Organization ID"), max_length=10, null=True, blank=True)
    CountryCode = models.CharField(_("Country Code"), max_length=3)

    def clean(self):
        if not re.match(r'^[A-Z]{3}$', self.CountryCode):
            raise ValidationError(_('Country code must be 3 uppercase letters.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.CountryName} ({self.CountryCode})"

    class Meta:
        managed = False
        db_table = 'Country'
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ['CountryName']

class Company(models.Model):
    CompanyID = models.CharField(_("Company ID"), max_length=10, primary_key=True)
    CompanyName = models.CharField(_("Company Name"), max_length=50)
    CountryID = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='companies', verbose_name=_("Country"))

    def clean(self):
        if not re.match(r'^C\d{9}$', self.CompanyID):
            raise ValidationError(_('Company ID must start with C followed by 9 digits.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.CompanyName

    class Meta:
        managed = False
        db_table = 'Company'
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ['CompanyName']

class SalesOrganization(models.Model):
    SalesOrganizationID = models.CharField(_("Sales Organization ID"), max_length=10, primary_key=True)
    SalesOrganizationName = models.CharField(_("Sales Organization Name"), max_length=50)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sales_organizations', verbose_name=_("Company"))

    def clean(self):
        if not re.match(r'^SO\d{8}$', self.SalesOrganizationID):
            raise ValidationError(_('Sales Organization ID must start with SO followed by 8 digits.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.SalesOrganizationName

    class Meta:
        managed = False
        db_table = 'SalesOrganization'
        verbose_name = _("Sales Organization")
        verbose_name_plural = _("Sales Organizations")
        ordering = ['SalesOrganizationName']

class AccountGroup(models.Model):
    AccountGroupID = models.CharField(_("Account Group ID"), max_length=10, primary_key=True)
    AccountGroupName = models.CharField(_("Account Group Name"), max_length=50)
    SalesOrganizationID = models.ForeignKey(SalesOrganization, on_delete=models.CASCADE, related_name='account_groups', verbose_name=_("Sales Organization"))

    def clean(self):
        if not re.match(r'^AG\d{8}$', self.AccountGroupID):
            raise ValidationError(_('Account Group ID must start with AG followed by 8 digits.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.AccountGroupName

    class Meta:
        managed = False
        db_table = 'AccountGroup'
        verbose_name = _("Account Group")
        verbose_name_plural = _("Account Groups")
        ordering = ['AccountGroupName']
