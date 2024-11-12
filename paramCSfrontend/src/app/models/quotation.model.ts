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
  Date: Date;
  CreationDate: Date;
  QStatusID: QuotationStatus;
  created_by?: number; // Assuming this is the user ID
  last_modified_by?: number; // Assuming this is the user ID
  total_value: number;
  rejection_reason?: string;
  details?: QuotationDetails[];
  is_valid?: boolean;
}

export interface QuotationDetails {
  QuotationDetailsId: number;
  QuoteId: string;
  QuoteRevisionNo: string;
  QuoteRevisionDate?: Date;
  SalesOrganization: string; // This should be the SalesOrganizationID
  CustomerInquiryNo?: string;
  SoldToCustomerNumber: string;
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
  QuoteValidFrom: Date;
  QuoteValidUntil: Date;
  SalesEmployeeNo?: string;
  DeliveryDate?: Date;
  CustomerPONumber?: string;
  ApprovalStatus: string;
  items?: QuotationItemDetails[];
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
}
