import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Plataforma } from '../models/plataforma.model';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class PlataformaService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getPlataformas(): Observable<Plataforma[]> {
        return this.http.get<Plataforma[]>(Constantes.PLATAFORMAS_URL).pipe(catchError(this.error.handleError<Plataforma[]>('getPlataformas', [])));
    }

}