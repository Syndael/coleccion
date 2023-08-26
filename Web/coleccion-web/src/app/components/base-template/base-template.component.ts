import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Base } from '../../models/base.model';
import { BasePlataforma } from '../../models/base-plataforma.model';
import { Edicion } from '../../models/edicion.model';
import { Plataforma } from '../../models/plataforma.model';
import { TipoBase } from '../../models/tipo-base.model';

import { BaseService } from '../../services/base.service';
import { ErrorService } from '../../services/error.service';
import { UtilService } from '../../services/util.service';

@Component({
  selector: 'app-base-template',
  templateUrl: './base-template.component.html'
})
export class BaseTemplateComponent {
  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private baseService: BaseService,
    private errorService: ErrorService,
    private utilService: UtilService
  ) { }

  private modoAlta: Boolean | undefined;
  base: Base = {
    id: undefined,
    tipo_base: undefined,
    nombre: undefined,
    codigo: undefined,
    saga: undefined,
    fecha_salida: undefined,
    plataformas: undefined
  };
  listaBasesPlataforma: BasePlataforma[] = [];
  listaEdiciones: Edicion[] = [];
  listaPlataformas: Plataforma[] = [];
  listaTipos: TipoBase[] = [];

  tipoSeleccionado: number | undefined;

  plataformaFechaSeleccionada: string | undefined;
  plataformaSeleccionada: number | undefined;

  edicionNombreSeleccionado: string | undefined;
  edicionFechaSeleccionada: string | undefined;
  edicionPlataformaSeleccionada: number | undefined;

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.utilService.getListaPlataformas(true).subscribe(plataformas => this.listaPlataformas = plataformas);
      this.utilService.getListaTiposBase(true).subscribe(tipo => this.listaTipos = tipo);

      const id = params['id'];
      if (id && id == "new") {
        this.modoAlta = true;
        this.listaBasesPlataforma = [];
      } else if (id) {
        this.modoModificacion(id);
      }
    });
  }

  modoModificacion(id: number): void {
    this.modoAlta = false;
    this.getBase(id);
    this.refreshBase(id);
  }

  getBase(id: number): void {
    this.baseService.getBase(id).subscribe(base => {
      this.base = base;
      this.tipoSeleccionado = this.base.tipo_base?.id;
    });
  }

  addBasePlataforma(): void {
    this.baseService.addBasePlataforma(this.base.id, this.plataformaSeleccionada, this.plataformaFechaSeleccionada).subscribe(() => this.refreshBase(this.base.id));
  }

  addEdicion(): void {
    this.baseService.addEdicion(this.base.id, this.edicionPlataformaSeleccionada, this.edicionNombreSeleccionado, this.edicionFechaSeleccionada).subscribe(() => this.refreshBase(this.base.id));
  }

  deleteBasePlataforma(id: number | undefined): void {
    if (id) {
      this.baseService.deleteBasePlataforma(id).subscribe(() => this.refreshBase(this.base.id));
    } else {
      this.errorService.printError("Error eliminando la base, no tiene id");
    }
  }

  deleteEdicion(id: number | undefined): void {
    if (id) {
      this.baseService.deleteEdicion(id).subscribe(() => this.refreshBase(this.base.id));
    } else {
      this.errorService.printError("Error eliminando la base, no tiene id");
    }
  }

  refreshBase(id: number | undefined): void {
    this.listaBasesPlataforma = [];
    this.listaEdiciones = [];

    if (id) {
      this.baseService.getBasesPlataforma(id).subscribe(datos => {
        datos.forEach((dato) => {
          this.listaBasesPlataforma.push(dato);
        });
      });
      this.baseService.getEdiciones(id).subscribe(datos => {
        datos.forEach((dato) => {
          this.listaEdiciones.push(dato);
        });
      });
    } else {
      this.errorService.printError("Error refrescando los datos de la base, no tiene id");
    }
  }

  save(): void {
    if (this.base) {
      console.info(this.tipoSeleccionado)
      console.info(this.listaTipos.find((tipo) => tipo.id == this.tipoSeleccionado))
      console.info(this.base.tipo_base)
      this.base.tipo_base = this.listaTipos.find((tipo) => tipo.id == this.tipoSeleccionado);
      console.info(this.base.tipo_base)
      if (this.modoAlta) {
        this.baseService.addBase(this.base).subscribe((base) => this.modoModificacion(base.id));
      } else {
        this.baseService.updateBase(this.base).subscribe(() => this.back());
      }
    }
  }

  back(): void {
    this.location.back();
  }
}
