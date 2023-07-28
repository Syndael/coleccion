import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Estado } from '../models/estado.model';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class EstadoService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getEstados(): Observable<Estado[]> {
        return this.http.get<Estado[]>(Constantes.ESTADOS_URL).pipe(catchError(this.error.handleError<Estado[]>('getEstados', [])));
    }
}