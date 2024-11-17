from django.db import connection, transaction
from django.utils import timezone
from django.db.models import Q
from .models import Quotation, QuotationStatus, QuotationDetails, QuotationItemDetails
from master_data.models import CustomerMaster, MaterialMaster
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

@transaction.atomic
def create_quotation(data, user):
    quotation = Quotation.objects.create(
        CustomerNumber=data['CustomerNumber'],
        CustomerInquiryNo=data.get('CustomerInquiryNo'),
        Date=data.get('Date', timezone.now().date()),
        QuoteValidFrom=data.get('QuoteValidFrom'),
        QuoteValidUntil=data.get('QuoteValidUntil'),
        CustomerEmail=data.get('CustomerEmail'),
        Remarks=data.get('Remarks'),
        created_by=user,
        last_modified_by=user,
        QStatusID=QuotationStatus.objects.get(QStatusName='Draft'),
        LastRevision='01',
        Version=1
    )

    details_data = data.get('details', [])
    for detail_data in details_data:
        detail = QuotationDetails.objects.create(
            QuoteId=quotation,
            SalesOrganization_id=detail_data['SalesOrganization'],
            QuoteRevisionNo='01',
            QuoteRevisionDate=timezone.now().date(),
            TradingCurrency=detail_data['TradingCurrency'],
            SoldToCustomerNumber=detail_data.get('SoldToCustomerNumber'),
            ShipToCustomerNumber=detail_data.get('ShipToCustomerNumber'),
            SalesGroup=detail_data.get('SalesGroup'),
            Customer=detail_data.get('Customer'),
            CustomerName=detail_data.get('CustomerName'),
            CustomerName2=detail_data.get('CustomerName2'),
            IndustryCode1=detail_data.get('IndustryCode1'),
            CustPriceProcedure=detail_data.get('CustPriceProcedure'),
            MaterialDisplay=detail_data.get('MaterialDisplay'),
            TermOfPayment=detail_data.get('TermOfPayment'),
            Incoterms=detail_data.get('Incoterms'),
            IncotermsPart2=detail_data.get('IncotermsPart2'),
            SalesEmployeeNo=detail_data.get('SalesEmployeeNo'),
            DeliveryDate=detail_data.get('DeliveryDate'),
            CustomerPONumber=detail_data.get('CustomerPONumber'),
            ApprovalStatus='P',  # Pending
            Version=1,
            PaymentTerms=detail_data.get('PaymentTerms'),
            DeliveryMethod=detail_data.get('DeliveryMethod')
        )

        items_data = detail_data.get('items', [])
        for item_data in items_data:
            QuotationItemDetails.objects.create(
                QuotationDetailsId=detail,
                MaterialNumber=item_data['MaterialNumber'],
                CustomerMatNumber=item_data.get('CustomerMatNumber'),
                FullMaterialDescription=item_data.get('FullMaterialDescription'),
                MaterialDescription=item_data.get('MaterialDescription'),
                BasicMaterialText=item_data.get('BasicMaterialText'),
                DrawingNo=item_data.get('DrawingNo'),
                PricePer=item_data['PricePer'],
                Per=item_data['Per'],
                UnitOfMeasure=item_data['UnitOfMeasure'],
                DiscountValue=item_data.get('DiscountValue'),
                SurchargeValue=item_data.get('SurchargeValue'),
                OrderQuantity=item_data['OrderQuantity'],
                OrderValue=item_data['OrderValue'],
                ItemText=item_data.get('ItemText'),
                Usage=item_data.get('Usage')
            )

    quotation.calculate_total_value()
    return quotation

