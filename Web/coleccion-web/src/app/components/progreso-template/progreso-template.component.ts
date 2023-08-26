import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Estado } from '../../models/estado.model';
import { Progreso } from '../../models/progreso.model';
import { Base } from '../../models/base.model';
import { Plataforma } from '../../models/plataforma.model';
import { TipoEstado } from '../../models/tipo-estado';

import { FiltroBase } from '../../filters/base.filter';

import { BaseService } from '../../services/base.service';
import { DatoFichero } from 'src/app/models/fichero.model';
import { ErrorService } from '../../services/error.service';
import { FicheroService } from '../../services/fichero.service';
import { ProgresoService } from '../../services/progreso.service';
import { UtilService } from '../../services/util.service';
import { TipoBaseEnum } from 'src/app/models/tipo-base.model';
import { TipoFicheroEnum } from 'src/app/models/tipo-fichero.model';

@Component({
  selector: 'app-progreso-template',
  templateUrl: './progreso-template.component.html'
})
export class ProgresoTemplateComponent {
  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private baseService: BaseService,
    private errorService: ErrorService,
    private ficheroService: FicheroService,
    private progresoService: ProgresoService,
    private utilService: UtilService
  ) { }

  private modoAlta: Boolean | undefined;
  progreso: Progreso = {
    id: undefined,
    base: undefined,
    plataforma: undefined,
    estado_progreso: undefined,
    porcentaje: undefined,
    horas: undefined,
    historia_completa: undefined,
    notas: undefined,
    fecha_inicio: undefined,
    fecha_fin: undefined,
    fecha_ultimo: undefined
  };
  listaEstados: Estado[] = [];
  listaBases: Base[] = [];
  listaPlataformas: Plataforma[] = [];

  fotos: DatoFichero[] = [];

  estadoSeleccionado: number | undefined;
  baseSeleccionado: number | undefined;
  plataformaSeleccionada: number | undefined;

  fotosSeleccionadas: File[] | undefined;
  strFotosSeleccionadas: string | undefined;
  subiendoFotos: boolean = false;

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.utilService.getListaEstados(TipoEstado.PROGRESO, false).subscribe(estados => this.listaEstados = estados);
      this.utilService.getListaPlataformas(false).subscribe(plataformas => this.listaPlataformas = plataformas);

      const id = params['id'];
      if (id && id == "new") {
        this.modoAlta = true;
        this.fotos = [];
      } else if (id) {
        this.modoAlta = false;
        this.getProgreso(id);
      }
    });
  }

  modoModificacion(id: number): void {
    this.modoAlta = false;
    this.getProgreso(id);
    this.refreshFicheros(id);
  }

  hayFotos(): boolean {
    return this.fotos.length > 0;
  }

  onFotosSeleccionadas(event: any) {
    const fotos: FileList = event.target.files;
    if (fotos.length > 0) {
      this.fotosSeleccionadas = [];
      for (let i = 0; i < fotos.length; i++) {
        const foto: File = fotos[i];
        this.fotosSeleccionadas.push(foto);
      }
    } else {
      this.fotosSeleccionadas = undefined;
    }
    this.strFotosSeleccionadas = this.fotosSeleccionadas?.map(file => file.name).join(', ');
  }

  subirFoto() {
    if (this.fotosSeleccionadas && this.progreso.id) {
      for (let i = 0; i < this.fotosSeleccionadas.length; i++) {
        this.subiendoFotos = true;
        const foto: File = this.fotosSeleccionadas[i];
        this.ficheroService.subirFicheroProgreso(this.progreso.id, TipoFicheroEnum.FOTO, foto).subscribe((fichero) => {
          this.addFichero(fichero);
          if (this.fotosSeleccionadas != undefined && i == this.fotosSeleccionadas.length - 1) {
            this.fotosSeleccionadas = undefined;
            this.strFotosSeleccionadas = '';
            this.subiendoFotos = false;
          }
        });
      }
    }
  }

  addFichero(dato: DatoFichero) {
    let url = this.utilService.buildUrlFichero(dato.id);
    if (url && dato.tipo_fichero == TipoFicheroEnum.FOTO) {
      dato.url = url;
      this.fotos.push(dato);
    }
  }

  getProgreso(id: number): void {
    this.progresoService.getProgreso(id).subscribe(progreso => {
      this.progreso = progreso;
      this.estadoSeleccionado = this.progreso.estado_progreso?.id;
      this.baseSeleccionado = this.progreso.base?.id;
      this.plataformaSeleccionada = this.progreso.plataforma?.id;

      this.progreso.horas = this.utilService.formatNumber(this.progreso.horas);
      this.refreshBases();
      this.refreshFicheros(id);
    });
  }

  eliminarFichero(id: number | undefined): void {
    if (id) {
      this.ficheroService.eliminarFichero(id).subscribe(() => {
        let indexFoto = this.fotos.findIndex((objeto) => objeto.id === id);
        if (indexFoto !== -1) {
          this.fotos.splice(indexFoto, 1);
        }
      });
    }
  }

  refreshFicheros(id: number): void {
    this.ficheroService.getDatosFicheroProgreso(id).subscribe(datos => {
      datos.forEach((dato) => {
        this.addFichero(dato);
      });
    })
  }

  refreshBases(): void {
    if (this.plataformaSeleccionada) {
      let filtro: FiltroBase = {
        id: undefined,
        tipo: undefined,
        tipoDescripcion: TipoBaseEnum.JUEGO,
        nombre: undefined,
        saga: undefined,
        plataforma: this.plataformaSeleccionada
      };
      this.baseService.getBases(filtro, true).subscribe((bases) => this.listaBases = bases);
    }
  }

  save(): void {
    if (this.progreso) {
      this.progreso.estado_progreso = this.listaEstados.find((estado) => estado.id === Number(this.estadoSeleccionado));
      this.progreso.base = this.listaBases.find((base) => base.id === Number(this.baseSeleccionado));
      this.progreso.plataforma = this.listaPlataformas.find((plataforma) => plataforma.id === Number(this.plataformaSeleccionada));

      if (this.baseSeleccionado == undefined || this.progreso.base == undefined || this.plataformaSeleccionada == undefined || this.progreso.plataforma == undefined || this.estadoSeleccionado == undefined || this.progreso.estado_progreso == undefined) {
        this.errorService.printError('Plataforma, base y edtado deben estar rellenos');
      } else if (this.modoAlta) {
        this.progresoService.addProgreso(this.progreso).subscribe((pro) => this.modoModificacion(pro.id));
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
