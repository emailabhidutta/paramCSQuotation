import { Injectable, Inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, shareReplay } from 'rxjs/operators';
import { API_URL } from '../app.module';
import {
  Quotation,
  QuotationStatus,
  QuotationDetails,
  QuotationItemDetails,
  CustomerMaster,
  MaterialMaster,
  SalesOrganization,
  Currency,
  CurrencyExchange
} from '../models/quotation.model';

export interface DashboardData {
  totalQuotations: number;
  acceptedQuotations: number;
  rejectedQuotations: number;
  cancelledQuotations: number;
  pendingQuotations: number;
  totalValue: number;
}

@Injectable({
  providedIn: 'root'
})
export class QuotationService {
  private quotationStatuses$: Observable<QuotationStatus[]>;

  constructor(
    private http: HttpClient,
    @Inject(API_URL) private apiUrl: string
  ) {
    this.quotationStatuses$ = this.http.get<QuotationStatus[]>(`${this.apiUrl}quotation/statuses/`)
      .pipe(
        shareReplay(1),
        catchError(this.handleError)
      );
  }

  getDashboardData(): Observable<DashboardData> {
    return this.http.get<DashboardData>(`${this.apiUrl}dashboard/`)
      .pipe(catchError(this.handleError));
  }

  getQuotations(page: number = 1, pageSize: number = 10, status?: string): Observable<Quotation[]> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    if (status) {
      params = params.set('status', status);
    }

    return this.http.get<Quotation[]>(`${this.apiUrl}quotation/quotations/`, { params })
      .pipe(catchError(this.handleError));
  }

  getQuotationById(id: string): Observable<Quotation> {
    return this.http.get<Quotation>(`${this.apiUrl}quotation/quotations/${id}/`)
      .pipe(catchError(this.handleError));
  }

  createQuotation(quotationData: Partial<Quotation>): Observable<Quotation> {
    return this.http.post<Quotation>(`${this.apiUrl}quotation/quotations/`, quotationData)
      .pipe(catchError(this.handleError));
  }

  updateQuotation(id: string, quotationData: Partial<Quotation>): Observable<Quotation> {
    return this.http.put<Quotation>(`${this.apiUrl}quotation/quotations/${id}/`, quotationData)
      .pipe(catchError(this.handleError));
  }

  deleteQuotation(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}quotation/quotations/${id}/`)
      .pipe(catchError(this.handleError));
  }

  getQuotationStatuses(): Observable<QuotationStatus[]> {
    return this.quotationStatuses$;
  }

  approveQuotation(id: string): Observable<Quotation> {
    return this.http.post<Quotation>(`${this.apiUrl}quotation/quotations/${id}/approve/`, {})
      .pipe(catchError(this.handleError));
  }

  rejectQuotation(id: string, reason: string): Observable<Quotation> {
    return this.http.post<Quotation>(`${this.apiUrl}quotation/quotations/${id}/reject/`, { reason })
      .pipe(catchError(this.handleError));
  }

  reviseQuotation(id: string): Observable<Quotation> {
    return this.http.post<Quotation>(`${this.apiUrl}quotation/quotations/${id}/revise/`, {})
      .pipe(catchError(this.handleError));
  }

  // New methods based on your Django models and views

  getQuotationDetails(quoteId: string): Observable<QuotationDetails[]> {
    return this.http.get<QuotationDetails[]>(`${this.apiUrl}quotation/quotations/${quoteId}/details/`)
      .pipe(catchError(this.handleError));
  }

  getQuotationItemDetails(detailsId: number): Observable<QuotationItemDetails[]> {
    return this.http.get<QuotationItemDetails[]>(`${this.apiUrl}quotation/details/${detailsId}/items/`)
      .pipe(catchError(this.handleError));
  }

  createQuotationDetails(quoteId: string, details: Partial<QuotationDetails>): Observable<QuotationDetails> {
    return this.http.post<QuotationDetails>(`${this.apiUrl}quotation/quotations/${quoteId}/details/`, details)
      .pipe(catchError(this.handleError));
  }

  createQuotationItemDetails(detailsId: number, item: Partial<QuotationItemDetails>): Observable<QuotationItemDetails> {
    return this.http.post<QuotationItemDetails>(`${this.apiUrl}quotation/details/${detailsId}/items/`, item)
      .pipe(catchError(this.handleError));
  }

  deleteQuotationItem(detailsId: number, itemId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}quotation/details/${detailsId}/items/${itemId}/`)
      .pipe(catchError(this.handleError));
  }

  searchCustomers(term: string): Observable<CustomerMaster[]> {
    return this.http.get<CustomerMaster[]>(`${this.apiUrl}master/customers/search/?term=${term}`)
      .pipe(catchError(this.handleError));
  }

  searchMaterials(term: string): Observable<MaterialMaster[]> {
    return this.http.get<MaterialMaster[]>(`${this.apiUrl}master/materials/search/?term=${term}`)
      .pipe(catchError(this.handleError));
  }

  getSalesOrganizations(): Observable<SalesOrganization[]> {
    return this.http.get<SalesOrganization[]>(`${this.apiUrl}company/sales-organizations/`)
      .pipe(catchError(this.handleError));
  }

  getCurrencies(): Observable<Currency[]> {
    return this.http.get<Currency[]>(`${this.apiUrl}finance/currencies/`)
      .pipe(catchError(this.handleError));
  }

  getCurrencyExchangeRates(): Observable<CurrencyExchange[]> {
    return this.http.get<CurrencyExchange[]>(`${this.apiUrl}finance/currency-exchange-rates/`)
      .pipe(catchError(this.handleError));
  }

  private handleError(error: any) {
    console.error('An error occurred:', error);
    return throwError(() => new Error('An error occurred. Please try again later.'));
  }
}
