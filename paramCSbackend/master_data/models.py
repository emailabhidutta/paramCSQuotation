from django.db import models

class CustomerMaster(models.Model):
    Customer = models.CharField(max_length=10, primary_key=True)
    SalesOrganization = models.CharField(max_length=4)
    AccountGroup = models.CharField(max_length=4, null=True, blank=True)
    Name = models.CharField(max_length=35, null=True, blank=True)
    Name2 = models.CharField(max_length=35, null=True, blank=True)
    SearchTerm = models.CharField(max_length=20, null=True, blank=True)
    Street = models.CharField(max_length=60, null=True, blank=True)
    City = models.CharField(max_length=40, null=True, blank=True)
    Country = models.CharField(max_length=3, null=True, blank=True)
    CustomerClassification = models.CharField(max_length=2, null=True, blank=True)
    IndustryCode1 = models.CharField(max_length=4, null=True, blank=True)
    SalesGroup = models.CharField(max_length=3, null=True, blank=True)
    CustPriceProcedure = models.CharField(max_length=1, null=True, blank=True)
    TermsOfPayment = models.CharField(max_length=4, null=True, blank=True)
    Incoterms = models.CharField(max_length=3, null=True, blank=True)
    IncotermsPart2 = models.CharField(max_length=28, null=True, blank=True)
    Currency = models.CharField(max_length=5, null=True, blank=True)
    OrderBlockForSalesArea = models.CharField(max_length=2, null=True, blank=True)
    CentralDelBlock = models.CharField(max_length=2, null=True, blank=True)
    Status = models.CharField(max_length=1, null=True, blank=True)
    CreatedOn = models.DateField(null=True, blank=True)
    CreatedSource = models.CharField(max_length=50, null=True, blank=True)
    LastUpdate = models.DateField(null=True, blank=True)
    UpdatedSource = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.Customer} - {self.Name}"

class MaterialMaster(models.Model):
    Material = models.CharField(max_length=18, primary_key=True)
    Plant = models.CharField(max_length=4, null=True, blank=True)
    MaterialDescription = models.CharField(max_length=255, null=True, blank=True)
    XPlantMatlStatus = models.CharField(max_length=50, null=True, blank=True)
    DrawingNo = models.CharField(max_length=35, null=True, blank=True)
    Description = models.CharField(max_length=255, null=True, blank=True)
    DescriptionText = models.TextField(null=True, blank=True)
    BasicMaterial = models.CharField(max_length=50, null=True, blank=True)
    BasicMaterialDesc = models.CharField(max_length=255, null=True, blank=True)
    MachineType = models.CharField(max_length=50, null=True, blank=True)
    ProductGroup = models.CharField(max_length=50, null=True, blank=True)
    ProductType = models.CharField(max_length=50, null=True, blank=True)
    Lifecycle = models.CharField(max_length=50, null=True, blank=True)
    OldMaterialNumber = models.CharField(max_length=18, null=True, blank=True)
    ProductHierarchy = models.CharField(max_length=50, null=True, blank=True)
    BaseUnitOfMeasure = models.CharField(max_length=3, null=True, blank=True)
    Status = models.CharField(max_length=1, null=True, blank=True)
    CreatedOn = models.DateField(null=True, blank=True)
    CreatedSource = models.CharField(max_length=50, null=True, blank=True)
    LastUpdate = models.DateField(null=True, blank=True)
    UpdatedSource = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.Material} - {self.MaterialDescription}"

class EmployeeMaster(models.Model):
    EmployeeNo = models.CharField(max_length=8, primary_key=True)
    LastName = models.CharField(max_length=50, null=True, blank=True)
    FirstName = models.CharField(max_length=50, null=True, blank=True)
    CoCd = models.CharField(max_length=4, null=True, blank=True)
    Status = models.CharField(max_length=1, null=True, blank=True)
    OntrackID = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.EmployeeNo} - {self.LastName}, {self.FirstName}"

class EbauPriceList(models.Model):
    ConditionType = models.CharField(max_length=4)
    SalesOrganization = models.CharField(max_length=4)
    DistributionChannel = models.CharField(max_length=2)
    SalesGroup = models.CharField(max_length=3)
    Material = models.CharField(max_length=18)
    Customer = models.CharField(max_length=10)
    ValidTo = models.DateField(null=True, blank=True)
    ValidFrom = models.DateField()
    Rate = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    ConditionCurrency = models.CharField(max_length=5, null=True, blank=True)
    PricingUnit = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    UnitOfMeasure = models.CharField(max_length=3, null=True, blank=True)
    ScaleBasis = models.CharField(max_length=50, null=True, blank=True)
    DeletionIndicator = models.CharField(max_length=1, null=True, blank=True)
    Status = models.CharField(max_length=1, null=True, blank=True)
    CreatedOn = models.DateField(null=True, blank=True)
    CreatedSource = models.CharField(max_length=50, null=True, blank=True)
    LastUpdate = models.DateField(null=True, blank=True)
    UpdatedSource = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ('ConditionType', 'SalesOrganization', 'DistributionChannel', 'SalesGroup', 'Material', 'Customer', 'ValidFrom')

    def __str__(self):
        return f"{self.Material} - {self.Customer} - {self.ValidFrom}"
