import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { TipoBase } from '../models/tipo-base.model';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class TipoBaseService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getTiposBase(): Observable<TipoBase[]> {
        return this.http.get<TipoBase[]>(Constantes.TIPOS_BASE_URL).pipe(catchError(this.error.handleError<TipoBase[]>('getTiposBase', [])));
    }

}