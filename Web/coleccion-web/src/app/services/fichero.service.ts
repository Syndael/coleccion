import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Fichero, DatoFichero } from '../models/fichero.model';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class FicheroService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getFichero(id: number): Observable<Fichero> {
        const url = `${Constantes.FICHERO_ID_URL}/${id}`;
        return this.http.get<Fichero>(url).pipe(catchError(this.error.handleError<Fichero>(`getFichero url=${url}`)));
    }

    getDatosFichero(id_coleccion: number): Observable<DatoFichero[]> {
        const url = `${Constantes.DATOS_FICHEROS_ID_URL}/${id_coleccion}`;
        return this.http.get<DatoFichero[]>(url).pipe(catchError(this.error.handleError<DatoFichero[]>('getDatosFichero', [])));
    }

    subirFichero(id_coleccion: number, tipo: string, file: File): Observable<DatoFichero> {
        const formData = new FormData();
        formData.append('fichero', file);
        formData.append('coleccion', id_coleccion.toString());
        formData.append('tipo', tipo);
        return this.http.post<DatoFichero>(Constantes.FICHERO_URL, formData).pipe(catchError(this.error.handleError<DatoFichero>('subirFichero')));
    }

    eliminarFichero(id: number): Observable<Fichero> {
        const url = `${Constantes.FICHERO_ID_URL}/${id}`;
        return this.http.delete<Fichero>(url).pipe(catchError(this.error.handleError<Fichero>(`eliminarFichero url=${url}`)));
    }
}