import { Component, OnInit } from '@angular/core';

import { Estado } from '../../models/estado.model';
import { Historial } from '../../models/historial.model';
import { Plataforma } from '../../models/plataforma.model';
import { TipoEstado } from '../../models/tipo-estado';

import { FiltroHistorial } from '../../filters/historial.filter';

import { HistorialService } from '../../services/historial.service';
import { UtilService } from '../../services/util.service';

@Component({
  selector: 'app-historial',
  templateUrl: './historial.component.html'
})

export class HistorialComponent implements OnInit {
  constructor(
    private historialService: HistorialService,
    private utilService: UtilService
  ) { }
  listaEstados: Estado[] = [];
  listaPlataformas: Plataforma[] = [];

  filtro: FiltroHistorial = this.getFiltroVacio();

  ngOnInit(): void {
    this.utilService.getListaEstados(TipoEstado.HISTORIAL, true).subscribe(estados => this.listaEstados = estados);
    this.utilService.getListaPlataformas(true).subscribe(plataformas => this.listaPlataformas = plataformas);

    let filtro = this.utilService.getFiltroHistorial();
    if (filtro) {
      this.filtro = filtro;
    }

    this.getHistoriales();
  }

  historiales: Historial[] = [];

  setHistorial?: Historial;
  onSelect(historial: Historial): void {
    this.setHistorial = historial;
  }

  getFiltroVacio(): FiltroHistorial {
    return {
      idHistorial: undefined,
      plataformaSeleccionada: undefined,
      nombreJuego: undefined,
      sagaJuego: undefined,
      estadoSeleccionado: undefined
    };
  }

  limpiarFiltro(): void {
    this.filtro = this.getFiltroVacio();
    this.getHistoriales();
  }

  getHistoriales(): void {
    this.utilService.setFiltroHistorial(this.filtro);
    this.historialService.getHistoriales(this.filtro).subscribe(historiales => this.historiales = historiales);
  }
}