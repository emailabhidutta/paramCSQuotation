import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_URL } from '../app.module';

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
  total_value: number;
  rejection_reason?: string;
}

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
  constructor(
    private http: HttpClient,
    @Inject(API_URL) private apiUrl: string
  ) { }

  getDashboardData(): Observable<DashboardData> {
    return this.http.get<DashboardData>(`${this.apiUrl}dashboard/`);
  }

  getQuotations(): Observable<Quotation[]> {
    return this.http.get<Quotation[]>(`${this.apiUrl}quotation/quotations/`);
  }

  getQuotationById(id: string): Observable<Quotation> {
    return this.http.get<Quotation>(`${this.apiUrl}quotation/quotations/${id}/`);
  }

  getQuotationsByStatus(status: string): Observable<Quotation[]> {
    return this.http.get<Quotation[]>(`${this.apiUrl}quotation/quotations/?status=${status}`);
  }

  createQuotation(quotationData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}quotation/quotations/`, quotationData);
  }

  updateQuotation(id: string, quotationData: Partial<Quotation>): Observable<Quotation> {
    return this.http.put<Quotation>(`${this.apiUrl}quotation/quotations/${id}/`, quotationData);
  }

  deleteQuotation(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}quotation/quotations/${id}/`);
  }

  getQuotationStatuses(): Observable<QuotationStatus[]> {
    return this.http.get<QuotationStatus[]>(`${this.apiUrl}quotation/statuses/`);
  }
}
