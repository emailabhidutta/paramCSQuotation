export interface QuotationStatus {
  QStatusID: string;
  QStatusName: string;
}

export interface Quotation {
  QuoteId: string;
  QuotationNo: string;
  CustomerNumber: string;
  LastRevision: string;
  CustomerInquiryNo?: string;
  Date: string;
  CreationDate: string;
  QStatusID: QuotationStatus;
  created_by: string;
  last_modified_by: string;
  total_value: number;
  rejection_reason?: string;
  QuoteValidFrom?: string;
  QuoteValidUntil?: string;
  CustomerEmail?: string;
  Version: number;
  Remarks?: string;
  GSTVATValue: number;
  TotalDiscount: number;
  details: QuotationDetails[];
}

export interface QuotationDetails {
  QuotationDetailsId: number;
  QuoteId: string;
  QuoteRevisionNo: string;
  QuoteRevisionDate?: string;
  SalesOrganization: string;
  CustomerInquiryNo?: string;
  SoldToCustomerNumber?: string;
  ShipToCustomerNumber?: string;
  SalesGroup?: string;
  Customer?: string;
  CustomerName?: string;
  CustomerName2?: string;
  IndustryCode1?: string;
  CustPriceProcedure?: string;
  MaterialDisplay?: string;
  TermOfPayment?: string;
  Incoterms?: string;
  IncotermsPart2?: string;
  TradingCurrency: string;
  SalesEmployeeNo?: string;
  DeliveryDate?: string;
  CustomerPONumber?: string;
  ApprovalStatus: ApprovalStatus;
  Version: number;
  PaymentTerms?: string;
  DeliveryMethod?: string;
  items: QuotationItemDetails[];
}

export interface QuotationItemDetails {
  QuoteItemId: number;
  QuotationDetailsId: number;
  MaterialNumber: string;
  CustomerMatNumber?: string;
  FullMaterialDescription?: string;
  MaterialDescription?: string;
  BasicMaterialText?: string;
  DrawingNo?: string;
  PricePer: number;
  Per: number;
  UnitOfMeasure: string;
  DiscountValue?: number;
  SurchargeValue?: number;
  OrderQuantity: number;
  OrderValue: number;
  ItemText?: string;
  Usage?: string;
  IsDeleted: boolean;
}

export interface SalesOrganization {
  SalesOrganizationID: string;
  CompanyID: string;
  SalesOrganizationName: string;
}

export interface Currency {
  CurrencyID: string;
  CurrencyName: string;
}

export interface CurrencyExchange {
  CurrencyExchangeID: number;
  FromCurrencyID: string;
  ToCurrencyID: string;
  EffectiveDate: string;
  ExchangeFactor: number;
}

export interface CustomerMaster {
  CustomerNumber: string;
  SalesOrg: string;
  Country: string;
  CustomerClass: string;
  CustomerName1: string;
  CustomerName2?: string;
  SearchTerm: string;
  Street?: string;
  City?: string;
  PostalCode?: string;
  Email?: string;
  Phone?: string;
  CustPriceProcedure?: string;
  PaymentTerm?: string;
  Incoterms?: string;
}

export interface MaterialMaster {
  MaterialNumber: string;
  Plant: string;
  ProductGroup: string;
  ProductType: string;
  MaterialDescription: string;
  DrawingNumber?: string;
  UnitOfMeasure: string;
  BasePrice?: number;
  FullMaterialDescription?: string;
  BasicMaterialText?: string;
}

export interface PriceMasterDetails {
  MaterialNumber: string;
  BasePrice: number;
  Currency: string;
  ValidFrom: string;
  ValidTo: string;
  PriceUnit: number;
  UnitOfMeasure: string;
}

export interface QuotationSummary {
  QuoteId: string;
  QuotationNo: string;
  CustomerNumber: string;
  CustomerName: string;
  Date: string;
  QStatusID: QuotationStatus;
  total_value: number;
}

export enum ApprovalStatus {
  Pending = 'Pending',
  Approved = 'Approved',
  Rejected = 'Rejected'
}

export enum MaterialDisplayOption {
  Full = 'Full Material Description',
  FourDigit = '4 digit Description (Text)',
  Basic = 'Basic Material (Text)',
  Drawing = 'Drawing #'
}
