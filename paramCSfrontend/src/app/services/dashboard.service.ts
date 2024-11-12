import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ConfigService } from './config.service';
import { switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  constructor(
    private http: HttpClient,
    private configService: ConfigService
  ) { }

  getDashboardData(): Observable<any> {
    return this.configService.getConfig().pipe(
      switchMap(config => this.http.get(`${config.ApiUrl}/dashboard`))
    );
  }

  // Add more methods as needed for specific dashboard data
}
