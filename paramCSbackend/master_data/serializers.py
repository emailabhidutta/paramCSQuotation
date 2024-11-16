from rest_framework import serializers
from .models import CustomerMaster, MaterialMaster

class CustomerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMaster
        fields = '__all__'

class MaterialMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialMaster
        fields = '__all__'
