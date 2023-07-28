import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Region } from '../models/region.model';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class RegionService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getRegiones(): Observable<Region[]> {
        return this.http.get<Region[]>(Constantes.REGIONES_URL).pipe(catchError(this.error.handleError<Region[]>('getRegiones', [])));
    }

}