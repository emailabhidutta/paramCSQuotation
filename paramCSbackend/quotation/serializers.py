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

    def validate(self, data):
        # Add any custom validation here
        return data

    @transaction.atomic
    def create(self, validated_data):
        details_data = self.context['request'].data.get('details', [])
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['last_modified_by'] = user
        quotation = Quotation.objects.create(**validated_data)

        details_to_create = []
        items_to_create = []

        for detail_data in details_data:
            items_data = detail_data.pop('items', [])
            detail = QuotationDetails(QuoteId=quotation, **detail_data)
            details_to_create.append(detail)

            for item_data in items_data:
                item = QuotationItemDetails(QuotationDetailsId=detail, **item_data)
                items_to_create.append(item)

        QuotationDetails.objects.bulk_create(details_to_create)
        QuotationItemDetails.objects.bulk_create(items_to_create)

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

        existing_details = {detail.QuotationDetailsId: detail for detail in instance.quotationdetails_set.all()}
        details_to_create = []
        details_to_update = []
        items_to_create = []
        items_to_update = []

        for detail_data in details_data:
            items_data = detail_data.pop('items', [])
            detail_id = detail_data.get('QuotationDetailsId')

            if detail_id and detail_id in existing_details:
                detail = existing_details[detail_id]
                for attr, value in detail_data.items():
                    setattr(detail, attr, value)
                details_to_update.append(detail)
            else:
                detail = QuotationDetails(QuoteId=instance, **detail_data)
                details_to_create.append(detail)

            existing_items = {item.QuoteItemId: item for item in detail.quotationitemdetails_set.all()}
            
            for item_data in items_data:
                item_id = item_data.get('QuoteItemId')

                if item_id and item_id in existing_items:
                    item = existing_items[item_id]
                    for attr, value in item_data.items():
                        setattr(item, attr, value)
                    items_to_update.append(item)
                else:
                    item = QuotationItemDetails(QuotationDetailsId=detail, **item_data)
                    items_to_create.append(item)

        QuotationDetails.objects.bulk_create(details_to_create)
        QuotationDetails.objects.bulk_update(details_to_update, fields=[f.name for f in QuotationDetails._meta.fields if f.name != 'QuotationDetailsId'])
        QuotationItemDetails.objects.bulk_create(items_to_create)
        QuotationItemDetails.objects.bulk_update(items_to_update, fields=[f.name for f in QuotationItemDetails._meta.fields if f.name != 'QuoteItemId'])

        instance.calculate_total_value()
        return instance
