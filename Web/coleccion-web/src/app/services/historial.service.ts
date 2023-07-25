import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Historial } from '../models/historial.model';

@Injectable({ providedIn: 'root', })
export class HistorialService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(private http: HttpClient) { }

    getHistoriales(): Observable<Historial[]> {
        return this.http.get<Historial[]>(Constantes.HISTORIALES_URL).pipe(catchError(this.handleError<Historial[]>('getHistoriales', [])));
    }

    getHistorial(id: number): Observable<Historial> {
        const url = `${Constantes.HISTORIAL_URL}/${id}`;
        return this.http.get<Historial>(url).pipe(catchError(this.handleError<Historial>(`getHistorial url=${url}`)));
    }

    private handleError<T>(operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {
            console.error(error);
            return of(result as T);
        };
    }
}