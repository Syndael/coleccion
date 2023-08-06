import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Estado } from '../../models/estado.model';
import { Progreso } from '../../models/progreso.model';
import { Base } from '../../models/base.model';
import { Plataforma } from '../../models/plataforma.model';
import { TipoEstado } from '../../models/tipo-estado';

import { ErrorService } from '../../services/error.service';
import { ProgresoService } from '../../services/progreso.service';
import { UtilService } from '../../services/util.service';

@Component({
  selector: 'app-progreso-template',
  templateUrl: './progreso-template.component.html'
})
export class ProgresoTemplateComponent {
  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private progresoService: ProgresoService,
    private utilService: UtilService,
    private errorService: ErrorService
  ) { }

  private modoAlta: Boolean | undefined;
  progreso: Progreso = {
    id: undefined,
    base: undefined,
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
  listaBases: Base[] = [];
  listaPlataformas: Plataforma[] = [];

  estadoSeleccionado: number | undefined;
  baseSeleccionado: number | undefined;
  plataformaSeleccionada: number | undefined;

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.utilService.getListaEstados(TipoEstado.PROGRESO, false).subscribe(estados => this.listaEstados = estados);
      this.utilService.getListaBases().subscribe(bases => this.listaBases = bases);
      this.utilService.getListaPlataformas(false).subscribe(plataformas => this.listaPlataformas = plataformas);

      const id = params['id'];
      if (id && id == "new") {
        this.modoAlta = true;
      } else if (id) {
        this.modoAlta = false;
        this.getProgreso(id);
      }
    });
  }

  getProgreso(id: number): void {
    this.progresoService.getProgreso(id).subscribe(progreso => {
      this.progreso = progreso;
      this.estadoSeleccionado = this.progreso.estado_jugado?.id;
      this.baseSeleccionado = this.progreso.base?.id;
      this.plataformaSeleccionada = this.progreso.plataforma?.id;

      this.progreso.horas = this.utilService.formatNumber(this.progreso.horas);
    });
  }

  save(): void {
    if (this.progreso) {
      this.progreso.estado_jugado = this.listaEstados.find((estado) => estado.id === Number(this.estadoSeleccionado));
      this.progreso.base = this.listaBases.find((base) => base.id === Number(this.baseSeleccionado));
      this.progreso.plataforma = this.listaPlataformas.find((plataforma) => plataforma.id === Number(this.plataformaSeleccionada));

      if (this.baseSeleccionado == undefined || this.progreso.base == undefined || this.plataformaSeleccionada == undefined || this.progreso.plataforma == undefined) {
        this.errorService.printError('Plataforma y base deben estar rellenos');
      }
      else if (this.modoAlta) {
        this.progresoService.addProgreso(this.progreso).subscribe(() => this.back());
      } else {
        this.progresoService.updateProgreso(this.progreso).subscribe(() => this.back());
      }
    }
  }

  formatHoras(event: any) {
    this.progreso.horas = this.utilService.formatNumber(event.target.value);
  }

  back(): void {
    this.location.back();
  }
}
