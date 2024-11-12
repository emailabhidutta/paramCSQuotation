import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:8000/api/users/'; // Update with your Django API URL

  constructor(private http: HttpClient, private authService: AuthService) { }

  getUsers(): Observable<any> {
    return this.http.get<any>(this.apiUrl).pipe(catchError(this.authService.handleError));
  }

  createUser(userData: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, userData).pipe(catchError(this.authService.handleError));
  }

  updateUser(userId: number, userData: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}${userId}/`, userData).pipe(catchError(this.authService.handleError));
  }

  deleteUser(userId: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}${userId}/`).pipe(catchError(this.authService.handleError));
  }
}
