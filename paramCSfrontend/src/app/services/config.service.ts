import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { shareReplay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  private config$: Observable<any>;

  constructor(private http: HttpClient) {
    this.config$ = this.http.get('/appsettings.json').pipe(
      shareReplay(1)
    );
  }

  getConfig(): Observable<any> {
    return this.config$;
  }
}
