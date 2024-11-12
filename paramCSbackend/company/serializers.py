from rest_framework import serializers
from .models import Country, Company, SalesOrganization, AccountGroup

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class SalesOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrganization
        fields = '__all__'

class AccountGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountGroup
        fields = '__all__'
