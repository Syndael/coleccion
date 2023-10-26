import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { catchError, map } from 'rxjs/operators';

import { Constantes } from '../constantes';

import { Completo, Gasto } from '../models/estadistica.model';

import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class EstadisticasService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getCompletos(): Observable<Completo[]> {
        return this.http.get<Completo[]>(`${Constantes.ESTADISITCAS_COMPLETOS_URL}`).pipe(catchError(this.error.handleError<Completo[]>('getCompletos', [])));
    }

    getGastos(): Observable<Gasto[]> {
        return this.http.get<Gasto[]>(`${Constantes.ESTADISITCAS_GASTOS_URL}`).pipe(catchError(this.error.handleError<Gasto[]>('getGastos', [])));
    }
}