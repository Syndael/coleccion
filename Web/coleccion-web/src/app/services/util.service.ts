import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { Estado } from '../models/estado.model';
import { Idioma } from '../models/idioma.model';
import { Juego } from '../models/juego.model';
import { Plataforma } from '../models/plataforma.model';
import { Region } from '../models/region.model';
import { Tienda } from '../models/tienda.model';
import { TipoRom } from '../models/tipo-rom.model';

import { FiltroColeccion } from '../filters/coleccion.filter';
import { FiltroHistorial } from '../filters/historial.filter';
import { FiltroJuego } from '../filters/juego.filter';
import { FiltroRom } from '../filters/roms.filter';

import { EstadoService } from '../services/estado.service';
import { IdiomaService } from '../services/idioma.service';
import { JuegoService } from '../services/juego.service';
import { PlataformaService } from '../services/plataforma.service';
import { RegionService } from '../services/region.service';
import { TiendaService } from '../services/tienda.service';
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
  tiendas: Tienda[] = [];
  tiposRom: TipoRom[] = [];

  filtroColeccion: FiltroColeccion | undefined;
  filtroHistorial: FiltroHistorial | undefined;
  filtroJuego: FiltroJuego | undefined;
  filtroRom: FiltroRom | undefined;

  constructor(
    private estadoService: EstadoService,
    private idiomaService: IdiomaService,
    private juegoService: JuegoService,
    private plataformaService: PlataformaService,
    private regionService: RegionService,
    private tiendaService: TiendaService,
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
      return this.juegoService.getJuegos(undefined).pipe(
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
  getListaPlataformas(incluirDefault: Boolean): Observable<Plataforma[]> {
    const plataformaNull: Plataforma = {
      id: undefined,
      nombre: '',
      corto: undefined
    }

    if (this.plataformas.length === 0) {
      return this.plataformaService.getPlataformas().pipe(
        map(plataformas => {
          this.plataformas = plataformas;
          if (incluirDefault) {
            return [plataformaNull, ...this.plataformas];
          } else {
            return this.plataformas;
          }
        }),
        catchError(error => {
          console.error('Error en la llamada a la API:', error);
          return of([]);
        })
      );
    } else {
      if (incluirDefault) {
        return of([plataformaNull, ...this.plataformas]);
      } else {
        return of(this.plataformas);
      }
    }
  }
  getListaRegiones(incluirDefault: Boolean): Observable<Region[]> {
    const regionNull: Region = {
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
  getListaTiendas(incluirDefault: Boolean): Observable<Tienda[]> {
    const tiendaNull: Tienda = {
      id: undefined,
      nombre: ''
    }

    if (this.tiendas.length === 0) {
      return this.tiendaService.getTiendas().pipe(
        map(tiendas => {
          this.tiendas = tiendas;
          if (incluirDefault) {
            return [tiendaNull, ...this.tiendas];
          } else {
            return this.tiendas;
          }
        }),
        catchError(error => {
          console.error('Error en la llamada a la API:', error);
          return of([]);
        })
      );
    } else {
      if (incluirDefault) {
        return of([tiendaNull, ...this.tiendas]);
      } else {
        return of(this.tiendas);
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
  setListaTiendas(tiendas: Tienda[]): void {
    this.tiendas = tiendas;
  }

  getFiltroColeccion(): FiltroColeccion | undefined {
    return this.filtroColeccion;
  }
  setFiltroColeccion(filtro: FiltroColeccion | undefined): void {
    this.filtroColeccion = filtro;
  }

  getFiltroHistorial(): FiltroHistorial | undefined {
    return this.filtroHistorial;
  }
  setFiltroHistorial(filtro: FiltroHistorial | undefined): void {
    this.filtroHistorial = filtro;
  }

  getFiltroJuego(): FiltroJuego | undefined {
    return this.filtroJuego;
  }
  setFiltroJuego(filtro: FiltroJuego | undefined): void {
    this.filtroJuego = filtro;
  }

  getFiltroRom(): FiltroRom | undefined {
    return this.filtroRom;
  }
  setFiltroRom(filtro: FiltroRom | undefined): void {
    this.filtroRom = filtro;
  }
}