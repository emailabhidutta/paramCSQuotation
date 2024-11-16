import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { MaterialMaster } from '../models/quotation.model';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class MaterialService {
  private apiUrl = 'api/materials'; // Adjust this to your API endpoint

  constructor(private http: HttpClient) { }

  searchMaterials(term: string): Observable<MaterialMaster[]> {
    return this.http.get<MaterialMaster[]>(`${this.apiUrl}/search?term=${term}`).pipe(
      catchError(this.handleError<MaterialMaster[]>('searchMaterials', []))
    );
  }

  getMaterialDetails(materialNumber: string): Observable<MaterialMaster> {
    return this.http.get<MaterialMaster>(`${this.apiUrl}/${materialNumber}`).pipe(
      catchError(this.handleError<MaterialMaster>('getMaterialDetails'))
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
