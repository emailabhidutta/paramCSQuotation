from django.db import models

class CustomerMaster(models.Model):
    CustomerNumber = models.CharField(max_length=10, primary_key=True)
    SalesOrg = models.CharField(max_length=4)
    AccountGroup = models.CharField(max_length=4)
    CustomerName1 = models.CharField(max_length=35)
    CustomerName2 = models.CharField(max_length=35, blank=True, null=True)
    SearchTerm = models.CharField(max_length=20)
    HouseStreetName = models.CharField(max_length=60)
    City = models.CharField(max_length=35)
    Country = models.CharField(max_length=3)
    CustomerClass = models.CharField(max_length=2)
    IndCode1 = models.CharField(max_length=4)
    KeyAccount = models.BooleanField(default=False)
    SalesGroup = models.CharField(max_length=3)
    CustPriceProc = models.CharField(max_length=2)
    TermOfPayment = models.CharField(max_length=4)
    Incoterms = models.CharField(max_length=3)
    IncotermsPort = models.CharField(max_length=28)
    TradingCurrency = models.CharField(max_length=5)
    CustomerBlocked = models.BooleanField(default=False)
    CustomerDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.CustomerNumber} - {self.CustomerName1}"

class MaterialMaster(models.Model):
    MaterialNumber = models.CharField(max_length=18, primary_key=True)
    Plant = models.CharField(max_length=4)
    MaterialDescription = models.CharField(max_length=40)
    CrossPlantStatus = models.CharField(max_length=2)
    DrawingNumber = models.CharField(max_length=30)
    FourDigitDescription = models.CharField(max_length=40)
    BasicMaterial = models.CharField(max_length=30)
    BasicMatDescription = models.CharField(max_length=40)
    MachineType = models.CharField(max_length=30)
    ProductGroup = models.CharField(max_length=30)
    ProductType = models.CharField(max_length=30)
    LifeCycleFlag = models.CharField(max_length=2)
    PlantOldMaterialNumber = models.CharField(max_length=18)
    ProductHierarchy = models.CharField(max_length=18)
    UnitOfMeasure = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.MaterialNumber} - {self.MaterialDescription}"
