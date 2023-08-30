import { Component, OnInit } from '@angular/core';

import { Estado, TipoEstado } from '../../models/estado.model';
import { Progreso } from '../../models/progreso.model';
import { Plataforma } from '../../models/plataforma.model';

import { FiltroProgreso } from '../../filters/progreso.filter';

import { ProgresoService } from '../../services/progreso.service';
import { UtilService } from '../../services/util.service';

@Component({
  selector: 'app-progreso',
  templateUrl: './progreso.component.html'
})

export class ProgresoComponent implements OnInit {
  constructor(
    private progresoService: ProgresoService,
    private utilService: UtilService
  ) { }
  listaEstados: Estado[] = [];
  listaPlataformas: Plataforma[] = [];

  filtro: FiltroProgreso = this.getFiltroVacio();

  ngOnInit(): void {
    this.utilService.getListaEstados(TipoEstado.PROGRESO, true).subscribe(estados => this.listaEstados = estados);
    this.utilService.getListaPlataformas(true).subscribe(plataformas => this.listaPlataformas = plataformas);

    let filtro = this.utilService.getFiltroProgreso();
    if (filtro) {
      this.filtro = filtro;
    }

    this.getProgresos();
  }

  progresos: Progreso[] = [];

  setProgreso?: Progreso;
  onSelect(progreso: Progreso): void {
    this.setProgreso = progreso;
  }

  getFiltroVacio(): FiltroProgreso {
    return {
      idProgreso: undefined,
      plataformaSeleccionada: undefined,
      nombreBase: undefined,
      saga: undefined,
      estadoSeleccionado: undefined
    };
  }

  limpiarFiltro(): void {
    this.filtro = this.getFiltroVacio();
    this.getProgresos();
  }

  getProgresos(): void {
    this.utilService.setFiltroProgreso(this.filtro);
    this.progresoService.getProgresos(this.filtro).subscribe(progresos => this.progresos = progresos);
  }
}