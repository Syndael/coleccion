import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Empresa } from '../models/empresa.model';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class EmpresaService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getEmpresas(): Observable<Empresa[]> {
        return this.http.get<Empresa[]>(Constantes.EMPRESAS_URL).pipe(catchError(this.error.handleError<Empresa[]>('getEmpresas', [])));
    }
}