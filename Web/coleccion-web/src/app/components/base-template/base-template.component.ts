import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Base } from '../../models/base.model';
import { BaseDlc } from '../../models/base-dlc.model';
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
    url: undefined,
    fecha_salida: undefined,
    plataformas: undefined
  };
  listaBasesPlataforma: BasePlataforma[] = [];
  listaBasesDlc: BaseDlc[] = [];
  listaEdiciones: Edicion[] = [];
  listaPlataformas: Plataforma[] = [];
  listaTipos: TipoBase[] = [];

  tipoSeleccionado: number | undefined;

  plataformaFechaSeleccionada: string | undefined;
  plataformaSeleccionada: number | undefined;

  edicionNombreSeleccionado: string | undefined;
  edicionFechaSeleccionada: string | undefined;
  edicionPlataformaSeleccionada: number | undefined;

  dlcNombreSeleccionado: string | undefined;

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

  goUrl(url: string | undefined) {
    this.utilService.goUrl(url);
  }

  urlValida(url: string | undefined): boolean {
    return this.utilService.urlValida(url);
  }

  urlVandalValida(url: string | undefined): boolean {
    try {
      if (url) {
        const urlObject = new URL(url);
        this.base.url = `${urlObject.protocol}//${urlObject.host}${urlObject.pathname}`;
        return `${urlObject.host}`.includes('vandal')
      }
    } catch (e) {
      console.error('Invalid URL');
    }
    return false;
  }

  rellenarDatosVandal(url: string | undefined): void {
    try {
      if (url) {
        const urlObject = new URL(url);
        this.base.url = `${urlObject.protocol}//${urlObject.host}${urlObject.pathname}`;
        if (`${urlObject.host}`.includes('vandal'))
          this.baseService.getValoresVandal(url).subscribe(base => {
            if(!this.base.nombre){
              this.base.nombre = base.nombre
            }
            if(!this.base.fecha_salida){
              this.base.fecha_salida = base.fecha_salida
            }
          });
      }
    } catch (e) {
      console.error('Invalid URL');
    }
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

  addBaseDlc(): void {
    this.baseService.addBaseDlc(this.base.id, this.dlcNombreSeleccionado).subscribe(() => this.refreshBase(this.base.id));
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

  deleteBaseDlc(id: number | undefined): void {
    if (id) {
      this.baseService.deleteBaseDlc(id).subscribe(() => this.refreshBase(this.base.id));
    } else {
      this.errorService.printError("Error eliminando la base, no tiene id");
    }
  }

  refreshBase(id: number | undefined): void {
    this.listaBasesPlataforma = [];
    this.listaEdiciones = [];
    this.listaBasesDlc = [];

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
      this.baseService.getBasesDlc(id, false).subscribe(datos => {
        datos.forEach((dato) => {
          this.listaBasesDlc.push(dato);
        });
      });
    } else {
      this.errorService.printError("Error refrescando los datos de la base, no tiene id");
    }
  }

  save(auto: boolean): void {
    if (this.base) {
      console.info(this.tipoSeleccionado)
      console.info(this.listaTipos.find((tipo) => tipo.id == this.tipoSeleccionado))
      console.info(this.base.tipo_base)
      this.base.tipo_base = this.listaTipos.find((tipo) => tipo.id == this.tipoSeleccionado);
      console.info(this.base.tipo_base)

      if (
        this.tipoSeleccionado == undefined || this.base.tipo_base == undefined ||
        this.base.nombre == undefined
      ) {
        if (auto == false) {
          this.errorService.printError('Tipo y nombre deben estar rellenos');
        }
      } else if (this.modoAlta) {
        this.modoAlta = false;
        this.baseService.addBase(this.base).subscribe((base) => this.modoModificacion(base.id));
      } else {
        this.baseService.updateBase(this.base).subscribe(() => {
          if (auto == false) {
            this.back();
          }
        });
      }
    }
  }

  delete(): void {
    if (this.base.id == undefined) {
      this.errorService.printError('La base no se ha genereado aún');
    } else {
      const confirmacion = window.confirm('¿Eliminar la base?');
      if (confirmacion) {
        this.baseService.deleteBase(this.base.id).subscribe((res) => {
          if (res.success) {
            this.back();
          } else {
            this.errorService.printError('Se ha producido un error eliminando la base ' + this.base.id);
          }
        });
      }
    }
  }

  back(): void {
    this.location.back();
  }
}
