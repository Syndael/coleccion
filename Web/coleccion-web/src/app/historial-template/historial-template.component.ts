import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Estado } from '../models/estado.model';
import { Historial } from '../models/historial.model';
import { Juego } from '../models/juego.model';
import { Plataforma } from '../models/plataforma.model';
import { TipoEstado } from '../models/tipo-estado';

import { ErrorService } from '../services/error.service';
import { HistorialService } from '../services/historial.service';
import { UtilService } from '../services/util.service';

@Component({
  selector: 'app-historial-template',
  templateUrl: './historial-template.component.html'
})
export class HistorialTemplateComponent {
  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private historialService: HistorialService,
    private utilService: UtilService,
    private errorService: ErrorService
  ) { }

  private modoAlta: Boolean | undefined;
  historial: Historial = {
    id: undefined,
    juego: undefined,
    plataforma: undefined,
    estado_jugado: undefined,
    porcentaje: undefined,
    horas: undefined,
    historia_completa: undefined,
    notas: undefined,
    fecha_inicio: undefined,
    fecha_fin: undefined
  };
  listaEstados: Estado[] = [];
  listaJuegos: Juego[] = [];
  listaPlataformas: Plataforma[] = [];

  estadoSeleccionado: number | undefined;
  juegoSeleccionado: number | undefined;
  plataformaSeleccionada: number | undefined;

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.utilService.getListaEstados(TipoEstado.HISTORIAL, false).subscribe(estados => this.listaEstados = estados);
      this.utilService.getListaJuegos().subscribe(juegos => this.listaJuegos = juegos);
      this.utilService.getListaPlataformas().subscribe(plataformas => this.listaPlataformas = plataformas);

      const id = params['id'];
      if (id && id == "new") {
        this.modoAlta = true;
      } else if (id) {
        this.modoAlta = false;
        this.getHistorial(id);
      }
    });
  }

  getHistorial(id: number): void {
    this.historialService.getHistorial(id).subscribe(historial => {
      this.historial = historial;
      this.estadoSeleccionado = this.historial.estado_jugado?.id;
      this.juegoSeleccionado = this.historial.juego?.id;
      this.plataformaSeleccionada = this.historial.plataforma?.id;

      this.historial.horas = this.utilService.formatNumber(this.historial.horas);
    });
  }

  save(): void {
    if (this.historial) {
      this.historial.estado_jugado = this.listaEstados.find((estado) => estado.id === Number(this.estadoSeleccionado));
      this.historial.juego = this.listaJuegos.find((juego) => juego.id === Number(this.juegoSeleccionado));
      this.historial.plataforma = this.listaPlataformas.find((plataforma) => plataforma.id === Number(this.plataformaSeleccionada));

      if (this.juegoSeleccionado == undefined || this.historial.juego == undefined || this.plataformaSeleccionada == undefined || this.historial.plataforma == undefined) {
        this.errorService.printError('Plataforma y juego deben estar rellenos');
      }
      else if (this.modoAlta) {
        this.historialService.addHistorial(this.historial).subscribe(() => this.back());
      } else {
        this.historialService.updateHistorial(this.historial).subscribe(() => this.back());
      }
    }
  }

  formatHoras(event: any) {
    this.historial.horas = this.utilService.formatNumber(event.target.value);
  }

  back(): void {
    this.location.back();
  }
}
