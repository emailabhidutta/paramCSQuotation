from rest_framework import serializers
from .models import Country, Company, SalesOrganization, AccountGroup

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='CountryID.CountryName', read_only=True)

    class Meta:
        model = Company
        fields = '__all__'

class SalesOrganizationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='CompanyID.CompanyName', read_only=True)

    class Meta:
        model = SalesOrganization
        fields = '__all__'

class AccountGroupSerializer(serializers.ModelSerializer):
    sales_organization_name = serializers.CharField(source='SalesOrganizationID.SalesOrganizationName', read_only=True)

    class Meta:
        model = AccountGroup
        fields = '__all__'
