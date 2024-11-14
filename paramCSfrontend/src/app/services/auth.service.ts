import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, BehaviorSubject } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/';
  private currentUserSubject: BehaviorSubject<any>;
  public currentUser: Observable<any>;

  constructor(private http: HttpClient) {
    this.currentUserSubject = new BehaviorSubject<any>(JSON.parse(localStorage.getItem('currentUser') || '{}'));
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue() {
    return this.currentUserSubject.value;
  }

  login(username: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}token/`, { username, password })
      .pipe(
        tap(response => {
          localStorage.setItem('token', response.access);
          localStorage.setItem('refresh_token', response.refresh);
          localStorage.setItem('currentUser', JSON.stringify({ username }));
          this.currentUserSubject.next({ username });
        }),
        catchError(error => {
          console.error('Login error:', error);
          if (error.error instanceof ErrorEvent) {
            console.error('Client-side error:', error.error.message);
          } else {
            console.error('Server-side error:', error.status, error.error);
          }
          return throwError('Login failed. Please check your credentials and try again.');
        })
      );
  }


  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('currentUser');
    this.currentUserSubject.next(null);
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

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'An error occurred';
    if (error.error instanceof ErrorEvent) {
      errorMessage = `Error: ${error.error.message}`;
    } else {
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    console.error(errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