@transaction.atomic
def update_quotation(quotation, data, user):
    for field, value in data.items():
        if field not in ['details', 'items']:
            setattr(quotation, field, value)
    
    quotation.last_modified_by = user
    quotation.save()

    if 'details' in data:
        for detail_data in data['details']:
            detail, created = QuotationDetails.objects.update_or_create(
                QuoteId=quotation,
                QuotationDetailsId=detail_data.get('QuotationDetailsId'),
                defaults={
                    'SalesOrganization_id': detail_data['SalesOrganization'],
                    'TradingCurrency': detail_data['TradingCurrency'],
                    'SoldToCustomerNumber': detail_data.get('SoldToCustomerNumber'),
                    'ShipToCustomerNumber': detail_data.get('ShipToCustomerNumber'),
                    'SalesGroup': detail_data.get('SalesGroup'),
                    'Customer': detail_data.get('Customer'),
                    'CustomerName': detail_data.get('CustomerName'),
                    'CustomerName2': detail_data.get('CustomerName2'),
                    'IndustryCode1': detail_data.get('IndustryCode1'),
                    'CustPriceProcedure': detail_data.get('CustPriceProcedure'),
                    'MaterialDisplay': detail_data.get('MaterialDisplay'),
                    'TermOfPayment': detail_data.get('TermOfPayment'),
                    'Incoterms': detail_data.get('Incoterms'),
                    'IncotermsPart2': detail_data.get('IncotermsPart2'),
                    'SalesEmployeeNo': detail_data.get('SalesEmployeeNo'),
                    'DeliveryDate': detail_data.get('DeliveryDate'),
                    'CustomerPONumber': detail_data.get('CustomerPONumber'),
                    'PaymentTerms': detail_data.get('PaymentTerms'),
                    'DeliveryMethod': detail_data.get('DeliveryMethod')
                }
            )

            if 'items' in detail_data:
                for item_data in detail_data['items']:
                    QuotationItemDetails.objects.update_or_create(
                        QuotationDetailsId=detail,
                        QuoteItemId=item_data.get('QuoteItemId'),
                        defaults={
                            'MaterialNumber': item_data['MaterialNumber'],
                            'CustomerMatNumber': item_data.get('CustomerMatNumber'),
                            'FullMaterialDescription': item_data.get('FullMaterialDescription'),
                            'MaterialDescription': item_data.get('MaterialDescription'),
                            'BasicMaterialText': item_data.get('BasicMaterialText'),
                            'DrawingNo': item_data.get('DrawingNo'),
                            'PricePer': item_data['PricePer'],
                            'Per': item_data['Per'],
                            'UnitOfMeasure': item_data['UnitOfMeasure'],
                            'DiscountValue': item_data.get('DiscountValue'),
                            'SurchargeValue': item_data.get('SurchargeValue'),
                            'OrderQuantity': item_data['OrderQuantity'],
                            'OrderValue': item_data['OrderValue'],
                            'ItemText': item_data.get('ItemText'),
                            'Usage': item_data.get('Usage')
                        }
                    )

    quotation.calculate_total_value()
    return quotation

def submit_quotation(quotation, user):
    if quotation.QStatusID.QStatusName == 'Draft':
        quotation.QStatusID = QuotationStatus.objects.get(QStatusName='Submitted')
        quotation.last_modified_by = user
        quotation.save()
    return quotation

def approve_quotation(quotation, user):
    if quotation.QStatusID.QStatusName == 'Submitted':
        quotation.QStatusID = QuotationStatus.objects.get(QStatusName='Approved')
        quotation.last_modified_by = user
        quotation.save()
    return quotation

def reject_quotation(quotation, user, reason):
    if quotation.QStatusID.QStatusName == 'Submitted':
        quotation.QStatusID = QuotationStatus.objects.get(QStatusName='Rejected')
        quotation.last_modified_by = user
        quotation.rejection_reason = reason
        quotation.save()
    return quotation

def cancel_quotation(quotation, user):
    if quotation.QStatusID.QStatusName in ['Draft', 'Submitted']:
        quotation.QStatusID = QuotationStatus.objects.get(QStatusName='Cancelled')
        quotation.last_modified_by = user
        quotation.save()
    return quotation

def revise_quotation(quotation, user):
    new_revision = int(quotation.LastRevision) + 1
    quotation.LastRevision = f"{new_revision:02d}"
    quotation.QStatusID = QuotationStatus.objects.get(QStatusName='Draft')
    quotation.last_modified_by = user
    quotation.save()
    
    for detail in quotation.details.all():
        detail.QuoteRevisionNo = quotation.LastRevision
        detail.QuoteRevisionDate = timezone.now().date()
        detail.save()
    
    return quotation

def delete_quotation_item(quotation, item_id):
    try:
        item = QuotationItemDetails.objects.get(QuoteItemId=item_id, QuotationDetailsId__QuoteId=quotation)
        item.IsDeleted = True
        item.save()
        quotation.calculate_total_value()
        return quotation
    except QuotationItemDetails.DoesNotExist:
        raise ValueError(f"Item with id {item_id} not found in this quotation.")

