import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Idioma } from '../models/idioma.model';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class IdiomaService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getIdiomas(): Observable<Idioma[]> {
        return this.http.get<Idioma[]>(Constantes.IDIOMAS_URL).pipe(catchError(this.error.handleError<Idioma[]>('getIdiomas', [])));
    }

}