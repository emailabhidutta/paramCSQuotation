from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from company.models import SalesOrganization

class QuotationStatus(models.Model):
    QStatusID = models.CharField(max_length=1, primary_key=True)
    QStatusName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.QStatusName

    class Meta:
        verbose_name = "Quotation Status"
        verbose_name_plural = "Quotation Statuses"

class Quotation(models.Model):
    QuoteId = models.CharField(max_length=8, primary_key=True)
    QuotationNo = models.CharField(max_length=8, unique=True)
    CustomerNumber = models.CharField(max_length=10)
    LastRevision = models.CharField(max_length=2)
    CustomerInquiryNo = models.CharField(max_length=35, null=True, blank=True)
    Date = models.DateField(auto_now_add=True)
    CreationDate = models.DateField(auto_now_add=True)
    QStatusID = models.ForeignKey(QuotationStatus, on_delete=models.PROTECT, related_name='quotations')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_quotations')
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='modified_quotations')
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    rejection_reason = models.TextField(null=True, blank=True)
    QuoteValidFrom = models.DateField(null=True, blank=True)
    QuoteValidUntil = models.DateField(null=True, blank=True)
    CustomerEmail = models.EmailField(max_length=254, null=True, blank=True)
    Version = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.QuotationNo} - Rev {self.LastRevision}"

    class Meta:
        verbose_name = "Quotation"
        verbose_name_plural = "Quotations"
        ordering = ['-Date', 'QuotationNo']

    def clean(self):
        if self.Date > timezone.now().date():
            raise ValidationError("Quotation date cannot be in the future.")
        if self.QuoteValidFrom and self.QuoteValidUntil and self.QuoteValidFrom > self.QuoteValidUntil:
            raise ValidationError("Valid from date must be before valid until date.")

    def calculate_total_value(self):
        self.total_value = sum(item.OrderValue for detail in self.quotationdetails_set.all() for item in detail.quotationitemdetails_set.all())
        self.save()

    def approve(self, approver):
        if self.QStatusID.QStatusName != 'Approved':
            self.QStatusID = QuotationStatus.objects.get(QStatusName='Approved')
            self.last_modified_by = approver
            self.save()

    def reject(self, rejector, reason):
        if self.QStatusID.QStatusName != 'Rejected':
            self.QStatusID = QuotationStatus.objects.get(QStatusName='Rejected')
            self.last_modified_by = rejector
            self.rejection_reason = reason
            self.save()

    def revise(self, reviser):
        new_revision = int(self.LastRevision) + 1
        self.LastRevision = f"{new_revision:02d}"
        self.QStatusID = QuotationStatus.objects.get(QStatusName='Draft')
        self.last_modified_by = reviser
        self.save()

    @property
    def is_valid(self):
        today = timezone.now().date()
        return (self.QuoteValidFrom is None or self.QuoteValidFrom <= today) and \
               (self.QuoteValidUntil is None or today <= self.QuoteValidUntil)

    @classmethod
    def get_latest_revision(cls, quotation_no):
        return cls.objects.filter(QuotationNo=quotation_no).order_by('-LastRevision').first()

    def create_new_version(self):
        new_version = self.Version + 1
        new_quote = Quotation.objects.create(
            QuotationNo=self.QuotationNo,
            CustomerNumber=self.CustomerNumber,
            LastRevision='01',
            Version=new_version,
            QStatusID=QuotationStatus.objects.get(QStatusName='Draft'),
            created_by=self.last_modified_by,
            CustomerEmail=self.CustomerEmail,
            QuoteValidFrom=self.QuoteValidFrom,
            QuoteValidUntil=self.QuoteValidUntil,
        )
        return new_quote

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class QuotationDetails(models.Model):
    QuotationDetailsId = models.AutoField(primary_key=True)
    QuoteId = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='details')
    QuoteRevisionNo = models.CharField(max_length=2)
    QuoteRevisionDate = models.DateField(null=True, blank=True)
    SalesOrganization = models.ForeignKey(SalesOrganization, on_delete=models.PROTECT)
    CustomerInquiryNo = models.CharField(max_length=35, null=True, blank=True)
    SoldToCustomerNumber = models.CharField(max_length=10)
    ShipToCustomerNumber = models.CharField(max_length=10, null=True, blank=True)
    SalesGroup = models.CharField(max_length=3, null=True, blank=True)
    Customer = models.CharField(max_length=35, null=True, blank=True)
    CustomerName = models.CharField(max_length=35, null=True, blank=True)
    CustomerName2 = models.CharField(max_length=35, null=True, blank=True)
    IndustryCode1 = models.CharField(max_length=10, null=True, blank=True)
    CustPriceProcedure = models.CharField(max_length=20, null=True, blank=True)
    MaterialDisplay = models.CharField(max_length=40, null=True, blank=True)
    TermOfPayment = models.CharField(max_length=4, null=True, blank=True)
    Incoterms = models.CharField(max_length=3, null=True, blank=True)
    IncotermsPart2 = models.CharField(max_length=28, null=True, blank=True)
    TradingCurrency = models.CharField(max_length=5)
    SalesEmployeeNo = models.CharField(max_length=8, null=True, blank=True)
    DeliveryDate = models.DateField(null=True, blank=True)
    CustomerPONumber = models.CharField(max_length=35, null=True, blank=True)
    ApprovalStatus = models.CharField(max_length=1)
    Version = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.QuoteId.QuotationNo} - {self.QuoteRevisionNo}"

    class Meta:
        verbose_name = "Quotation Detail"
        verbose_name_plural = "Quotation Details"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class QuotationItemDetails(models.Model):
    QuoteItemId = models.AutoField(primary_key=True)
    QuotationDetailsId = models.ForeignKey(QuotationDetails, on_delete=models.CASCADE, related_name='items')
    MaterialNumber = models.CharField(max_length=18)
    CustomerMatNumber = models.CharField(max_length=18, null=True, blank=True)
    FullMaterialDescription = models.CharField(max_length=255, null=True, blank=True)
    MaterialDescription = models.CharField(max_length=255, null=True, blank=True)
    BasicMaterialText = models.CharField(max_length=255, null=True, blank=True)
    DrawingNo = models.CharField(max_length=35, null=True, blank=True)
    PricePer = models.DecimalField(max_digits=15, decimal_places=2)
    Per = models.DecimalField(max_digits=5, decimal_places=2)
    UnitOfMeasure = models.CharField(max_length=3)
    DiscountValue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    SurchargeValue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    OrderQuantity = models.DecimalField(max_digits=13, decimal_places=3)
    OrderValue = models.DecimalField(max_digits=15, decimal_places=2)
    ItemText = models.CharField(max_length=255, null=True, blank=True)
    Usage = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return f"{self.QuotationDetailsId.QuoteId.QuotationNo} - {self.MaterialNumber}"

    class Meta:
        verbose_name = "Quotation Item Detail"
        verbose_name_plural = "Quotation Item Details"

    def clean(self):
        if self.OrderQuantity <= 0:
            raise ValidationError("Order quantity must be greater than zero.")
        if self.PricePer <= 0:
            raise ValidationError("Price must be greater than zero.")
        if self.OrderValue != self.OrderQuantity * self.PricePer:
            raise ValidationError("Order value must equal quantity times price.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
