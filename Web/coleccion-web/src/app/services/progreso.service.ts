import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Progreso } from '../models/progreso.model';
import { FiltroProgreso } from '../filters/progreso.filter';
import { ErrorService } from './error.service';
import { ProgresoSesion } from '../models/progreso-sesion.model';

@Injectable({ providedIn: 'root', })
export class ProgresoService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getProgresos(filtro: FiltroProgreso | undefined): Observable<Progreso[]> {
        let params = new HttpParams()
        if (filtro) {
            if (filtro.plataformaSeleccionada && filtro.plataformaSeleccionada.toString() != 'undefined') {
                params = params.set('plataforma_id', filtro.plataformaSeleccionada.toString());
            }
            if (filtro.nombreBase && filtro.nombreBase.length != 0) {
                params = params.set('nombre', filtro.nombreBase);
            }
            if (filtro.saga && filtro.saga.length != 0) {
                params = params.set('saga', filtro.saga);
            }
            if (filtro.estadoSeleccionado && filtro.estadoSeleccionado.toString() != 'undefined') {
                params = params.set('estado_id', filtro.estadoSeleccionado.toString());
            }
        }
        return this.http.get<Progreso[]>(Constantes.PROGRESOS_URL, { params: params }).pipe(catchError(this.error.handleError<Progreso[]>('getProgresos', [])));
    }

    getSesiones(progreso: number): Observable<ProgresoSesion[]> {
        let params = new HttpParams()
        params = params.set('progreso_id', progreso);
        return this.http.get<ProgresoSesion[]>(Constantes.SESIONES_URL, { params: params }).pipe(catchError(this.error.handleError<ProgresoSesion[]>('getSesiones', [])));
    }

    getProgreso(id: number): Observable<Progreso> {
        const url = `${Constantes.PROGRESO_ID_URL}/${id}`;
        return this.http.get<Progreso>(url).pipe(catchError(this.error.handleError<Progreso>(`getProgreso url=${url}`)));
    }

    getUltimosProgresos(): Observable<Progreso[]> {
        const url = `${Constantes.ULTIMOS_PROGRESOS_ID_URL}`;
        return this.http.get<Progreso[]>(url).pipe(catchError(this.error.handleError<Progreso[]>(`getUiltimosProgresos url=${url}`)));
    }

    addProgreso(progreso: Progreso): Observable<any> {
        const url = `${Constantes.PROGRESO_URL}`;
        return this.http.post(url, progreso, this.httpOptions).pipe(catchError(this.error.handleError<any>('addProgreso')));
    }

    addSesion(sesion: ProgresoSesion): Observable<any> {
        const url = `${Constantes.SESION_URL}`;
        return this.http.post(url, sesion, this.httpOptions).pipe(catchError(this.error.handleError<any>('addSesion')));
    }

    updateProgreso(progreso: Progreso): Observable<any> {
        const url = `${Constantes.PROGRESO_ID_URL}/${progreso.id}`;
        return this.http.put(url, progreso, this.httpOptions).pipe(catchError(this.error.handleError<any>('updateProgreso')));
    }

    updateSesion(sesion: ProgresoSesion): Observable<any> {
        const url = `${Constantes.SESION_ID_URL}/${sesion.id}`;
        return this.http.put(url, sesion, this.httpOptions).pipe(catchError(this.error.handleError<any>('updateSesion')));
    }

    deleteProgreso(id: number): Observable<any> {
        const url = `${Constantes.PROGRESO_ID_URL}/${id}`;
        return this.http.delete(url).pipe(catchError(this.error.handleError<any>('deleteProgreso')));
    }

    deleteSesion(id: number): Observable<any> {
        const url = `${Constantes.SESION_ID_URL}/${id}`;
        return this.http.delete(url).pipe(catchError(this.error.handleError<any>('deleteSesion')));
    }

}