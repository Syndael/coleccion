import { Component, OnInit } from '@angular/core';

import { Coleccion } from '../../models/coleccion.model';
import { Estado, TipoEstado } from '../../models/estado.model';
import { Plataforma } from '../../models/plataforma.model';
import { Tienda } from '../../models/tienda.model';
import { TipoBase } from '../../models/tipo-base.model';

import { FiltroColeccion, OrdenEnum } from '../../filters/coleccion.filter';

import { ColeccionService } from '../../services/coleccion.service';
import { UtilService } from '../../services/util.service';

@Component({
  selector: 'app-coleccion',
  templateUrl: './coleccion.component.html'
})

export class ColeccionComponent implements OnInit {
  constructor(
    private coleccionService: ColeccionService,
    private utilService: UtilService
  ) { }
  listaEstadosGeneral: Estado[] = [];
  listaPlataformas: Plataforma[] = [];
  listaTiendas: Tienda[] = [];
  listaTipos: TipoBase[] = [];
  listaOrdenes: string[] = Object.values(OrdenEnum);

  filtro: FiltroColeccion = this.getFiltroVacio();

  ngOnInit(): void {
    this.utilService.getListaEstados(TipoEstado.GENERAL, true).subscribe(estados => this.listaEstadosGeneral = estados);
    this.utilService.getListaPlataformas(true).subscribe(plataformas => this.listaPlataformas = plataformas);
    this.utilService.getListaTiendas(true).subscribe(tiendas => this.listaTiendas = tiendas);
    this.utilService.getListaTiposBase(true).subscribe(tipos => this.listaTipos = tipos);

    let filtro = this.utilService.getFiltroColeccion();
    if (filtro) {
      this.filtro = filtro;
    }

    this.getColecciones();
  }

  colecciones: Coleccion[] = [];

  setColeccion?: Coleccion;
  onSelect(coleccion: Coleccion): void {
    this.setColeccion = coleccion;
  }

  goUrl(url: string | undefined) {
    this.utilService.goUrl(url);
  }

  getMascara(i: number, tipo: string | undefined, mascara: string | undefined) {
    return this.utilService.getMascara(i, tipo, mascara);
  }

  urlValida(url: string | undefined): boolean {
    return this.utilService.urlValida(url);
  }

  getFiltroVacio(): FiltroColeccion {
    return {
      idColeccion: undefined,
      tipo: undefined,
      estadoGeneralSeleccionado: undefined,
      plataformaSeleccionada: undefined,
      nombreBase: undefined,
      saga: undefined,
      tiendaSeleccionada: undefined,
      ordenSeleccionado: OrdenEnum.POKEMON
    };
  }

  limpiarFiltro(): void {
    this.filtro = this.getFiltroVacio();
    this.filtro.ordenSeleccionado = undefined,
      this.getColecciones();
  }

  getColecciones(): void {
    this.utilService.setFiltroColeccion(this.filtro);
    this.coleccionService.getColecciones(this.filtro).subscribe(colecciones => this.colecciones = colecciones);
  }
}