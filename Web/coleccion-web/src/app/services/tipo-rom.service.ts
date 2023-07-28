import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { TipoRom } from '../models/tipo-rom.model';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class TipoRomService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getTiposRom(): Observable<TipoRom[]> {
        return this.http.get<TipoRom[]>(Constantes.TIPOS_ROM_URL).pipe(catchError(this.error.handleError<TipoRom[]>('getTiposRom', [])));
    }

}