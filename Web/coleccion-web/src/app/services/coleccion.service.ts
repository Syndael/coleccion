import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Coleccion } from '../models/coleccion.model';
import { FiltroColeccion } from '../filters/coleccion.filter';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class ColeccionService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getColecciones(filtro: FiltroColeccion | undefined): Observable<Coleccion[]> {
        let params = new HttpParams()
        if (filtro) {
            if (filtro.tipo && filtro.tipo.toString() != 'undefined') {
                params = params.set('tipo_base_id', filtro.tipo.toString());
            }
            if (filtro.plataformaSeleccionada && filtro.plataformaSeleccionada.toString() != 'undefined') {
                params = params.set('plataforma_id', filtro.plataformaSeleccionada.toString());
            }
            if (filtro.nombreBase && filtro.nombreBase.length != 0) {
                params = params.set('nombre', filtro.nombreBase);
            }
            if (filtro.saga && filtro.saga.length != 0) {
                params = params.set('saga', filtro.saga);
            }
            if (filtro.estadoGeneralSeleccionado && filtro.estadoGeneralSeleccionado.toString() != 'undefined') {
                params = params.set('estado_gen_id', filtro.estadoGeneralSeleccionado.toString());
            }
            if (filtro.tiendaSeleccionada && filtro.tiendaSeleccionada.toString() != 'undefined') {
                params = params.set('tienda_id', filtro.tiendaSeleccionada.toString());
            }
        }
        return this.http.get<Coleccion[]>(Constantes.COLECCIONES_URL, { params: params }).pipe(catchError(this.error.handleError<Coleccion[]>('getColecciones', [])));
    }

    getColeccion(id: number): Observable<Coleccion> {
        const url = `${Constantes.COLECCION_ID_URL}/${id}`;
        return this.http.get<Coleccion>(url).pipe(catchError(this.error.handleError<Coleccion>(`getColeccion url=${url}`)));
    }

    addColeccion(coleccion: Coleccion): Observable<any> {
        const url = `${Constantes.COLECCION_URL}`;
        return this.http.post(url, coleccion, this.httpOptions).pipe(catchError(this.error.handleError<any>('addColeccion')));
    }

    updateColeccion(coleccion: Coleccion): Observable<any> {
        const url = `${Constantes.COLECCION_ID_URL}/${coleccion.id}`;
        return this.http.put(url, coleccion, this.httpOptions).pipe(catchError(this.error.handleError<any>('updateColeccion')));
    }

    deleteColeccion(id: number): Observable<any> {
        const url = `${Constantes.COLECCION_ID_URL}/${id}`;
        return this.http.delete(url).pipe(catchError(this.error.handleError<any>('deleteColeccion')));
    }
}