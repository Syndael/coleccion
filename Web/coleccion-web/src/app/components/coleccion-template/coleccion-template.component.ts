import { Component, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Coleccion } from '../../models/coleccion.model';
import { Edicion } from '../../models/edicion.model';
import { Estado, TipoEstado } from '../../models/estado.model';
import { Idioma } from '../../models/idioma.model';
import { Base } from '../../models/base.model';
import { Plataforma } from '../../models/plataforma.model';
import { Region } from '../../models/region.model';
import { Tienda } from '../../models/tienda.model';
import { TipoBase } from '../../models/tipo-base.model';

import { FiltroBase } from '../../filters/base.filter';

import { BaseService } from '../../services/base.service';
import { DatoFichero } from 'src/app/models/fichero.model';
import { ErrorService } from '../../services/error.service';
import { ColeccionService } from '../../services/coleccion.service';
import { FicheroService } from '../../services/fichero.service';
import { UtilService } from '../../services/util.service';
import { TipoFicheroEnum } from 'src/app/models/tipo-fichero.model';

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
    private baseService: BaseService,
    private coleccionService: ColeccionService,
    private errorService: ErrorService,
    private ficheroService: FicheroService,
    private utilService: UtilService
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
    fecha_reserva: undefined,
    fecha_compra: undefined,
    fecha_recibo: undefined,
    unidades: undefined,
    coste: undefined,
    tienda: undefined,
    url: undefined,
    notas: undefined,
    codigo: undefined,
    mascara_aux: undefined
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

  facturasSeleccionadas: File[] | undefined;
  strFacturasSeleccionadas: string | undefined;
  subiendoFacturas: boolean = false;

  fotosSeleccionadas: File[] | undefined;
  strFotosSeleccionadas: string | undefined;
  subiendoFotos: boolean = false;

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
        this.modoModificacion(id);
      }
    });
  }

  goUrlBase() {
    if (this.baseSeleccionado) {
      let base = this.listaBases.find(elemento => elemento.id === this.baseSeleccionado);
      this.utilService.goUrl(base?.url);
    }
  }

  urlValidaBase(): boolean {
    if (this.baseSeleccionado) {
      let base = this.listaBases.find(elemento => elemento.id === this.baseSeleccionado);
      return this.utilService.urlValida(base?.url);
    } else {
      return false;
    }
  }

  goUrl(url: string | undefined) {
    this.utilService.goUrl(url);
  }

  urlValida(url: string | undefined): boolean {
    return this.utilService.urlValida(url);
  }

  modoModificacion(id: number): void {
    this.modoAlta = false;
    this.getColeccion(id);
    this.refreshFicheros(id);
  }

  hayFacturas(): boolean {
    return this.facturas.length > 0;
  }

  hayFotos(): boolean {
    return this.fotos.length > 0;
  }

  onFacturasSeleccionadas(event: any) {
    const facturas: FileList = event.target.files;
    if (facturas.length > 0) {
      this.facturasSeleccionadas = [];
      for (let i = 0; i < facturas.length; i++) {
        const factura: File = facturas[i];
        this.facturasSeleccionadas.push(factura);
      }
    } else {
      this.facturasSeleccionadas = undefined;
    }
    this.strFacturasSeleccionadas = this.facturasSeleccionadas?.map(file => file.name).join(', ');
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

  subirFactura() {
    if (this.facturasSeleccionadas && this.coleccion.id) {
      for (let i = 0; i < this.facturasSeleccionadas.length; i++) {
        this.subiendoFacturas = true;
        const factura: File = this.facturasSeleccionadas[i];
        this.ficheroService.subirFicheroColeccion(this.coleccion.id, TipoFicheroEnum.FACTURA, factura).subscribe((fichero) => {
          this.addFichero(fichero);
          if (this.facturasSeleccionadas != undefined && i == this.facturasSeleccionadas.length - 1) {
            this.facturasSeleccionadas = undefined;
            this.strFacturasSeleccionadas = '';
            this.subiendoFacturas = false;
          }
        });
      }
    }
  }

  subirFoto() {
    if (this.fotosSeleccionadas && this.coleccion.id) {
      for (let i = 0; i < this.fotosSeleccionadas.length; i++) {
        this.subiendoFotos = true;
        const foto: File = this.fotosSeleccionadas[i];
        this.ficheroService.subirFicheroColeccion(this.coleccion.id, TipoFicheroEnum.FOTO, foto).subscribe((fichero) => {
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
    this.ficheroService.getDatosFicheroColeccion(id).subscribe(datos => {
      datos?.sort((a, b) => {
        if (a.nombre_original && b.nombre_original) {
          return a.nombre_original.localeCompare(b.nombre_original);
        }
        return 0;
      });
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
        plataforma: this.plataformaSeleccionada,
        ordenSeleccionado: 'Nombre'
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

  save(auto: boolean): void {
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
        if (auto == false) {
          this.errorService.printError('Plataforma, base y estados deben estar rellenos');
        }
      } else if (this.modoAlta) {
        this.modoAlta = false;
        this.coleccionService.addColeccion(this.coleccion).subscribe((col) => this.modoModificacion(col.id));
      } else {
        this.coleccionService.updateColeccion(this.coleccion).subscribe((col) => {
          if (auto == false) {
            this.back();
          }
          this.coleccion.codigo = col.codigo;
        });
      }
    }
  }

  delete(): void {
    if (this.coleccion.id == undefined) {
      this.errorService.printError('La coleccion no se ha genereado aún');
    } else {
      const confirmacion = window.confirm('¿Eliminar la coleccion?');
      if (confirmacion) {
        this.coleccionService.deleteColeccion(this.coleccion.id).subscribe((res) => {
          if (res.success) {
            this.back();
          } else {
            this.errorService.printError('Se ha producido un error eliminando la coleccion ' + this.coleccion.id);
          }
        });
      }
    }
  }

  back(): void {
    this.location.back();
  }
}
