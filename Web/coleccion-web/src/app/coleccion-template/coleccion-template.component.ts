import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Coleccion } from '../models/coleccion.model';
import { Estado } from '../models/estado.model';
import { Idioma } from '../models/idioma.model';
import { Juego } from '../models/juego.model';
import { Plataforma } from '../models/plataforma.model';
import { Region } from '../models/region.model';
import { TipoEstado } from '../models/tipo-estado';

import { ErrorService } from '../services/error.service';
import { ColeccionService } from '../services/coleccion.service';
import { UtilService } from '../services/util.service';

@Component({
  selector: 'app-coleccion-template',
  templateUrl: './coleccion-template.component.html'
})
export class ColeccionTemplateComponent {
  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private coleccionService: ColeccionService,
    private utilService: UtilService,
    private errorService: ErrorService
  ) { }

  private modoAlta: Boolean | undefined;
  coleccion: Coleccion = {
    id: undefined,
    juego: undefined,
    plataforma: undefined,
    idioma: undefined,
    region: undefined,
    estado_general: undefined,
    estado_caja: undefined,
    fecha_compra: undefined,
    fecha_recibo: undefined,
    coste: undefined,
    tienda: undefined,
    notas: undefined
  };
  listaEstadosGeneral: Estado[] = [];
  listaEstadosCaja: Estado[] = [];
  listaIdiomas: Idioma[] = [];
  listaJuegos: Juego[] = [];
  listaPlataformas: Plataforma[] = [];
  listaRegiones: Region[] = [];

  estadoGeneralSeleccionado: number | undefined;
  estadoCajaSeleccionado: number | undefined;
  idiomaSeleccionado: number | undefined;
  juegoSeleccionado: number | undefined;
  plataformaSeleccionada: number | undefined;
  regionSeleccionada: number | undefined;

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.utilService.getListaEstados(TipoEstado.GENERAL, false).subscribe(estados => this.listaEstadosGeneral = estados);
      this.utilService.getListaEstados(TipoEstado.CAJAS, false).subscribe(estados => this.listaEstadosCaja = estados);
      this.utilService.getListaIdiomas(true).subscribe(idiomas => this.listaIdiomas = idiomas);
      this.utilService.getListaJuegos().subscribe(juegos => this.listaJuegos = juegos);
      this.utilService.getListaPlataformas().subscribe(plataformas => this.listaPlataformas = plataformas);
      this.utilService.getListaRegiones(true).subscribe(regiones => this.listaRegiones = regiones);

      const id = params['id'];
      if (id && id == "new") {
        this.modoAlta = true;
      } else if (id) {
        this.modoAlta = false;
        this.getColeccion(id);
      }
    });
  }

  getColeccion(id: number): void {
    this.coleccionService.getColeccion(id).subscribe(coleccion => {
      this.coleccion = coleccion;
      this.estadoGeneralSeleccionado = this.coleccion.estado_general?.id;
      this.estadoCajaSeleccionado = this.coleccion.estado_caja?.id;
      this.idiomaSeleccionado = this.coleccion.idioma?.id;
      this.juegoSeleccionado = this.coleccion.juego?.id;
      this.plataformaSeleccionada = this.coleccion.plataforma?.id;
      this.regionSeleccionada = this.coleccion.region?.id;
    });
  }

  save(): void {
    if (this.coleccion) {
      this.coleccion.estado_general = this.listaEstadosGeneral.find((estado) => estado.id === Number(this.estadoGeneralSeleccionado));
      this.coleccion.estado_caja = this.listaEstadosCaja.find((estado) => estado.id === Number(this.estadoCajaSeleccionado));
      this.coleccion.idioma = this.listaIdiomas.find((idioma) => idioma.id === Number(this.idiomaSeleccionado));
      this.coleccion.juego = this.listaJuegos.find((juego) => juego.id === Number(this.juegoSeleccionado));
      this.coleccion.plataforma = this.listaPlataformas.find((plataforma) => plataforma.id === Number(this.plataformaSeleccionada));
      this.coleccion.region = this.listaRegiones.find((region) => region.id === Number(this.regionSeleccionada));

      if (this.juegoSeleccionado == undefined || this.coleccion.juego == undefined || this.plataformaSeleccionada == undefined || this.coleccion.plataforma == undefined) {
        this.errorService.printError('Plataforma y juego deben estar rellenos');
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
