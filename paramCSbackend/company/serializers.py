from rest_framework import serializers
from .models import Country, Company, SalesOrganization, AccountGroup

class CountrySerializer(serializers.ModelSerializer):
    company_count = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['CountryID', 'CountryName', 'CountryCode', 'SalesOrganizationID', 'company_count']

    def get_company_count(self, obj):
        return obj.companies.count()

class CompanySerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='CountryID.CountryName', read_only=True)
    country_code = serializers.CharField(source='CountryID.CountryCode', read_only=True)
    sales_organization_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['CompanyID', 'CompanyName', 'CountryID', 'country_name', 'country_code', 'sales_organization_count']

    def get_sales_organization_count(self, obj):
        return obj.sales_organizations.count()

    def validate_CompanyID(self, value):
        if not value.startswith('C') or not value[1:].isdigit() or len(value) != 10:
            raise serializers.ValidationError("Company ID must start with C followed by 9 digits.")
        return value

class SalesOrganizationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='CompanyID.CompanyName', read_only=True)
    account_group_count = serializers.SerializerMethodField()

    class Meta:
        model = SalesOrganization
        fields = ['SalesOrganizationID', 'SalesOrganizationName', 'CompanyID', 'company_name', 'account_group_count']

    def get_account_group_count(self, obj):
        return obj.account_groups.count()

    def validate_SalesOrganizationID(self, value):
        if not value.startswith('SO') or not value[2:].isdigit() or len(value) != 10:
            raise serializers.ValidationError("Sales Organization ID must start with SO followed by 8 digits.")
        return value

class AccountGroupSerializer(serializers.ModelSerializer):
    sales_organization_name = serializers.CharField(source='SalesOrganizationID.SalesOrganizationName', read_only=True)
    company_name = serializers.SerializerMethodField()

    class Meta:
        model = AccountGroup
        fields = ['AccountGroupID', 'AccountGroupName', 'SalesOrganizationID', 'sales_organization_name', 'company_name']

    def get_company_name(self, obj):
        return obj.SalesOrganizationID.CompanyID.CompanyName

    def validate_AccountGroupID(self, value):
        if not value.startswith('AG') or not value[2:].isdigit() or len(value) != 10:
            raise serializers.ValidationError("Account Group ID must start with AG followed by 8 digits.")
        return value

class CountryDetailSerializer(CountrySerializer):
    companies = CompanySerializer(many=True, read_only=True)

    class Meta(CountrySerializer.Meta):
        fields = CountrySerializer.Meta.fields + ['companies']

class CompanyDetailSerializer(CompanySerializer):
    sales_organizations = SalesOrganizationSerializer(many=True, read_only=True)

    class Meta(CompanySerializer.Meta):
        fields = CompanySerializer.Meta.fields + ['sales_organizations']

class SalesOrganizationDetailSerializer(SalesOrganizationSerializer):
    account_groups = AccountGroupSerializer(many=True, read_only=True)

    class Meta(SalesOrganizationSerializer.Meta):
        fields = SalesOrganizationSerializer.Meta.fields + ['account_groups']

# New serializers for list views
class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['CountryID', 'CountryName', 'CountryCode']

class CompanyListSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='CountryID.CountryName', read_only=True)

    class Meta:
        model = Company
        fields = ['CompanyID', 'CompanyName', 'country_name']

class SalesOrganizationListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='CompanyID.CompanyName', read_only=True)

    class Meta:
        model = SalesOrganization
        fields = ['SalesOrganizationID', 'SalesOrganizationName', 'company_name']

class AccountGroupListSerializer(serializers.ModelSerializer):
    sales_organization_name = serializers.CharField(source='SalesOrganizationID.SalesOrganizationName', read_only=True)

    class Meta:
        model = AccountGroup
        fields = ['AccountGroupID', 'AccountGroupName', 'sales_organization_name']
