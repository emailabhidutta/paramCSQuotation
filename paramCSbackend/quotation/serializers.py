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
    items = QuotationItemDetailsSerializer(many=True, read_only=True)
    SalesOrganization = SalesOrganizationSerializer(read_only=True)

    class Meta:
        model = QuotationDetails
        fields = '__all__'

class QuotationSerializer(serializers.ModelSerializer):
    details = QuotationDetailsSerializer(many=True, read_only=True)
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

    def validate(self, data):
        if data.get('QuoteValidFrom') and data.get('QuoteValidUntil'):
            if data['QuoteValidFrom'] > data['QuoteValidUntil']:
                raise serializers.ValidationError("QuoteValidFrom must be before QuoteValidUntil")
        return data

    @transaction.atomic
    def create(self, validated_data):
        details_data = self.context['request'].data.get('details', [])
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['last_modified_by'] = user
        quotation = Quotation.objects.create(**validated_data)

        for detail_data in details_data:
            items_data = detail_data.pop('items', [])
            detail = QuotationDetails.objects.create(QuoteId=quotation, **detail_data)

            for item_data in items_data:
                QuotationItemDetails.objects.create(QuotationDetailsId=detail, **item_data)

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

        existing_details = {detail.QuotationDetailsId: detail for detail in instance.details.all()}
        
        for detail_data in details_data:
            items_data = detail_data.pop('items', [])
            detail_id = detail_data.get('QuotationDetailsId')

            if detail_id and detail_id in existing_details:
                detail = existing_details.pop(detail_id)
                for attr, value in detail_data.items():
                    setattr(detail, attr, value)
                detail.save()
            else:
                detail = QuotationDetails.objects.create(QuoteId=instance, **detail_data)

            existing_items = {item.QuoteItemId: item for item in detail.items.all()}
            
            for item_data in items_data:
                item_id = item_data.get('QuoteItemId')

                if item_id and item_id in existing_items:
                    item = existing_items.pop(item_id)
                    for attr, value in item_data.items():
                        setattr(item, attr, value)
                    item.save()
                else:
                    QuotationItemDetails.objects.create(QuotationDetailsId=detail, **item_data)

            # Mark remaining items as deleted
            for item in existing_items.values():
                item.IsDeleted = True
                item.save()

        # Mark remaining details as deleted
        for detail in existing_details.values():
            detail.IsDeleted = True
            detail.save()

        instance.calculate_total_value()
        return instance

class QuotationListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='QStatusID.QStatusName', read_only=True)
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Quotation
        fields = ['QuoteId', 'QuotationNo', 'CustomerNumber', 'customer_name', 'Date', 'CreationDate', 'status', 'total_value']

    def get_customer_name(self, obj):
        detail = obj.details.first()
        return detail.CustomerName if detail else None

class QuotationSummarySerializer(serializers.Serializer):
    total_quotations = serializers.IntegerField()
    quotation_status = serializers.ListField(child=serializers.DictField())
    recent_quotations = serializers.ListField(child=serializers.DictField())
    total_value = serializers.DecimalField(max_digits=15, decimal_places=2)
