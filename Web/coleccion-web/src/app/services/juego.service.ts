import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Juego } from '../models/juego.model';

@Injectable({ providedIn: 'root', })
export class JuegoService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(private http: HttpClient) { }

    getJuegos(): Observable<Juego[]> {
        return this.http.get<Juego[]>(Constantes.JUEGOS_URL).pipe(catchError(this.handleError<Juego[]>('getJuegos', [])));
    }

    getJuego(id: number): Observable<Juego> {
        const url = `${Constantes.JUEGO_ID_URL}/${id}`;
        return this.http.get<Juego>(url).pipe(catchError(this.handleError<Juego>(`getJuego url=${url}`)));
    }

    getJuegosByNombre(nombre: string): Observable<Juego[]> {
        if (!nombre.trim()) {
            return of([]);
        }
        return this.http.get<Juego[]>(`${Constantes.JUEGOS_URL}/${nombre}`).pipe(catchError(this.handleError<Juego[]>('getJuegosByNombre', [])));
    }

    addJuego(juego: Juego): Observable<any> {
        const url = `${Constantes.JUEGO_URL}`;
        return this.http.post(url, juego, this.httpOptions).pipe(catchError(this.handleError<any>('addJuego')));
    }

    updateJuego(juego: Juego): Observable<any> {
        const url = `${Constantes.JUEGO_ID_URL}/${juego.id}`;
        return this.http.put(url, juego, this.httpOptions).pipe(catchError(this.handleError<any>('updateJuego')));
    }

    private handleError<T>(operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {
            console.error(error);
            return of(result as T);
        };
    }
}