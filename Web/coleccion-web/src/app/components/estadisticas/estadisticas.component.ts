import { Component, OnInit } from '@angular/core';

import { Completo, Gasto, TipoGasto } from '../../models/estadistica.model';
import { Progreso } from '../../models/progreso.model';

import { EstadisticasService } from '../../services/estadisticas.service';
import { ProgresoService } from '../../services/progreso.service';

@Component({
  selector: 'app-estadisticas',
  templateUrl: './estadisticas.component.html'
})

export class EstadisticasComponent implements OnInit {
  constructor(
    private estadisticasService: EstadisticasService,
    private progresoService: ProgresoService
  ) { }

  ngOnInit(): void {
    this.getCompletos();
    this.getGastos();
    this.getUltimosProgresos();
  }

  completos: Completo[] = [];
  gastosJuegosMes: Gasto[] = [];
  gastosJuegosPlataforma: Gasto[] = [];
  gastosJuegosTienda: Gasto[] = [];
  gastosTotales: Gasto[] = [];
  romsPlataforma: Gasto[] = [];
  ultimosProgresos: Progreso[] = [];

  getCompletos(): void {
    this.estadisticasService.getCompletos().subscribe(completos => this.completos = this.ordenarCompletos(completos));
  }

  getGastos(): void {
    this.estadisticasService.getGastos().subscribe(gastos => {
      this.gastosJuegosMes = this.ordenarGastos(gastos.filter(gasto => gasto.tipo === TipoGasto.JUEGOS_MES)).slice(0, 11);
      this.gastosTotales = this.ordenarGastos(gastos.filter(gasto => gasto.tipo === TipoGasto.TOTAL));
      this.gastosJuegosPlataforma = this.ordenarGastos(gastos.filter(gasto => gasto.tipo === TipoGasto.JUEGOS_PLATAFORMA));
      this.gastosJuegosTienda = this.ordenarGastos(gastos.filter(gasto => gasto.tipo === TipoGasto.JUEGOS_TIENDA));
      this.romsPlataforma = this.ordenarGastos(gastos.filter(gasto => gasto.tipo === TipoGasto.ROMS_PLATAFORMA));
    });
  }

  getUltimosProgresos(): void {
    this.progresoService.getUltimosProgresos().subscribe(progresos => this.ultimosProgresos = progresos);
  }

  ordenarCompletos(completos: Completo[]): Completo[] {
    return completos.sort((a, b) => {
      let res: number = 0;
      if (a.orden_desc) {
        res = a.orden_desc < (b.orden_desc ? b.orden_desc : - 1) ? 1 : -1;
      }
      return res;
    });
  }

  ordenarGastos(gastos: Gasto[]): Gasto[] {
    return gastos.sort((a, b) => {
      let res: number = 0;
      if (a.orden_desc || a.orden_asc) {
        if (a.orden_desc) {
          res = a.orden_desc < (b.orden_desc ? b.orden_desc : - 1) ? 1 : -1;
        } else if (a.orden_asc) {
          res = a.orden_asc > (b.orden_asc ? b.orden_asc : - 1) ? 1 : -1;
        }
      }
      return res;
    });
  }

}
