import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Historial } from '../models/historial.model';
import { FiltroHistorial } from '../filters/historial.filter';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class HistorialService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getHistoriales(filtro: FiltroHistorial | undefined): Observable<Historial[]> {
        let params = new HttpParams()
        if (filtro) {
            if (filtro.plataformaSeleccionada && filtro.plataformaSeleccionada.toString() != 'undefined') {
                params = params.set('plataforma_id', filtro.plataformaSeleccionada.toString());
            }
            if (filtro.nombreJuego && filtro.nombreJuego.length != 0) {
                params = params.set('nombre', filtro.nombreJuego);
            }
            if (filtro.sagaJuego && filtro.sagaJuego.length != 0) {
                params = params.set('saga', filtro.sagaJuego);
            }
            if (filtro.estadoSeleccionado && filtro.estadoSeleccionado.toString() != 'undefined') {
                params = params.set('estado_id', filtro.estadoSeleccionado.toString());
            }
        }
        return this.http.get<Historial[]>(Constantes.HISTORIALES_URL, { params: params }).pipe(catchError(this.error.handleError<Historial[]>('getHistoriales', [])));
    }

    getHistorial(id: number): Observable<Historial> {
        const url = `${Constantes.HISTORIAL_ID_URL}/${id}`;
        return this.http.get<Historial>(url).pipe(catchError(this.error.handleError<Historial>(`getHistorial url=${url}`)));
    }

    addHistorial(historial: Historial): Observable<any> {
        const url = `${Constantes.HISTORIAL_URL}`;
        return this.http.post(url, historial, this.httpOptions).pipe(catchError(this.error.handleError<any>('addHistorial')));
    }

    updateHistorial(historial: Historial): Observable<any> {
        const url = `${Constantes.HISTORIAL_ID_URL}/${historial.id}`;
        return this.http.put(url, historial, this.httpOptions).pipe(catchError(this.error.handleError<any>('updateHistorial')));
    }

}