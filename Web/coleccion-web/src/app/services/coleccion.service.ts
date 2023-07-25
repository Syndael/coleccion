import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Coleccion } from '../models/coleccion.model';

@Injectable({ providedIn: 'root', })
export class ColeccionService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(private http: HttpClient) { }

    getColecciones(): Observable<Coleccion[]> {
        return this.http.get<Coleccion[]>(Constantes.COLECCIONES_URL).pipe(catchError(this.handleError<Coleccion[]>('getColecciones', [])));
    }

    getColeccion(id: number): Observable<Coleccion> {
        const url = `${Constantes.COLECCION_URL}/${id}`;
        return this.http.get<Coleccion>(url).pipe(catchError(this.handleError<Coleccion>(`getColeccion url=${url}`)));
    }

    private handleError<T>(operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {
            console.error(error);
            return of(result as T);
        };
    }
}