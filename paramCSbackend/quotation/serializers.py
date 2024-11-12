from rest_framework import serializers
from django.db import transaction
from .models import QuotationStatus, Quotation, QuotationDetails, QuotationItemDetails
from core.serializers import CustomUserSerializer
from company.serializers import SalesOrganizationSerializer

class QuotationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationStatus
        fields = '__all__'

class QuotationItemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItemDetails
        fields = '__all__'

class QuotationDetailsSerializer(serializers.ModelSerializer):
    items = QuotationItemDetailsSerializer(many=True, read_only=True, source='quotationitemdetails_set')
    SalesOrganization = SalesOrganizationSerializer(read_only=True)

    class Meta:
        model = QuotationDetails
        fields = '__all__'

class QuotationSerializer(serializers.ModelSerializer):
    details = QuotationDetailsSerializer(many=True, read_only=True, source='quotationdetails_set')
    QStatusID = QuotationStatusSerializer(read_only=True)
    created_by = CustomUserSerializer(read_only=True)
    last_modified_by = CustomUserSerializer(read_only=True)
    status = serializers.CharField(source='QStatusID.QStatusName', read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    total_value = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Quotation
        fields = '__all__'
        read_only_fields = ('total_value', 'created_by', 'last_modified_by', 'Date', 'CreationDate')

    @transaction.atomic
    def create(self, validated_data):
        details_data = self.context['request'].data.get('details', [])
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['last_modified_by'] = user
        quotation = Quotation.objects.create(**validated_data)

        for detail_data in details_data:
            items_data = detail_data.pop('items', [])
            quotation_detail = QuotationDetails.objects.create(QuoteId=quotation, **detail_data)

            for item_data in items_data:
                QuotationItemDetails.objects.create(QuotationDetailsId=quotation_detail, **item_data)

        quotation.calculate_total_value()
        return quotation

    @transaction.atomic
    def update(self, instance, validated_data):
        details_data = self.context['request'].data.get('details', [])
        user = self.context['request'].user
        validated_data['last_modified_by'] = user
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for detail_data in details_data:
            items_data = detail_data.pop('items', [])
            detail_id = detail_data.get('QuotationDetailsId')

            if detail_id:
                quotation_detail = QuotationDetails.objects.get(QuotationDetailsId=detail_id)
                for attr, value in detail_data.items():
                    setattr(quotation_detail, attr, value)
                quotation_detail.save()
            else:
                quotation_detail = QuotationDetails.objects.create(QuoteId=instance, **detail_data)

            for item_data in items_data:
                item_id = item_data.get('QuoteItemId')

                if item_id:
                    quotation_item = QuotationItemDetails.objects.get(QuoteItemId=item_id)
