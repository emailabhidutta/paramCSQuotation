import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_URL } from '../app.module';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  constructor(
    private http: HttpClient,
    @Inject(API_URL) private apiUrl: string
  ) { }

  getDashboardData(): Observable<any> {
    return this.http.get(`${this.apiUrl}/dashboard/`);
  }
}