def get_customer_details(search_term):
    """
    Fetch customer details based on CustomerNumber, CustomerName1, or CustomerName2.
    """
    try:
        customer = CustomerMaster.objects.filter(
            Q(CustomerNumber__iexact=search_term) |
            Q(CustomerName1__icontains=search_term) |
            Q(CustomerName2__icontains=search_term)
        ).first()

        if customer:
            return {
                'CustomerNumber': customer.CustomerNumber,
                'CustomerName1': customer.CustomerName1,
                'CustomerName2': customer.CustomerName2,
                'SearchTerm': customer.SearchTerm,
                'HouseStreetName': customer.HouseStreetName,
                'City': customer.City,
                'Country': customer.Country,
                'CustomerClass': customer.CustomerClass,
                'IndCode1': customer.IndCode1,
                'KeyAccount': customer.KeyAccount,
                'SalesGroup': customer.SalesGroup,
                'CustPriceProc': customer.CustPriceProc,
                'TermOfPayment': customer.TermOfPayment,
                'Incoterms': customer.Incoterms,
                'IncotermsPort': customer.IncotermsPort,
                'TradingCurrency': customer.TradingCurrency,
                'CustomerBlocked': customer.CustomerBlocked,
                'CustomerDeleted': customer.CustomerDeleted,
            }
        else:
            return None
    except Exception as e:
        logger.error(f"Error fetching customer details: {str(e)}")
        return None

def get_item_rates(customer_number, material_number, sales_org, distribution_channel):
    """
    Fetch item rates based on customer, material, sales organization, and distribution channel.
    """
    try:
        with connection.cursor() as cursor:
            # First, try to get a customer-specific price
            cursor.execute("""
                SELECT Price, Currency, Per, UoM, ValidityStartDate, ValidityEndDate
                FROM SalesPriceList
                WHERE ConditionType = 'ZP00'
                AND SalesOrg = %s
                AND DistributionChannel = %s
                AND Identifier = %s
                AND MaterialNumber = %s
                AND ValidityStartDate <= GETDATE()
                AND ValidityEndDate >= GETDATE()
                AND DeletionIndicator = 0
            """, [sales_org, distribution_channel, customer_number, material_number])
            
            row = cursor.fetchone()
            
            if not row:
                # If no customer-specific price found, try to get a general price
                cursor.execute("""
                    SELECT Price, Currency, Per, UoM, ValidityStartDate, ValidityEndDate
                    FROM SalesPriceList
                    WHERE ConditionType = 'PR00'
                    AND SalesOrg = %s
                    AND DistributionChannel = %s
                    AND MaterialNumber = %s
                    AND ValidityStartDate <= GETDATE()
                    AND ValidityEndDate >= GETDATE()
                    AND DeletionIndicator = 0
                """, [sales_org, distribution_channel, material_number])
                
                row = cursor.fetchone()

            if row:
                return {
                    'Price': row[0],
                    'Currency': row[1],
                    'Per': row[2],
                    'UoM': row[3],
                    'ValidityStartDate': row[4],
                    'ValidityEndDate': row[5],
                }
            else:
                return None
    except Exception as e:
        logger.error(f"Error fetching item rates: {str(e)}")
        return None

def get_material_details(material_number):
    """
    Fetch material details based on MaterialNumber.
    """
    try:
        material = MaterialMaster.objects.filter(MaterialNumber=material_number).first()

        if material:
            return {
                'MaterialNumber': material.MaterialNumber,
                'MaterialDescription': material.MaterialDescription,
                'Plant': material.Plant,
                'CrossPlantStatus': material.CrossPlantStatus,
                'DrawingNumber': material.DrawingNumber,
                'FourDigitDescription': material.FourDigitDescription,
                'BasicMaterial': material.BasicMaterial,
                'BasicMatDescription': material.BasicMatDescription,
                'MachineType': material.MachineType,
                'ProductGroup': material.ProductGroup,
                'ProductType': material.ProductType,
                'LifeCycleFlag': material.LifeCycleFlag,
                'PlantOldMaterialNumber': material.PlantOldMaterialNumber,
                'ProductHierarchy': material.ProductHierarchy,
                'UnitOfMeasure': material.UnitOfMeasure,
            }
        else:
            return None
    except Exception as e:
        logger.error(f"Error fetching material details: {str(e)}")
        return None
