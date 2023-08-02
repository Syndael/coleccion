import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

import { Constantes } from '../constantes';
import { Rom } from '../models/rom.model';
import { FiltroRom } from '../filters/roms.filter';
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

    getRoms(filtro: FiltroRom | undefined): Observable<Rom[]> {
        let params = new HttpParams()
        if (filtro) {
            if (filtro.plataformaSeleccionada && filtro.plataformaSeleccionada.toString() != 'undefined') {
                params = params.set('plataforma_id', filtro.plataformaSeleccionada.toString());
            }
            if (filtro.nombreJuego && filtro.nombreJuego.length != 0) {
                params = params.set('nombre', filtro.nombreJuego);
            }
            if (filtro.sagaJuego && filtro.sagaJuego.length != 0) {
                params = params.set('saga', filtro.sagaJuego);
            }
        }
        return this.http.get<Rom[]>(Constantes.ROMS_URL, { params: params }).pipe(catchError(this.error.handleError<Rom[]>('getRoms', [])));
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