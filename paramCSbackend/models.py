Python version: 3.12.7 (tags/v3.12.7:0b05ead, Oct  1 2024, 03:06:41) [MSC v.1941 64 bit (AMD64)]
Python executable: C:\Users\email\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe
Current working directory: E:\ParamCS\paramCSQuotation\paramCSbackend
DJANGO_SETTINGS_MODULE: paramCSbackend.settings
sys.path: ['E:\\ParamCS\\paramCSQuotation\\paramCSbackend', 'E:\\ParamCS\\paramCSQuotation\\paramCSbackend', 'C:\\Program Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.12_3.12.2032.0_x64__qbz5n2kfra8p0\\python312.zip', 'C:\\Program Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.12_3.12.2032.0_x64__qbz5n2kfra8p0\\DLLs', 'C:\\Program Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.12_3.12.2032.0_x64__qbz5n2kfra8p0\\Lib', 'C:\\Program Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.12_3.12.2032.0_x64__qbz5n2kfra8p0', 'C:\\Users\\email\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python312\\site-packages', 'C:\\Program Files\\WindowsApps\\PythonSoftwareFoundation.Python.3.12_3.12.2032.0_x64__qbz5n2kfra8p0\\Lib\\site-packages']
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Customermaster(models.Model):
    customernumber = models.CharField(db_column='CustomerNumber', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    salesorg = models.CharField(db_column='SalesOrg', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    accountgroup = models.CharField(db_column='AccountGroup', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customername1 = models.CharField(db_column='CustomerName1', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customername2 = models.CharField(db_column='CustomerName2', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    searchterm = models.CharField(db_column='SearchTerm', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    housestreetname = models.CharField(db_column='HouseStreetName', max_length=60, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customerclass = models.CharField(db_column='CustomerClass', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    indcode1 = models.CharField(db_column='IndCode1', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    keyaccount = models.BooleanField(db_column='KeyAccount', blank=True, null=True)  # Field name made lowercase.
    salesgroup = models.CharField(db_column='SalesGroup', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    custpriceproc = models.CharField(db_column='CustPriceProc', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    termofpayment = models.CharField(db_column='TermOfPayment', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    incoterms = models.CharField(db_column='Incoterms', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    incotermsport = models.CharField(db_column='IncotermsPort', max_length=28, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    tradingcurrency = models.CharField(db_column='TradingCurrency', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customerblocked = models.BooleanField(db_column='CustomerBlocked', blank=True, null=True)  # Field name made lowercase.
    customerdeleted = models.BooleanField(db_column='CustomerDeleted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CustomerMaster'


class Materialmaster(models.Model):
    materialnumber = models.CharField(db_column='MaterialNumber', primary_key=True, max_length=18, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    plant = models.CharField(db_column='Plant', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    materialdescription = models.CharField(db_column='MaterialDescription', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    crossplantstatus = models.CharField(db_column='CrossPlantStatus', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    drawingnumber = models.CharField(db_column='DrawingNumber', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fourdigitdescription = models.CharField(db_column='FourDigitDescription', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    basicmaterial = models.CharField(db_column='BasicMaterial', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    basicmatdescription = models.CharField(db_column='BasicMatDescription', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    machinetype = models.CharField(db_column='MachineType', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    productgroup = models.CharField(db_column='ProductGroup', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    producttype = models.CharField(db_column='ProductType', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    lifecycleflag = models.CharField(db_column='LifeCycleFlag', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    plantoldmaterialnumber = models.CharField(db_column='PlantOldMaterialNumber', max_length=18, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    producthierarchy = models.CharField(db_column='ProductHierarchy', max_length=18, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    unitofmeasure = models.CharField(db_column='UnitOfMeasure', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MaterialMaster'


class Salesperson(models.Model):
    salespersonno = models.CharField(db_column='SalesPersonNo', primary_key=True, max_length=8, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    employeelastname = models.CharField(db_column='EmployeeLastName', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    employeefirstname = models.CharField(db_column='EmployeeFirstName', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    companycode = models.CharField(db_column='CompanyCode', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ontrackid = models.CharField(db_column='OnTrackID', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SalesPerson'


class Salespricelist(models.Model):
    conditiontype = models.CharField(db_column='ConditionType', primary_key=True, max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase. The composite primary key (ConditionType, SalesOrg, DistributionChannel, Identifier, MaterialNumber) found, that is not supported. The first column is selected.
    salesorg = models.CharField(db_column='SalesOrg', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    distributionchannel = models.CharField(db_column='DistributionChannel', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    identifier = models.CharField(db_column='Identifier', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    materialnumber = models.CharField(db_column='MaterialNumber', max_length=18, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    identifiername = models.CharField(db_column='IdentifierName', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    per = models.DecimalField(db_column='Per', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UoM', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scalebasis = models.CharField(db_column='ScaleBasis', max_length=6, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    validitystartdate = models.DateField(db_column='ValidityStartDate', blank=True, null=True)  # Field name made lowercase.
    validityenddate = models.DateField(db_column='ValidityEndDate', blank=True, null=True)  # Field name made lowercase.
    deletionindicator = models.BooleanField(db_column='DeletionIndicator', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SalesPriceList'
        unique_together = (('conditiontype', 'salesorg', 'distributionchannel', 'identifier', 'materialnumber'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS')
    employeeno = models.CharField(db_column='EmployeeNo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', unique=True, max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    is_deleted = models.BooleanField()
    reset_password_token = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    reset_password_expires = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)
    roleid = models.ForeignKey('CoreRole', models.DO_NOTHING, db_column='RoleID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    customuser = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('customuser', 'group'),)


class AuthUserUserPermissions(models.Model):
    customuser = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('customuser', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    created = models.DateTimeField()
    user_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class CompanyAccountgroup(models.Model):
    accountgroupid = models.CharField(db_column='AccountGroupID', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    accountgroupname = models.CharField(db_column='AccountGroupName', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    salesorganizationid = models.ForeignKey('CompanySalesorganization', models.DO_NOTHING, db_column='SalesOrganizationID_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company_accountgroup'


class CompanyCompany(models.Model):
    companyid = models.CharField(db_column='CompanyID', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    countryid = models.ForeignKey('CompanyCountry', models.DO_NOTHING, db_column='CountryID_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company_company'


class CompanyCountry(models.Model):
    countryid = models.CharField(db_column='CountryID', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    countryname = models.CharField(db_column='CountryName', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company_country'


class CompanySalesorganization(models.Model):
    salesorganizationid = models.CharField(db_column='SalesOrganizationID', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    salesorganizationname = models.CharField(db_column='SalesOrganizationName', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    companyid = models.ForeignKey(CompanyCompany, models.DO_NOTHING, db_column='CompanyID_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company_salesorganization'


class CoreCustomuser(models.Model):
    userid = models.CharField(db_column='UserID', primary_key=True, max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    employeeno = models.CharField(db_column='EmployeeNo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    roleid_id = models.CharField(db_column='RoleID_id', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    is_deleted = models.BooleanField()
    reset_password_expires = models.DateTimeField(blank=True, null=True)
    reset_password_token = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_customuser'


class CoreRights(models.Model):
    rightsid = models.CharField(db_column='RightsID', primary_key=True, max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    rightname = models.CharField(db_column='RightName', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_rights'


class CoreRole(models.Model):
    id = models.BigAutoField(primary_key=True)
    rolename = models.CharField(db_column='RoleName', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    roleid = models.ForeignKey('self', models.DO_NOTHING, db_column='RoleID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_role'


class CoreUserrights(models.Model):
    userrightsid = models.CharField(db_column='UserRightsID', primary_key=True, max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    rightsid = models.ForeignKey(CoreRights, models.DO_NOTHING, db_column='RightsID_id')  # Field name made lowercase.
    roleid = models.ForeignKey(CoreRole, models.DO_NOTHING, db_column='RoleID_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_userrights'
        unique_together = (('roleid', 'rightsid'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    model = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    session_data = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FinanceCurrency(models.Model):
    currencyid = models.CharField(db_column='CurrencyID', primary_key=True, max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    currencyname = models.CharField(db_column='CurrencyName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'finance_currency'


class FinanceCurrencyexchange(models.Model):
    currencyexchangeid = models.CharField(db_column='CurrencyExchangeID', primary_key=True, max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    exchangefactor = models.DecimalField(db_column='ExchangeFactor', max_digits=10, decimal_places=4)  # Field name made lowercase.
    fromcurrencyid = models.ForeignKey(FinanceCurrency, models.DO_NOTHING, db_column='FromCurrencyID_id')  # Field name made lowercase.
    tocurrencyid = models.ForeignKey(FinanceCurrency, models.DO_NOTHING, db_column='ToCurrencyID_id', related_name='financecurrencyexchange_tocurrencyid_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'finance_currencyexchange'


class MasterDataCustomermaster(models.Model):
    customernumber = models.CharField(db_column='CustomerNumber', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    salesorg = models.CharField(db_column='SalesOrg', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    accountgroup = models.CharField(db_column='AccountGroup', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    customername1 = models.CharField(db_column='CustomerName1', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    customername2 = models.CharField(db_column='CustomerName2', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    searchterm = models.CharField(db_column='SearchTerm', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    housestreetname = models.CharField(db_column='HouseStreetName', max_length=60, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    customerclass = models.CharField(db_column='CustomerClass', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    indcode1 = models.CharField(db_column='IndCode1', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    keyaccount = models.BooleanField(db_column='KeyAccount')  # Field name made lowercase.
    salesgroup = models.CharField(db_column='SalesGroup', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    custpriceproc = models.CharField(db_column='CustPriceProc', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    termofpayment = models.CharField(db_column='TermOfPayment', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    incoterms = models.CharField(db_column='Incoterms', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    incotermsport = models.CharField(db_column='IncotermsPort', max_length=28, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tradingcurrency = models.CharField(db_column='TradingCurrency', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    customerblocked = models.BooleanField(db_column='CustomerBlocked')  # Field name made lowercase.
    customerdeleted = models.BooleanField(db_column='CustomerDeleted')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_data_customermaster'


class MasterDataMaterialmaster(models.Model):
    materialnumber = models.CharField(db_column='MaterialNumber', primary_key=True, max_length=18, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    plant = models.CharField(db_column='Plant', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    materialdescription = models.CharField(db_column='MaterialDescription', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    crossplantstatus = models.CharField(db_column='CrossPlantStatus', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    drawingnumber = models.CharField(db_column='DrawingNumber', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fourdigitdescription = models.CharField(db_column='FourDigitDescription', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    basicmaterial = models.CharField(db_column='BasicMaterial', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    basicmatdescription = models.CharField(db_column='BasicMatDescription', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    machinetype = models.CharField(db_column='MachineType', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    productgroup = models.CharField(db_column='ProductGroup', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    producttype = models.CharField(db_column='ProductType', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    lifecycleflag = models.CharField(db_column='LifeCycleFlag', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    plantoldmaterialnumber = models.CharField(db_column='PlantOldMaterialNumber', max_length=18, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    producthierarchy = models.CharField(db_column='ProductHierarchy', max_length=18, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    unitofmeasure = models.CharField(db_column='UnitOfMeasure', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_data_materialmaster'


class QuotationAttachment(models.Model):
    attachmentid = models.AutoField(db_column='AttachmentId', primary_key=True)  # Field name made lowercase.
    quoteid = models.ForeignKey('QuotationQuotation', models.DO_NOTHING, db_column='QuoteId')  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    filetype = models.CharField(db_column='FileType', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    filesize = models.IntegerField(db_column='FileSize', blank=True, null=True)  # Field name made lowercase.
    uploaddate = models.DateTimeField(db_column='UploadDate', blank=True, null=True)  # Field name made lowercase.
    uploadedby = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='UploadedBy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quotation_attachment'


class QuotationAuditTrail(models.Model):
    auditid = models.AutoField(db_column='AuditId', primary_key=True)  # Field name made lowercase.
    quoteid = models.ForeignKey('QuotationQuotation', models.DO_NOTHING, db_column='QuoteId')  # Field name made lowercase.
    fieldname = models.CharField(db_column='FieldName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    oldvalue = models.TextField(db_column='OldValue', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    newvalue = models.TextField(db_column='NewValue', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    changedate = models.DateTimeField(db_column='ChangeDate', blank=True, null=True)  # Field name made lowercase.
    changedby = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='ChangedBy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quotation_audit_trail'


class QuotationQuotation(models.Model):
    quoteid = models.CharField(db_column='QuoteId', primary_key=True, max_length=8, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    quotationno = models.CharField(db_column='QuotationNo', unique=True, max_length=8, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    customernumber = models.CharField(db_column='CustomerNumber', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    lastrevision = models.CharField(db_column='LastRevision', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    customerinquiryno = models.CharField(db_column='CustomerInquiryNo', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    creationdate = models.DateField(db_column='CreationDate')  # Field name made lowercase.
    total_value = models.DecimalField(max_digits=15, decimal_places=2)
    rejection_reason = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    quotevalidfrom = models.DateField(db_column='QuoteValidFrom', blank=True, null=True)  # Field name made lowercase.
    quotevaliduntil = models.DateField(db_column='QuoteValidUntil', blank=True, null=True)  # Field name made lowercase.
    customeremail = models.CharField(db_column='CustomerEmail', max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    version = models.IntegerField(db_column='Version')  # Field name made lowercase.
    qstatusid = models.ForeignKey('QuotationQuotationstatus', models.DO_NOTHING, db_column='QStatusID_id')  # Field name made lowercase.
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    last_modified_by = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='quotationquotation_last_modified_by_set', blank=True, null=True)
    gstvatvalue = models.DecimalField(db_column='GSTVATValue', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    gstvatpercentage = models.DecimalField(db_column='GSTVATPercentage', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    approvalstatus = models.CharField(db_column='ApprovalStatus', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    approvedby = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='ApprovedBy', related_name='quotationquotation_approvedby_set', blank=True, null=True)  # Field name made lowercase.
    approvaldate = models.DateTimeField(db_column='ApprovalDate', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    totaldiscountamount = models.DecimalField(db_column='TotalDiscountAmount', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    expirydate = models.DateField(db_column='ExpiryDate', blank=True, null=True)  # Field name made lowercase.
    remarks = models.TextField(db_column='Remarks', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    totaldiscount = models.DecimalField(db_column='TotalDiscount', max_digits=15, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quotation_quotation'


class QuotationQuotationdetails(models.Model):
    quotationdetailsid = models.AutoField(db_column='QuotationDetailsId', primary_key=True)  # Field name made lowercase.
    quoterevisionno = models.CharField(db_column='QuoteRevisionNo', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    quoterevisiondate = models.DateField(db_column='QuoteRevisionDate', blank=True, null=True)  # Field name made lowercase.
    customerinquiryno = models.CharField(db_column='CustomerInquiryNo', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    soldtocustomernumber = models.ForeignKey(Customermaster, models.DO_NOTHING, db_column='SoldToCustomerNumber', blank=True, null=True)  # Field name made lowercase.
    shiptocustomernumber = models.CharField(db_column='ShipToCustomerNumber', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    salesgroup = models.CharField(db_column='SalesGroup', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customer = models.CharField(db_column='Customer', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customername = models.CharField(db_column='CustomerName', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customername2 = models.CharField(db_column='CustomerName2', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    industrycode1 = models.CharField(db_column='IndustryCode1', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    custpriceprocedure = models.CharField(db_column='CustPriceProcedure', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    materialdisplay = models.CharField(db_column='MaterialDisplay', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    termofpayment = models.CharField(db_column='TermOfPayment', max_length=4, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    incoterms = models.CharField(db_column='Incoterms', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    incotermspart2 = models.CharField(db_column='IncotermsPart2', max_length=28, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    tradingcurrency = models.CharField(db_column='TradingCurrency', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    salesemployeeno = models.CharField(db_column='SalesEmployeeNo', max_length=8, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    deliverydate = models.DateField(db_column='DeliveryDate', blank=True, null=True)  # Field name made lowercase.
    customerponumber = models.CharField(db_column='CustomerPONumber', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    approvalstatus = models.CharField(db_column='ApprovalStatus', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    version = models.IntegerField(db_column='Version')  # Field name made lowercase.
    quoteid = models.ForeignKey(QuotationQuotation, models.DO_NOTHING, db_column='QuoteId_id')  # Field name made lowercase.
    salesorganization = models.ForeignKey(CompanySalesorganization, models.DO_NOTHING, db_column='SalesOrganization_id')  # Field name made lowercase.
    paymentterms = models.CharField(db_column='PaymentTerms', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    deliverymethod = models.CharField(db_column='DeliveryMethod', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quotation_quotationdetails'


class QuotationQuotationitemdetails(models.Model):
    quoteitemid = models.AutoField(db_column='QuoteItemId', primary_key=True)  # Field name made lowercase.
    materialnumber = models.CharField(db_column='MaterialNumber', max_length=18, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    customermatnumber = models.CharField(db_column='CustomerMatNumber', max_length=18, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fullmaterialdescription = models.CharField(db_column='FullMaterialDescription', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    materialdescription = models.CharField(db_column='MaterialDescription', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    basicmaterialtext = models.CharField(db_column='BasicMaterialText', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    drawingno = models.CharField(db_column='DrawingNo', max_length=35, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    priceper = models.DecimalField(db_column='PricePer', max_digits=15, decimal_places=2)  # Field name made lowercase.
    per = models.DecimalField(db_column='Per', max_digits=5, decimal_places=2)  # Field name made lowercase.
    unitofmeasure = models.CharField(db_column='UnitOfMeasure', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    discountvalue = models.DecimalField(db_column='DiscountValue', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    surchargevalue = models.DecimalField(db_column='SurchargeValue', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    orderquantity = models.DecimalField(db_column='OrderQuantity', max_digits=13, decimal_places=3)  # Field name made lowercase.
    ordervalue = models.DecimalField(db_column='OrderValue', max_digits=15, decimal_places=2)  # Field name made lowercase.
    itemtext = models.CharField(db_column='ItemText', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    usage = models.CharField(db_column='Usage', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    quotationdetailsid = models.ForeignKey(QuotationQuotationdetails, models.DO_NOTHING, db_column='QuotationDetailsId_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quotation_quotationitemdetails'


class QuotationQuotationstatus(models.Model):
    qstatusid = models.CharField(db_column='QStatusID', primary_key=True, max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    qstatusname = models.CharField(db_column='QStatusName', unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quotation_quotationstatus'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
