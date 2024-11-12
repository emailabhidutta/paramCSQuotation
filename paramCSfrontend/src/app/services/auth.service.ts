import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/'; // Update with your Django API URL

  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}token/`, { username, password })
      .pipe(
        tap(response => {
          localStorage.setItem('token', response.access);
          localStorage.setItem('refresh_token', response.refresh);
        }),
        catchError(this.handleError)
      );
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  refreshToken(): Observable<any> {
    const refreshToken = localStorage.getItem('refresh_token');
    return this.http.post<any>(`${this.apiUrl}token/refresh/`, { refresh: refreshToken })
      .pipe(
        tap(response => {
          localStorage.setItem('token', response.access);
        }),
        catchError(this.handleError)
      );
  }

  // Add these new methods
  getUsers(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}users/`).pipe(catchError(this.handleError));
  }

  createUser(userData: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}users/`, userData).pipe(catchError(this.handleError));
  }

  updateUser(userData: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}users/${userData.id}/`, userData).pipe(catchError(this.handleError));
  }

  deleteUser(userId: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}users/${userId}/`).pipe(catchError(this.handleError));
  }

  handleError(error: HttpErrorResponse) {
    let errorMessage = 'An error occurred';
    if (error.error instanceof ErrorEvent) {
      errorMessage = `Error: ${error.error.message}`;
    } else {
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    console.error(errorMessage);
    return throwError(errorMessage);
  }
}
