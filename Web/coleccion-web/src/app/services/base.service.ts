import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { catchError, map } from 'rxjs/operators';

import { Constantes } from '../constantes';

import { Base } from '../models/base.model';
import { BaseDlc, BaseDlcBeanNew } from '../models/base-dlc.model';
import { BasePlataforma, BasePlataformaBeanNew } from '../models/base-plataforma.model';
import { Edicion, EdicionBeanNew } from '../models/edicion.model';

import { FiltroBase } from '../filters/base.filter';

import { ErrorService } from './error.service';

@Injectable({ providedIn: 'root', })
export class BaseService {
    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private error: ErrorService
    ) { }

    getBases(filtro: FiltroBase | undefined, incluirDefault: boolean): Observable<Base[]> {
        const baseDefault: Base = {
            id: undefined,
            tipo_base: undefined,
            nombre: undefined,
            codigo: undefined,
            saga: undefined,
            url: undefined,
            fecha_salida: undefined,
            plataformas: undefined
        };

        return this.getBasesDefault(filtro).pipe(
            map(bases => {
                if (incluirDefault) {
                    return [baseDefault, ...bases];
                } else {
                    return bases;
                }
            }),
            catchError(error => {
                console.error('Error en la llamada a la API:', error);
                return of([]);
            })
        );
    }

    getBasesDefault(filtro: FiltroBase | undefined): Observable<Base[]> {
        let params = new HttpParams()
        if (filtro) {
            if (filtro.tipo && filtro.tipo.toString() != 'undefined') {
                params = params.set('tipo_base_id', filtro.tipo);
            }
            if (filtro.tipoDescripcion && filtro.tipoDescripcion.length != 0) {
                params = params.set('tipo_base_descripcion', filtro.tipoDescripcion);
            }
            if (filtro.nombre && filtro.nombre.length != 0) {
                params = params.set('nombre', filtro.nombre);
            }
            if (filtro.saga && filtro.saga.length != 0) {
                params = params.set('saga', filtro.saga);
            }
            if (filtro.plataforma && filtro.plataforma.toString() != 'undefined') {
                params = params.set('plataforma_id', filtro.plataforma);
            }
            if (filtro.ordenSeleccionado && filtro.ordenSeleccionado.toString() != 'undefined') {
                params = params.set('orden', filtro.ordenSeleccionado.toString());
            }
        }
        return this.http.get<Base[]>(Constantes.BASES_URL, { params: params }).pipe(catchError(this.error.handleError<Base[]>('getBases', [])));
    }

    getBase(id: number): Observable<Base> {
        const url = `${Constantes.BASE_ID_URL}/${id}`;
        return this.http.get<Base>(url).pipe(catchError(this.error.handleError<Base>(`getBase url=${url}`)));
    }

    getValoresVandal(url: string): Observable<Base> {
        const url_vandal = `${Constantes.BASE_VANDAL_URL}`;
        const params = new HttpParams().set('url', url);
        return this.http.get<Base>(url_vandal, { params }).pipe(catchError(this.error.handleError<Base>(`getValoresVandal url=${url_vandal}`)));
    }

    getBasesByNombre(nombre: string): Observable<Base[]> {
        if (!nombre.trim()) {
            return of([]);
        }
        return this.http.get<Base[]>(`${Constantes.BASES_URL}/${nombre}`).pipe(catchError(this.error.handleError<Base[]>('getBasesByNombre', [])));
    }

    addBase(base: Base): Observable<any> {
        const url = `${Constantes.BASE_URL}`;
        return this.http.post(url, base, this.httpOptions).pipe(catchError(this.error.handleError<any>('addBase')));
    }

    updateBase(base: Base): Observable<any> {
        const url = `${Constantes.BASE_ID_URL}/${base.id}`;
        return this.http.put(url, base, this.httpOptions).pipe(catchError(this.error.handleError<any>('updateBase')));
    }

    deleteBase(id: number): Observable<any> {
        const url = `${Constantes.BASE_ID_URL}/${id}`;
        return this.http.delete(url).pipe(catchError(this.error.handleError<any>('deleteBase')));
    }

    getBasesPlataforma(base_id: number): Observable<BasePlataforma[]> {
        let params = new HttpParams()
        if (base_id) {
            params = params.set('base_id', base_id);
        }
        return this.http.get<BasePlataforma[]>(Constantes.BASES_PLATAFORMA_URL, { params: params }).pipe(catchError(this.error.handleError<BasePlataforma[]>(`getBasesPlataforma`)));
    }

    getBasePlataforma(id: number): Observable<BasePlataforma> {
        const url = `${Constantes.BASE_PLATAFORMA_ID_URL}/${id}`;
        return this.http.get<BasePlataforma>(url).pipe(catchError(this.error.handleError<BasePlataforma>(`getBasePlataforma url=${url}`)));
    }

    getBasesDlc(base_id: number, incluirDefault: boolean): Observable<BaseDlc[]> {
        const dlcDefault: BaseDlc = {
            id: 0,
            base: undefined,
            nombre: undefined
        };

        let params = new HttpParams()
        if (base_id) {
            params = params.set('base_id', base_id);
        }
        return this.http.get<BaseDlc[]>(Constantes.BASES_DLC_URL, { params: params }).pipe(
            map(dlcs => {
                if (incluirDefault) {
                    return [dlcDefault, ...dlcs];
                } else {
                    return dlcs;
                }
            }),
            catchError(this.error.handleError<BaseDlc[]>(`getBasesDlc`)));
    }

    addBasePlataforma(juego: number | undefined, plataforma: number | undefined, fecha: string | undefined): Observable<any> {
        if (juego && plataforma) {
            let basePlata: BasePlataformaBeanNew = {
                base: juego,
                plataforma: plataforma,
                fecha: fecha
            };
            return this.http.post(Constantes.BASE_PLATAFORMA_URL, basePlata, this.httpOptions).pipe(catchError(this.error.handleError<any>('addBasePlataforma')));
        }
        this.error.printError("No se ha encontrado la base o plataforma");
        return of([]);
    }

    deleteBasePlataforma(basePlataforma: number | undefined): Observable<any> {
        if (basePlataforma) {
            const url = `${Constantes.BASE_PLATAFORMA_ID_URL}/${basePlataforma}`;
            return this.http.delete(url, this.httpOptions).pipe(catchError(this.error.handleError<any>('deleteBasePlataforma')));
        }
        this.error.printError("No se ha encontrado la base");
        return of([]);
    }

    getEdiciones(base_id: number | undefined): Observable<Edicion[]> {
        let params = new HttpParams()
        if (base_id) {
            params = params.set('base_id', base_id);
        }
        return this.http.get<Edicion[]>(Constantes.EDICIONES_URL, { params: params }).pipe(catchError(this.error.handleError<Edicion[]>(`getEdiciones`)));
    }

    getEdicion(id: number): Observable<Edicion> {
        const url = `${Constantes.EDICION_ID_URL}/${id}`;
        return this.http.get<Edicion>(url).pipe(catchError(this.error.handleError<Edicion>(`getEdicion url=${url}`)));
    }

    addEdicion(juego: number | undefined, plataforma: number | undefined, nombre: string | undefined, fecha: string | undefined): Observable<any> {
        if (juego && nombre) {
            let edi: EdicionBeanNew = {
                base: juego,
                plataforma: plataforma,
                nombre: nombre,
                fecha: fecha
            };
            return this.http.post(Constantes.EDICION_URL, edi, this.httpOptions).pipe(catchError(this.error.handleError<any>('addEdicion')));
        }
        this.error.printError("No se ha encontrado la base o nombre");
        return of([]);
    }

    addBaseDlc(juego: number | undefined, nombre: string | undefined): Observable<any> {
        if (juego && nombre) {
            let dlc: BaseDlcBeanNew = {
                base: juego,
                nombre: nombre
            };
            return this.http.post(Constantes.BASE_DLC_URL, dlc, this.httpOptions).pipe(catchError(this.error.handleError<any>('addBaseDlc')));
        }
        this.error.printError("No se ha encontrado la base o nombre");
        return of([]);
    }

    deleteEdicion(edicion: number | undefined): Observable<any> {
        if (edicion) {
            const url = `${Constantes.EDICION_ID_URL}/${edicion}`;
            return this.http.delete(url, this.httpOptions).pipe(catchError(this.error.handleError<any>('deleteEdicion')));
        }
        this.error.printError("No se ha encontrado la base");
        return of([]);
    }

    deleteBaseDlc(dlc: number | undefined): Observable<any> {
        if (dlc) {
            const url = `${Constantes.BASE_DLC_ID_URL}/${dlc}`;
            return this.http.delete(url, this.httpOptions).pipe(catchError(this.error.handleError<any>('deleteBaseDlc')));
        }
        this.error.printError("No se ha encontrado la base");
        return of([]);
    }
}