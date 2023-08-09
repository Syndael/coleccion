import { Component, OnInit } from '@angular/core';

import { Base } from '../../models/base.model';
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

  ngOnInit(): void {
    let filtro = this.utilService.getFiltroBase();
    if (filtro) {
      this.filtro = filtro;
    }
    this.utilService.getListaTiposBase(true).subscribe(tipos => this.listaTipos = tipos);
    this.getBases();
  }

  filtro: FiltroBase = this.getFiltroVacio();

  bases: Base[] = [];
  listaTipos: TipoBase[] = [];
  tipoSeleccionado: number | undefined;

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
      plataforma: undefined
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