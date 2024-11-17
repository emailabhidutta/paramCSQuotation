from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from unittest.mock import patch, MagicMock

from quotation.models import Quotation, QuotationStatus, QuotationDetails, QuotationItemDetails
from master_data.models import CustomerMaster, MaterialMaster
from quotation.services import (
    create_quotation, update_quotation, submit_quotation, approve_quotation,
    reject_quotation, cancel_quotation, revise_quotation, delete_quotation_item,
    get_customer_details, get_item_rates, get_material_details
)

User = get_user_model()

class QuotationServicesTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create test QuotationStatus instances
        self.draft_status = QuotationStatus.objects.create(QStatusID='D', QStatusName='Draft')
        self.submitted_status = QuotationStatus.objects.create(QStatusID='S', QStatusName='Submitted')
        self.approved_status = QuotationStatus.objects.create(QStatusID='A', QStatusName='Approved')
        self.rejected_status = QuotationStatus.objects.create(QStatusID='R', QStatusName='Rejected')
        self.cancelled_status = QuotationStatus.objects.create(QStatusID='C', QStatusName='Cancelled')

        # Create test CustomerMaster
        self.customer = CustomerMaster.objects.create(
            CustomerNumber='CUST001',
            CustomerName1='Test Customer',
            CustomerName2='Test Customer 2',
            City='Test City',
            Country='Test Country'
        )

        # Create test MaterialMaster
        self.material = MaterialMaster.objects.create(
            MaterialNumber='MAT001',
            MaterialDescription='Test Material',
            UnitOfMeasure='EA'
        )

    def test_create_quotation(self):
        data = {
            'CustomerNumber': 'CUST001',
            'CustomerInquiryNo': 'INQ001',
            'QuoteValidFrom': timezone.now().date(),
            'QuoteValidUntil': timezone.now().date() + timezone.timedelta(days=30),
            'CustomerEmail': 'test@example.com',
            'Remarks': 'Test remarks',
            'details': [
                {
                    'SalesOrganization': 'ORG001',
                    'TradingCurrency': 'USD',
                    'items': [
                        {
                            'MaterialNumber': 'MAT001',
                            'PricePer': '10.00',
                            'Per': '1',
                            'UnitOfMeasure': 'EA',
                            'OrderQuantity': '5',
                            'OrderValue': '50.00'
                        }
                    ]
                }
            ]
        }

        quotation = create_quotation(data, self.user)

        self.assertIsNotNone(quotation)
        self.assertEqual(quotation.CustomerNumber, 'CUST001')
        self.assertEqual(quotation.QStatusID, self.draft_status)
        self.assertEqual(quotation.details.count(), 1)
        self.assertEqual(quotation.details.first().items.count(), 1)

    def test_update_quotation(self):
        quotation = create_quotation({
            'CustomerNumber': 'CUST001',
            'details': [{'SalesOrganization': 'ORG001', 'TradingCurrency': 'USD'}]
        }, self.user)

        update_data = {
            'CustomerInquiryNo': 'INQ002',
            'details': [
                {
                    'QuotationDetailsId': quotation.details.first().QuotationDetailsId,
                    'SalesOrganization': 'ORG002',
                    'TradingCurrency': 'EUR',
                    'items': [
                        {
                            'MaterialNumber': 'MAT001',
                            'PricePer': '15.00',
                            'Per': '1',
                            'UnitOfMeasure': 'EA',
                            'OrderQuantity': '3',
                            'OrderValue': '45.00'
                        }
                    ]
                }
            ]
        }

        updated_quotation = update_quotation(quotation, update_data, self.user)

        self.assertEqual(updated_quotation.CustomerInquiryNo, 'INQ002')
        self.assertEqual(updated_quotation.details.first().SalesOrganization, 'ORG002')
        self.assertEqual(updated_quotation.details.first().items.count(), 1)

    def test_submit_quotation(self):
        quotation = create_quotation({'CustomerNumber': 'CUST001'}, self.user)
        submitted_quotation = submit_quotation(quotation, self.user)

        self.assertEqual(submitted_quotation.QStatusID, self.submitted_status)

    def test_approve_quotation(self):
        quotation = create_quotation({'CustomerNumber': 'CUST001'}, self.user)
        quotation.QStatusID = self.submitted_status
        quotation.save()

        approved_quotation = approve_quotation(quotation, self.user)

        self.assertEqual(approved_quotation.QStatusID, self.approved_status)

    def test_reject_quotation(self):
        quotation = create_quotation({'CustomerNumber': 'CUST001'}, self.user)
        quotation.QStatusID = self.submitted_status
        quotation.save()

        rejected_quotation = reject_quotation(quotation, self.user, 'Test rejection reason')

        self.assertEqual(rejected_quotation.QStatusID, self.rejected_status)
        self.assertEqual(rejected_quotation.rejection_reason, 'Test rejection reason')

    def test_cancel_quotation(self):
        quotation = create_quotation({'CustomerNumber': 'CUST001'}, self.user)
        cancelled_quotation = cancel_quotation(quotation, self.user)

        self.assertEqual(cancelled_quotation.QStatusID, self.cancelled_status)

    def test_revise_quotation(self):
        quotation = create_quotation({'CustomerNumber': 'CUST001'}, self.user)
        revised_quotation = revise_quotation(quotation, self.user)

        self.assertEqual(revised_quotation.LastRevision, '02')
        self.assertEqual(revised_quotation.QStatusID, self.draft_status)

    def test_delete_quotation_item(self):
        quotation = create_quotation({
            'CustomerNumber': 'CUST001',
            'details': [{
                'SalesOrganization': 'ORG001',
                'TradingCurrency': 'USD',
                'items': [{
                    'MaterialNumber': 'MAT001',
                    'PricePer': '10.00',
                    'Per': '1',
                    'UnitOfMeasure': 'EA',
                    'OrderQuantity': '5',
                    'OrderValue': '50.00'
                }]
            }]
        }, self.user)

        item = quotation.details.first().items.first()
        updated_quotation = delete_quotation_item(quotation, item.QuoteItemId)

        self.assertTrue(updated_quotation.details.first().items.first().IsDeleted)

    def test_get_customer_details(self):
        result = get_customer_details('CUST001')

        self.assertIsNotNone(result)
        self.assertEqual(result['CustomerNumber'], 'CUST001')
        self.assertEqual(result['CustomerName1'], 'Test Customer')

    @patch('quotation.services.connection')
    def test_get_item_rates(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (Decimal('10.00'), 'USD', Decimal('1'), 'EA', timezone.now().date(), timezone.now().date() + timezone.timedelta(days=30))

        result = get_item_rates('CUST001', 'MAT001', 'ORG001', 'DC001')

        self.assertIsNotNone(result)
        self.assertEqual(result['Price'], Decimal('10.00'))
        self.assertEqual(result['Currency'], 'USD')

    def test_get_material_details(self):
        result = get_material_details('MAT001')

        self.assertIsNotNone(result)
        self.assertEqual(result['MaterialNumber'], 'MAT001')
        self.assertEqual(result['MaterialDescription'], 'Test Material')
