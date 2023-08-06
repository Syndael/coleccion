import { Component, OnInit } from '@angular/core';

import { Base } from '../../models/base.model';

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

  filtro: FiltroBase = this.getFiltroVacio();

  ngOnInit(): void {
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
      nombre: undefined,
      saga: undefined
    };
  }

  limpiarFiltro(): void {
    this.filtro = this.getFiltroVacio();
    this.getBases();
  }

  getBases(): void {
    this.utilService.setFiltroBase(this.filtro);
    this.baseService.getBases(this.filtro).subscribe(bases => { this.bases = bases; this.utilService.setListaBases(bases) });
  }
}