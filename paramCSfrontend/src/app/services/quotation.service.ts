import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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
  private apiUrl = 'http://localhost:8000/api/'; // Update with your Django API URL

  constructor(private http: HttpClient) { }

  getDashboardData(): Observable<DashboardData> {
    return this.http.get<DashboardData>(`${this.apiUrl}dashboard/`);
  }

  getQuotations(): Observable<Quotation[]> {
    return this.http.get<Quotation[]>(`${this.apiUrl}quotations/`);
  }

  getQuotationById(id: string): Observable<Quotation> {
    return this.http.get<Quotation>(`${this.apiUrl}quotations/${id}/`);
  }

  getQuotationsByStatus(status: string): Observable<Quotation[]> {
    return this.http.get<Quotation[]>(`${this.apiUrl}quotations/?status=${status}`);
  }

  createQuotation(quotationData: Partial<Quotation>): Observable<Quotation> {
    return this.http.post<Quotation>(`${this.apiUrl}quotations/`, quotationData);
  }

  updateQuotation(id: string, quotationData: Partial<Quotation>): Observable<Quotation> {
    return this.http.put<Quotation>(`${this.apiUrl}quotations/${id}/`, quotationData);
  }

  deleteQuotation(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}quotations/${id}/`);
  }
}
