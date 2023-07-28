import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { Estado } from '../models/estado.model';
import { Idioma } from '../models/idioma.model';
import { Juego } from '../models/juego.model';
import { Plataforma } from '../models/plataforma.model';
import { Region } from '../models/region.model';
import { TipoRom } from '../models/tipo-rom.model';

import { EstadoService } from '../services/estado.service';
import { IdiomaService } from '../services/idioma.service';
import { JuegoService } from '../services/juego.service';
import { PlataformaService } from '../services/plataforma.service';
import { RegionService } from '../services/region.service';
import { TipoRomService } from '../services/tipo-rom.service';
import { TipoEstado } from '../models/tipo-estado';

@Injectable({ providedIn: 'root', })
export class UtilService {
  estadosGeneral: Estado[] = [];
  estadosCajas: Estado[] = [];
  estadosHistorial: Estado[] = [];
  idiomas: Idioma[] = [];
  juegos: Juego[] = [];
  plataformas: Plataforma[] = [];
  regiones: Region[] = [];
  tiposRom: TipoRom[] = [];

  constructor(
    private estadoService: EstadoService,
    private idiomaService: IdiomaService,
    private juegoService: JuegoService,
    private plataformaService: PlataformaService,
    private regionService: RegionService,
    private tipoRomService: TipoRomService
  ) { }

  formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = this.addLeadingZero(date.getMonth() + 1);
    const day = this.addLeadingZero(date.getDate());
    return `${year}-${month}-${day}`;
  }
  private addLeadingZero(value: number): string {
    return value < 10 ? `0${value}` : `${value}`;
  }

  formatNumber(rawValue: string | number | undefined): number | undefined {
    if (rawValue == undefined) {
      return undefined;
    }
    const value = typeof rawValue === 'string' ? Number(rawValue.replace(/,/g, '')) : rawValue;
    const num = value.toLocaleString('en-US', { maximumFractionDigits: 2 });
    return Number(num.replace(/,/g, ''));
  }

  getListaEstados(tipo: TipoEstado, incluirDefault: Boolean): Observable<Estado[]> {
    const estadoNull: Estado = {
      id: undefined,
      descripcion: '',
      tipo: -1
    }

    if (this.getListaEstadosByTipo(tipo).length === 0) {
      return this.estadoService.getEstados().pipe(
        map(estados => {
          this.estadosGeneral = estados.filter((estado) => estado.tipo === TipoEstado.GENERAL);
          this.estadosCajas = estados.filter((estado) => estado.tipo === TipoEstado.CAJAS);
          this.estadosHistorial = estados.filter((estado) => estado.tipo === TipoEstado.HISTORIAL);

          if (incluirDefault) {
            return [estadoNull, ...this.getListaEstadosByTipo(tipo)];
          } else {
            return this.getListaEstadosByTipo(tipo);
          }
        }),
        catchError(error => {
          console.error('Error en la llamada a la API:', error);
          return of([]);
        })
      );
    } else {
      if (incluirDefault) {
        return of([estadoNull, ...this.getListaEstadosByTipo(tipo)]);
      } else {
        return of(this.getListaEstadosByTipo(tipo));
      }
    }
  }
  private getListaEstadosByTipo(tipo: TipoEstado): Estado[] {
    if (tipo === TipoEstado.GENERAL) {
      return this.estadosGeneral;
    } else if (tipo === TipoEstado.CAJAS) {
      return this.estadosCajas;
    } else if (tipo === TipoEstado.HISTORIAL) {
      return this.estadosHistorial;
    }
    return [];
  }
  getListaIdiomas(incluirDefault: Boolean): Observable<Idioma[]> {
    const idiomaNull: Idioma = {
      id: undefined,
      descripcion: '',
      corto: undefined
    }

    if (this.idiomas.length === 0) {
      return this.idiomaService.getIdiomas().pipe(
        map(idiomas => {
          this.idiomas = idiomas;
          if (incluirDefault) {
            return [idiomaNull, ...this.idiomas];
          } else {
            return this.idiomas;
          }
        }),
        catchError(error => {
          console.error('Error en la llamada a la API:', error);
          return of([]);
        })
      );
    } else {
      if (incluirDefault) {
        return of([idiomaNull, ...this.idiomas]);
      } else {
        return of(this.idiomas);
      }
    }
  }
  getListaJuegos(): Observable<Juego[]> {
    if (this.juegos.length === 0) {
      return this.juegoService.getJuegos().pipe(
        map(juegos => {
          this.juegos = juegos;
          return juegos;
        }),
        catchError(error => {
          console.error('Error en la llamada a la API:', error);
          return of([]);
        })
      );
    } else {
      return of(this.juegos);
    }
  }
  getListaPlataformas(): Observable<Plataforma[]> {
    if (this.plataformas.length === 0) {
      return this.plataformaService.getPlataformas().pipe(
        map(plataformas => {
          this.plataformas = plataformas;
          return plataformas;
        }),
        catchError(error => {
          console.error('Error en la llamada a la API:', error);
          return of([]);
        })
      );
    } else {
      return of(this.plataformas);
    }
  }
  getListaRegiones(incluirDefault: Boolean): Observable<Region[]> {
    const regionNull: Idioma = {
      id: undefined,
      descripcion: '',
      corto: undefined
    }

    if (this.regiones.length === 0) {
      return this.regionService.getRegiones().pipe(
        map(regiones => {
          this.regiones = regiones;
          if (incluirDefault) {
            return [regionNull, ...this.regiones];
          } else {
            return this.regiones;
          }
        }),
        catchError(error => {
          console.error('Error en la llamada a la API:', error);
          return of([]);
        })
      );
    } else {
      if (incluirDefault) {
        return of([regionNull, ...this.regiones]);
      } else {
        return of(this.regiones);
      }
    }
  }
  getListaTiposRom(incluirDefault: Boolean): Observable<TipoRom[]> {
    const tipoRomNull: TipoRom = {
      id: undefined,
      extension: ''
    }

    if (this.tiposRom.length === 0) {
      return this.tipoRomService.getTiposRom().pipe(
        map(tiposRom => {
          this.tiposRom = tiposRom;
          if (incluirDefault) {
            return [tipoRomNull, ...this.tiposRom];
          } else {
            return this.tiposRom;
          }
        }),
        catchError(error => {
          console.error('Error en la llamada a la API:', error);
          return of([]);
        })
      );
    } else {
      if (incluirDefault) {
        return of([tipoRomNull, ...this.tiposRom]);
      } else {
        return of(this.tiposRom);
      }
    }
  }


  setListaIdiomas(idiomas: Idioma[]): void {
    this.idiomas = idiomas;
  }
  setListaJuegos(juegos: Juego[]): void {
    this.juegos = juegos;
  }
  setListaPlataformas(plataformas: Plataforma[]): void {
    this.plataformas = plataformas;
  }
  setListaRegiones(regiones: Region[]): void {
    this.regiones = regiones;
  }
  setListaTiposRom(tiposRom: TipoRom[]): void {
    this.tiposRom = tiposRom;
  }
}