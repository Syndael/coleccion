import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Juego } from '../models/juego.model';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class JuegoService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getJuegos(): Observable<Juego[]> {
        return this.http.get<Juego[]>(Constantes.JUEGOS_URL).pipe(catchError(this.error.handleError<Juego[]>('getJuegos', [])));
    }

    getJuego(id: number): Observable<Juego> {
        const url = `${Constantes.JUEGO_ID_URL}/${id}`;
        return this.http.get<Juego>(url).pipe(catchError(this.error.handleError<Juego>(`getJuego url=${url}`)));
    }

    getJuegosByNombre(nombre: string): Observable<Juego[]> {
        if (!nombre.trim()) {
            return of([]);
        }
        return this.http.get<Juego[]>(`${Constantes.JUEGOS_URL}/${nombre}`).pipe(catchError(this.error.handleError<Juego[]>('getJuegosByNombre', [])));
    }

    addJuego(juego: Juego): Observable<any> {
        const url = `${Constantes.JUEGO_URL}`;
        return this.http.post(url, juego, this.httpOptions).pipe(catchError(this.error.handleError<any>('addJuego')));
    }

    updateJuego(juego: Juego): Observable<any> {
        const url = `${Constantes.JUEGO_ID_URL}/${juego.id}`;
        return this.http.put(url, juego, this.httpOptions).pipe(catchError(this.error.handleError<any>('updateJuego')));
    }

}