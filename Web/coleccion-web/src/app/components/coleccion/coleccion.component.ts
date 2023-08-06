import { Component, OnInit } from '@angular/core';

import { Coleccion } from '../../models/coleccion.model';
import { Estado } from '../../models/estado.model';
import { Plataforma } from '../../models/plataforma.model';
import { Tienda } from '../../models/tienda.model';
import { TipoEstado } from '../../models/tipo-estado';

import { FiltroColeccion } from '../../filters/coleccion.filter';

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

  filtro: FiltroColeccion = this.getFiltroVacio();

  ngOnInit(): void {
    this.utilService.getListaEstados(TipoEstado.GENERAL, true).subscribe(estados => this.listaEstadosGeneral = estados);
    this.utilService.getListaPlataformas(true).subscribe(plataformas => this.listaPlataformas = plataformas);
    this.utilService.getListaTiendas(true).subscribe(tiendas => this.listaTiendas = tiendas);

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

  getFiltroVacio(): FiltroColeccion {
    return {
      idColeccion: undefined,
      estadoGeneralSeleccionado: undefined,
      plataformaSeleccionada: undefined,
      nombreBase: undefined,
      saga: undefined,
      tiendaSeleccionada: undefined
    };
  }

  limpiarFiltro(): void {
    this.filtro = this.getFiltroVacio();
    this.getColecciones();
  }

  getColecciones(): void {
    this.utilService.setFiltroColeccion(this.filtro);
    this.coleccionService.getColecciones(this.filtro).subscribe(colecciones => this.colecciones = colecciones);
  }
}