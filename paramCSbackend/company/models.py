from django.db import models

class Country(models.Model):
    CountryID = models.CharField(max_length=10, primary_key=True)
    CountryName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.CountryName

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class Company(models.Model):
    CompanyID = models.CharField(max_length=10, primary_key=True)
    CompanyName = models.CharField(max_length=50, unique=True)
    CountryID = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='companies')

    def __str__(self):
        return self.CompanyName

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

class SalesOrganization(models.Model):
    SalesOrganizationID = models.CharField(max_length=10, primary_key=True)
    SalesOrganizationName = models.CharField(max_length=50, unique=True)
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sales_organizations')

    def __str__(self):
        return self.SalesOrganizationName

    class Meta:
        verbose_name = "Sales Organization"
        verbose_name_plural = "Sales Organizations"

class AccountGroup(models.Model):
    AccountGroupID = models.CharField(max_length=10, primary_key=True)
    AccountGroupName = models.CharField(max_length=50, unique=True)
    SalesOrganizationID = models.ForeignKey(SalesOrganization, on_delete=models.CASCADE, related_name='account_groups')

    def __str__(self):
        return self.AccountGroupName

    class Meta:
        verbose_name = "Account Group"
        verbose_name_plural = "Account Groups"
