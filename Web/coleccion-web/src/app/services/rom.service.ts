import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Rom } from '../models/rom.model';
import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class RomService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getRoms(): Observable<Rom[]> {
        return this.http.get<Rom[]>(Constantes.ROMS_URL).pipe(catchError(this.error.handleError<Rom[]>('getRoms', [])));
    }

    getRom(id: number): Observable<Rom> {
        const url = `${Constantes.ROM_ID_URL}/${id}`;
        return this.http.get<Rom>(url).pipe(catchError(this.error.handleError<Rom>(`getRom url=${url}`)));
    }

    addRom(rom: Rom): Observable<any> {
        const url = `${Constantes.ROM_URL}`;
        return this.http.post(url, rom, this.httpOptions).pipe(catchError(this.error.handleError<any>('addRom')));
    }

    updateRom(rom: Rom): Observable<any> {
        const url = `${Constantes.ROM_ID_URL}/${rom.id}`;
        return this.http.put(url, rom, this.httpOptions).pipe(catchError(this.error.handleError<any>('updateRom')));
    }
}