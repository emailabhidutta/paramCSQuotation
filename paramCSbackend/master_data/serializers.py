from rest_framework import serializers
from .models import CustomerMaster, MaterialMaster, EmployeeMaster, EbauPriceList

class CustomerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMaster
        fields = '__all__'

class MaterialMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialMaster
        fields = '__all__'

class EmployeeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = '__all__'

class EbauPriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EbauPriceList
        fields = '__all__'

    def validate(self, data):
        """
        Check that the start date is before the end date.
        """
        if data['ValidFrom'] > data['ValidTo']:
            raise serializers.ValidationError("End date must be after start date")
        return data

class CustomerMasterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMaster
        fields = ['Customer', 'Name', 'SalesOrganization', 'City', 'Country']

class MaterialMasterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialMaster
        fields = ['Material', 'MaterialDescription', 'Plant', 'ProductGroup', 'BaseUnitOfMeasure']

class EmployeeMasterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['EmployeeNo', 'LastName', 'FirstName', 'CoCd', 'Status']

class EbauPriceListListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EbauPriceList
        fields = ['ConditionType', 'SalesOrganization', 'Material', 'Customer', 'ValidFrom', 'ValidTo', 'Rate']
