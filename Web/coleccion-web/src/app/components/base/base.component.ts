import { Component, OnInit } from '@angular/core';

import { Base } from '../../models/base.model';
import { Plataforma } from '../../models/plataforma.model';
import { TipoBase } from '../../models/tipo-base.model';

import { FiltroBase } from '../../filters/base.filter';

import { BaseService } from '../../services/base.service';
import { UtilService } from '../../services/util.service';

@Component({
  selector: 'app-bases',
  templateUrl: './base.component.html'
})

export class BaseComponent implements OnInit {
  constructor(
    private baseService: BaseService,
    private utilService: UtilService
  ) { }
  listaTipos: TipoBase[] = [];
  listaPlataformas: Plataforma[] = [];
  tipoSeleccionado: number | undefined;

  filtro: FiltroBase = this.getFiltroVacio();

  ngOnInit(): void {
    this.utilService.getListaPlataformas(true).subscribe(plataformas => this.listaPlataformas = plataformas);
    this.utilService.getListaTiposBase(true).subscribe(tipos => this.listaTipos = tipos);

    let filtro = this.utilService.getFiltroBase();
    if (filtro) {
      this.filtro = filtro;
    }
    this.getBases();
  }
  
  bases: Base[] = [];

  setBase?: Base;
  onSelect(base: Base): void {
    this.setBase = base;
  }

  getFiltroVacio(): FiltroBase {
    return {
      id: undefined,
      tipo: undefined,
      tipoDescripcion: undefined,
      nombre: undefined,
      saga: undefined,
      plataforma: undefined,
      ordenSeleccionado: undefined
    };
  }

  limpiarFiltro(): void {
    this.filtro = this.getFiltroVacio();
    this.getBases();
  }

  getBases(): void {
    this.utilService.setFiltroBase(this.filtro);
    this.baseService.getBases(this.filtro, false).subscribe(bases => { this.bases = bases; });
  }
}