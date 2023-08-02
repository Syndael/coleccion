import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Tienda } from '../models/tienda.model';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class TiendaService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getTiendas(): Observable<Tienda[]> {
        return this.http.get<Tienda[]>(Constantes.TIENDAS_URL).pipe(catchError(this.error.handleError<Tienda[]>('getTiendas', [])));
    }
}