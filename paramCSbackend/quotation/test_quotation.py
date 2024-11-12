from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Quotation, QuotationStatus, QuotationDetails, QuotationItemDetails
from core.models import CustomUser, Role
from company.models import SalesOrganization
from decimal import Decimal

class QuotationTests(TestCase):
    def setUp(self):
        # Create test users and roles
        self.admin_role = Role.objects.create(RoleID='ADMIN', RoleName='Admin')
        self.sales_manager_role = Role.objects.create(RoleID='SALMGR', RoleName='Sales Manager')
        self.sales_user_role = Role.objects.create(RoleID='SALUSR', RoleName='Sales User')

        self.admin_user = User.objects.create_user('admin', 'admin@test.com', 'adminpass')
        self.sales_manager = User.objects.create_user('salesmanager', 'sm@test.com', 'smpass')
        self.sales_user = User.objects.create_user('salesuser', 'su@test.com', 'supass')

        CustomUser.objects.create(user=self.admin_user, RoleID=self.admin_role)
        CustomUser.objects.create(user=self.sales_manager, RoleID=self.sales_manager_role)
        CustomUser.objects.create(user=self.sales_user, RoleID=self.sales_user_role)

        # Create test data
        self.status_draft = QuotationStatus.objects.create(QStatusID='D', QStatusName='Draft')
        self.status_approved = QuotationStatus.objects.create(QStatusID='A', QStatusName='Approved')
        self.sales_org = SalesOrganization.objects.create(SalesOrganizationID='SO01', SalesOrganizationName='Test SO')

        self.client = APIClient()

    def test_create_quotation(self):
        self.client.force_authenticate(user=self.sales_user)
        data = {
            'QuoteId': 'Q0001',
            'QuotationNo': 'QN0001',
            'CustomerNumber': 'C001',
            'LastRevision': '01',
            'QStatusID': self.status_draft.QStatusID,
            'details': [{
                'SalesOrganization': self.sales_org.SalesOrganizationID,
                'SoldToCustomerNumber': 'C001',
                'QuoteValidFrom': '2023-01-01',
                'QuoteValidUntil': '2023-12-31',
                'items': [{
                    'MaterialNumber': 'M001',
                    'OrderQuantity': 10,
                    'PricePer': 100,
                    'OrderValue': 1000
                }]
            }]
        }
        response = self.client.post('/api/quotation/quotations/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quotation.objects.count(), 1)
        self.assertEqual(QuotationDetails.objects.count(), 1)
        self.assertEqual(QuotationItemDetails.objects.count(), 1)

    def test_approve_quotation(self):
        quotation = Quotation.objects.create(
            QuoteId='Q0002',
            QuotationNo='QN0002',
            CustomerNumber='C002',
            LastRevision='01',
            QStatusID=self.status_draft,
            created_by=self.sales_user
        )
        self.client.force_authenticate(user=self.sales_manager)
        response = self.client.post(f'/api/quotation/quotations/{quotation.QuoteId}/approve/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quotation.refresh_from_db()
        self.assertEqual(quotation.QStatusID, self.status_approved)

    def test_reject_quotation(self):
        quotation = Quotation.objects.create(
            QuoteId='Q0003',
            QuotationNo='QN0003',
            CustomerNumber='C003',
            LastRevision='01',
            QStatusID=self.status_draft,
            created_by=self.sales_user
        )
        self.client.force_authenticate(user=self.sales_manager)
        response = self.client.post(f'/api/quotation/quotations/{quotation.QuoteId}/reject/', {'reason': 'Test rejection'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quotation.refresh_from_db()
        self.assertEqual(quotation.QStatusID.QStatusName, 'Rejected')
        self.assertEqual(quotation.rejection_reason, 'Test rejection')

    def test_revise_quotation(self):
        quotation = Quotation.objects.create(
            QuoteId='Q0004',
            QuotationNo='QN0004',
            CustomerNumber='C004',
            LastRevision='01',
            QStatusID=self.status_approved,
            created_by=self.sales_user
        )
        self.client.force_authenticate(user=self.sales_user)
        response = self.client.post(f'/api/quotation/quotations/{quotation.QuoteId}/revise/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quotation.refresh_from_db()
        self.assertEqual(quotation.LastRevision, '02')
        self.assertEqual(quotation.QStatusID, self.status_draft)

    def test_calculate_total_value(self):
        quotation = Quotation.objects.create(
            QuoteId='Q0005',
            QuotationNo='QN0005',
            CustomerNumber='C005',
            LastRevision='01',
            QStatusID=self.status_draft,
            created_by=self.sales_user
        )
        details = QuotationDetails.objects.create(
            QuoteId=quotation,
            SalesOrganization=self.sales_org,
            SoldToCustomerNumber='C005',
            QuoteValidFrom='2023-01-01',
            QuoteValidUntil='2023-12-31'
        )
        QuotationItemDetails.objects.create(
            QuotationDetailsId=details,
            MaterialNumber='M001',
            OrderQuantity=10,
            PricePer=100,
            OrderValue=1000
        )
        self.client.force_authenticate(user=self.sales_user)
        response = self.client.get(f'/api/quotation/quotations/{quotation.QuoteId}/calculate_total/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['total_value']), Decimal('1000.00'))

    def test_get_latest_revision(self):
        Quotation.objects.create(
            QuoteId='Q0006A',
            QuotationNo='QN0006',
            CustomerNumber='C006',
            LastRevision='01',
            QStatusID=self.status_draft,
            created_by=self.sales_user
        )
        latest = Quotation.objects.create(
            QuoteId='Q0006B',
            QuotationNo='QN0006',
            CustomerNumber='C006',
            LastRevision='02',
            QStatusID=self.status_draft,
            created_by=self.sales_user
        )
        self.client.force_authenticate(user=self.sales_user)
        response = self.client.get('/api/quotation/quotations/get_latest_revision/?quotation_no=QN0006')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['QuoteId'], latest.QuoteId)

    def test_quotation_permissions(self):
        quotation = Quotation.objects.create(
            QuoteId='Q0007',
            QuotationNo='QN0007',
            CustomerNumber='C007',
            LastRevision='01',
            QStatusID=self.status_draft,
            created_by=self.sales_user
        )
        
        # Test that sales user can't approve
        self.client.force_authenticate(user=self.sales_user)
        response = self.client.post(f'/api/quotation/quotations/{quotation.QuoteId}/approve/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test that sales manager can approve
        self.client.force_authenticate(user=self.sales_manager)
        response = self.client.post(f'/api/quotation/quotations/{quotation.QuoteId}/approve/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_quotation_validation(self):
        self.client.force_authenticate(user=self.sales_user)
        data = {
            'QuoteId': 'Q0008',
            'QuotationNo': 'QN0008',
            'CustomerNumber': 'C008',
            'LastRevision': '01',
            'QStatusID': self.status_draft.QStatusID,
            'details': [{
                'SalesOrganization': self.sales_org.SalesOrganizationID,
                'SoldToCustomerNumber': 'C008',
                'QuoteValidFrom': '2023-12-31',  # Invalid: end date before start date
                'QuoteValidUntil': '2023-01-01',
                'items': [{
                    'MaterialNumber': 'M001',
                    'OrderQuantity': -1,  # Invalid: negative quantity
                    'PricePer': 100,
                    'OrderValue': 1000
                }]
            }]
        }
        response = self.client.post('/api/quotation/quotations/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
