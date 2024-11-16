import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CustomerMaster } from '../models/quotation.model';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class CustomerService {
  private apiUrl = 'api/customers'; // Adjust this to your API endpoint

  constructor(private http: HttpClient) { }

  searchCustomers(term: string): Observable<CustomerMaster[]> {
    return this.http.get<CustomerMaster[]>(`${this.apiUrl}/search?term=${term}`).pipe(
      catchError(this.handleError<CustomerMaster[]>('searchCustomers', []))
    );
  }

  getCustomerDetails(customerNumber: string): Observable<CustomerMaster> {
    return this.http.get<CustomerMaster>(`${this.apiUrl}/${customerNumber}`).pipe(
      catchError(this.handleError<CustomerMaster>('getCustomerDetails'))
    );
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(`${operation} failed: ${error.message}`);
      // Let the app keep running by returning an empty result.
      return new Observable<T>();
    };
  }
}
