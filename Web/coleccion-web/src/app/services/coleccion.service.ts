import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Coleccion } from '../models/coleccion.model';
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

    getColecciones(): Observable<Coleccion[]> {
        return this.http.get<Coleccion[]>(Constantes.COLECCIONES_URL).pipe(catchError(this.error.handleError<Coleccion[]>('getColecciones', [])));
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
}