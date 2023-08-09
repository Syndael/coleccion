import { Component, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Coleccion } from '../../models/coleccion.model';
import { Edicion } from '../../models/edicion.model';
import { Estado } from '../../models/estado.model';
import { Idioma } from '../../models/idioma.model';
import { Base } from '../../models/base.model';
import { Plataforma } from '../../models/plataforma.model';
import { Region } from '../../models/region.model';
import { Tienda } from '../../models/tienda.model';
import { TipoEstado } from '../../models/tipo-estado';
import { TipoBase } from '../../models/tipo-base.model';

import { FiltroBase } from '../../filters/base.filter';

import { BaseService } from '../../services/base.service';
import { ErrorService } from '../../services/error.service';
import { ColeccionService } from '../../services/coleccion.service';
import { FicheroService } from '../../services/fichero.service';
import { UtilService } from '../../services/util.service';
import { TipoFicheroEnum } from 'src/app/models/tipo-fichero.model';
import { DatoFichero } from 'src/app/models/fichero.model';

@Component({
  selector: 'app-coleccion-template',
  templateUrl: './coleccion-template.component.html'
})
export class ColeccionTemplateComponent {
  @ViewChild('facturaInput') facturaInput!: ElementRef<HTMLInputElement>;
  @ViewChild('fotoInput') fotoInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private coleccionService: ColeccionService,
    private ficheroService: FicheroService,
    private utilService: UtilService,
    private errorService: ErrorService,
    private baseService: BaseService
  ) { }

  private modoAlta: Boolean | undefined;
  coleccion: Coleccion = {
    id: undefined,
    base: undefined,
    edicion: undefined,
    plataforma: undefined,
    idioma: undefined,
    region: undefined,
    estado_general: undefined,
    estado_caja: undefined,
    fecha_compra: undefined,
    fecha_recibo: undefined,
    unidades: undefined,
    coste: undefined,
    tienda: undefined,
    notas: undefined,
    codigo: undefined
  };
  listaEdiciones: Edicion[] = [];
  listaEstadosGeneral: Estado[] = [];
  listaEstadosCaja: Estado[] = [];
  listaIdiomas: Idioma[] = [];
  listaBases: Base[] = [];
  listaPlataformas: Plataforma[] = [];
  listaRegiones: Region[] = [];
  listaTiendas: Tienda[] = [];
  listaTipos: TipoBase[] = [];

  facturas: DatoFichero[] = [];
  fotos: DatoFichero[] = [];

  edicionSeleccionada: number | undefined;
  estadoGeneralSeleccionado: number | undefined;
  estadoCajaSeleccionado: number | undefined;
  idiomaSeleccionado: number | undefined;
  baseSeleccionado: number | undefined;
  plataformaSeleccionada: number | undefined;
  regionSeleccionada: number | undefined;
  tiendaSeleccionada: number | undefined;
  tipoSeleccionado: number | undefined;

  facturaSeleccionada: File | null = null;
  fotoSeleccionada: File | null = null;

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.utilService.getListaEstados(TipoEstado.GENERAL, false).subscribe(estados => this.listaEstadosGeneral = estados);
      this.utilService.getListaEstados(TipoEstado.CAJAS, false).subscribe(estados => this.listaEstadosCaja = estados);
      this.utilService.getListaIdiomas(true).subscribe(idiomas => this.listaIdiomas = idiomas);
      this.utilService.getListaPlataformas(false).subscribe(plataformas => this.listaPlataformas = plataformas);
      this.utilService.getListaRegiones(true).subscribe(regiones => this.listaRegiones = regiones);
      this.utilService.getListaTiendas(true).subscribe(tiendas => this.listaTiendas = tiendas);
      this.utilService.getListaTiposBase(false).subscribe(tipo => this.listaTipos = tipo);

      const id = params['id'];
      if (id && id == "new") {
        this.modoAlta = true;
        this.facturas = [];
        this.fotos = [];
        this.listaEdiciones = [];
      } else if (id) {
        this.modoAlta = false;
        this.getColeccion(id);
        this.refreshFicheros(id);
      }
    });
  }

  hayFacturas(): boolean {
    return this.facturas.length > 0;
  }

  hayFotos(): boolean {
    return this.fotos.length > 0;
  }

  onFacturaSeleccionada(event: any) {
    this.facturaSeleccionada = event.target.files[0];
  }

  onFotoSeleccionada(event: any) {
    this.fotoSeleccionada = event.target.files[0];
  }

  subirFactura() {
    if (this.facturaSeleccionada && this.coleccion.id) {
      this.ficheroService.subirFichero(this.coleccion.id, TipoFicheroEnum.FACTURA, this.facturaSeleccionada).subscribe((fichero) => {
        this.facturaSeleccionada = null;
        this.addFichero(fichero);
        if (this.facturaInput) {
          this.facturaInput.nativeElement.value = '';
        }
      });
    }
  }

  subirFoto() {
    if (this.fotoSeleccionada && this.coleccion.id) {
      this.ficheroService.subirFichero(this.coleccion.id, TipoFicheroEnum.FOTO, this.fotoSeleccionada).subscribe((fichero) => {
        this.fotoSeleccionada = null;
        this.addFichero(fichero);
        if (this.fotoInput) {
          this.fotoInput.nativeElement.value = '';
        }
      });
    }
  }

  getColeccion(id: number): void {
    this.coleccionService.getColeccion(id).subscribe(coleccion => {
      this.coleccion = coleccion;
      this.estadoGeneralSeleccionado = this.coleccion.estado_general?.id;
      this.estadoCajaSeleccionado = this.coleccion.estado_caja?.id;
      this.idiomaSeleccionado = this.coleccion.idioma?.id;
      this.tipoSeleccionado = this.coleccion.base?.tipo_base?.id;
      this.baseSeleccionado = this.coleccion.base?.id;
      this.plataformaSeleccionada = this.coleccion.plataforma?.id;
      this.edicionSeleccionada = this.coleccion.edicion?.id;
      this.regionSeleccionada = this.coleccion.region?.id;
      this.tiendaSeleccionada = this.coleccion.tienda?.id;
      this.baseSeleccionado = this.coleccion.base?.id;
      this.refreshBases();
      this.refreshEdiciones();
    });
  }

  eliminarFichero(id: number | undefined): void {
    if (id) {
      this.ficheroService.eliminarFichero(id).subscribe(() => {
        let indexFactura = this.facturas.findIndex((objeto) => objeto.id === id);
        let indexFoto = this.fotos.findIndex((objeto) => objeto.id === id);
        if (indexFactura !== -1) {
          this.facturas.splice(indexFactura, 1);
        } else if (indexFoto !== -1) {
          this.fotos.splice(indexFoto, 1);
        }
      });
    }
  }

  refreshFicheros(id: number): void {
    this.ficheroService.getDatosFichero(id).subscribe(datos => {
      datos.forEach((dato) => {
        this.addFichero(dato);
      });
    })
  }

  refreshEdiciones(): void {
    this.listaEdiciones = [];
    if (this.baseSeleccionado) {
      const edicionNull: Edicion = {
        id: undefined,
        base: undefined,
        plataforma: undefined,
        nombre: undefined,
        fecha: undefined
      }

      this.listaEdiciones.push(edicionNull);
      this.baseService.getEdiciones(this.baseSeleccionado).subscribe(datos => {
        datos.forEach((dato) => {
          this.listaEdiciones.push(dato);
        });
      });
    }
  }

  refreshBases(): void {
    this.listaBases = [];
    if (this.tipoSeleccionado && this.plataformaSeleccionada) {
      let filtro: FiltroBase = {
        id: undefined,
        tipo: this.tipoSeleccionado,
        tipoDescripcion: undefined,
        nombre: undefined,
        saga: undefined,
        plataforma: this.plataformaSeleccionada
      };
      this.baseService.getBases(filtro, true).subscribe((bases) => {
        this.listaBases = bases;
      });
    }
  }

  hayEdiciones(): boolean {
    return this.listaEstadosGeneral.length > 0;
  }

  addFichero(dato: DatoFichero) {
    let url = this.utilService.buildUrlFichero(dato.id);
    if (url && dato.tipo_fichero == TipoFicheroEnum.FOTO) {
      dato.url = url;
      this.fotos.push(dato);
    } else if (url && dato.tipo_fichero == TipoFicheroEnum.FACTURA) {
      dato.url = url;
      this.facturas.push(dato);
    }
  }

  save(): void {
    if (this.coleccion) {
      this.coleccion.estado_general = this.listaEstadosGeneral.find((estado) => estado.id === Number(this.estadoGeneralSeleccionado));
      this.coleccion.estado_caja = this.listaEstadosCaja.find((estado) => estado.id === Number(this.estadoCajaSeleccionado));
      this.coleccion.idioma = this.listaIdiomas.find((idioma) => idioma.id === Number(this.idiomaSeleccionado));
      this.coleccion.base = this.listaBases.find((base) => base.id === Number(this.baseSeleccionado));
      this.coleccion.plataforma = this.listaPlataformas.find((plataforma) => plataforma.id === Number(this.plataformaSeleccionada));
      this.coleccion.region = this.listaRegiones.find((region) => region.id === Number(this.regionSeleccionada));
      this.coleccion.tienda = this.listaTiendas.find((tienda) => tienda.id === Number(this.tiendaSeleccionada));
      this.coleccion.edicion = this.listaEdiciones.find((edicion) => edicion.id === Number(this.edicionSeleccionada));

      if (
        this.baseSeleccionado == undefined || this.coleccion.base == undefined ||
        this.plataformaSeleccionada == undefined || this.coleccion.plataforma == undefined ||
        this.estadoGeneralSeleccionado == undefined || this.coleccion.estado_general == undefined ||
        this.estadoCajaSeleccionado == undefined || this.coleccion.estado_caja == undefined
      ) {
        this.errorService.printError('Plataforma, base y estados deben estar rellenos');
      }
      else if (this.modoAlta) {
        this.coleccionService.addColeccion(this.coleccion).subscribe(() => this.back());
      } else {
        this.coleccionService.updateColeccion(this.coleccion).subscribe(() => this.back());
      }
    }
  }

  back(): void {
    this.location.back();
  }
}
