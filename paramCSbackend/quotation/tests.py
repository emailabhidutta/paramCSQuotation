from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import QuotationStatus, Quotation, QuotationDetails, QuotationItemDetails
from core.models import Role, CustomUser
from company.models import SalesOrganization

class QuotationTests(TestCase):
    def setUp(self):
        # Create test users and roles
        self.admin_role = Role.objects.create(RoleID='ADMN', RoleName='Admin')
        self.sales_manager_role = Role.objects.create(RoleID='SMGR', RoleName='Sales Manager')
        self.sales_user_role = Role.objects.create(RoleID='SUSR', RoleName='Sales User')

        self.admin_user = User.objects.create_user('admin', 'admin@test.com', 'adminpass')
        self.sales_manager = User.objects.create_user('salesmanager', 'sm@test.com', 'smpass')
        self.sales_user = User.objects.create_user('salesuser', 'su@test.com', 'supass')

        CustomUser.objects.create(user=self.admin_user, RoleID=self.admin_role)
        CustomUser.objects.create(user=self.sales_manager, RoleID=self.sales_manager_role)
        CustomUser.objects.create(user=self.sales_user, RoleID=self.sales_user_role)

        # Create test data
        self.status_draft = QuotationStatus.objects.create(QStatusID='D', QStatusName='Draft')
        self.status_approved = QuotationStatus.objects.create(QStatusID='A', QStatusName='Approved')
        self.status_rejected = QuotationStatus.objects.create(QStatusID='R', QStatusName='Rejected')
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
                'QuoteValidFrom': timezone.now().date(),
                'QuoteValidUntil': timezone.now().date() + timezone.timedelta(days=30),
                'TradingCurrency': 'USD',
                'items': [{
                    'MaterialNumber': 'M001',
                    'OrderQuantity': 10,
                    'PricePer': 100,
                    'OrderValue': 1000,
                    'UnitOfMeasure': 'EA'
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
        self.assertEqual(quotation.QStatusID, self.status_rejected)
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
            QuoteValidFrom=timezone.now().date(),
            QuoteValidUntil=timezone.now().date() + timezone.timedelta(days=30),
            TradingCurrency='USD'
        )
        QuotationItemDetails.objects.create(
            QuotationDetailsId=details,
            MaterialNumber='M001',
            OrderQuantity=10,
            PricePer=100,
            OrderValue=1000,
            UnitOfMeasure='EA'
        )
        quotation.calculate_total_value()
        self.assertEqual(quotation.total_value, Decimal('1000.00'))

    def test_quotation_validation(self):
        with self.assertRaises(ValidationError):
            Quotation.objects.create(
                QuoteId='Q0006',
                QuotationNo='QN0006',
                CustomerNumber='C006',
                LastRevision='01',
                QStatusID=self.status_draft,
                Date=timezone.now().date() + timezone.timedelta(days=1),  # Future date
                created_by=self.sales_user
            )

        with self.assertRaises(ValidationError):
            details = QuotationDetails.objects.create(
                QuoteId=Quotation.objects.create(
                    QuoteId='Q0007',
                    QuotationNo='QN0007',
                    CustomerNumber='C007',
                    LastRevision='01',
                    QStatusID=self.status_draft,
                    created_by=self.sales_user
                ),
                SalesOrganization=self.sales_org,
                SoldToCustomerNumber='C007',
                QuoteValidFrom=timezone.now().date() + timezone.timedelta(days=30),
                QuoteValidUntil=timezone.now().date(),  # End date before start date
                TradingCurrency='USD'
            )

        with self.assertRaises(ValidationError):
            QuotationItemDetails.objects.create(
                QuotationDetailsId=QuotationDetails.objects.create(
                    QuoteId=Quotation.objects.create(
                        QuoteId='Q0008',
                        QuotationNo='QN0008',
                        CustomerNumber='C008',
                        LastRevision='01',
                        QStatusID=self.status_draft,
                        created_by=self.sales_user
                    ),
                    SalesOrganization=self.sales_org,
                    SoldToCustomerNumber='C008',
                    QuoteValidFrom=timezone.now().date(),
                    QuoteValidUntil=timezone.now().date() + timezone.timedelta(days=30),
                    TradingCurrency='USD'
                ),
                MaterialNumber='M001',
                OrderQuantity=-1,  # Negative quantity
                PricePer=100,
                OrderValue=1000,
                UnitOfMeasure='EA'
            )

    def test_get_latest_revision(self):
        Quotation.objects.create(
            QuoteId='Q0009A',
            QuotationNo='QN0009',
            CustomerNumber='C009',
            LastRevision='01',
            QStatusID=self.status_draft,
            created_by=self.sales_user
        )
        latest = Quotation.objects.create(
            QuoteId='Q0009B',
            QuotationNo='QN0009',
            CustomerNumber='C009',
            LastRevision='02',
            QStatusID=self.status_draft,
            created_by=self.sales_user
        )
        self.assertEqual(Quotation.get_latest_revision('QN0009'), latest)