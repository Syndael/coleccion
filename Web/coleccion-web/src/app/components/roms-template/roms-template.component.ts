import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Rom } from '../../models/rom.model';
import { Base } from '../../models/base.model';
import { Plataforma } from '../../models/plataforma.model';
import { Idioma } from '../../models/idioma.model';
import { Region } from '../../models/region.model';
import { TipoRom } from '../../models/tipo-rom.model';

import { FiltroBase } from '../../filters/base.filter';

import { BaseService } from '../../services/base.service';
import { ErrorService } from '../../services/error.service';
import { RomService } from '../../services/rom.service';
import { UtilService } from '../../services/util.service';
import { TipoBaseEnum } from 'src/app/models/tipo-base.model';

@Component({
  selector: 'app-roms-template',
  templateUrl: './roms-template.component.html'
})
export class RomsTemplateComponent {
  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private baseService: BaseService,
    private romService: RomService,
    private utilService: UtilService,
    private errorService: ErrorService
  ) { }

  private modoAlta: Boolean | undefined;
  rom: Rom = {
    id: undefined,
    base: undefined,
    plataforma: undefined,
    nombre_rom: undefined,
    nombre_rom_ext: undefined,
    idioma: undefined,
    region: undefined,
    tipo_rom: undefined,
    fecha_descarga: this.utilService.formatDate(new Date())
  };
  listaIdiomas: Idioma[] = [];
  listaBases: Base[] = [];
  listaPlataformas: Plataforma[] = [];
  listaRegiones: Region[] = [];
  listaTiposRom: TipoRom[] = [];

  idiomaSeleccionado: number | undefined;
  baseSeleccionado: number | undefined;
  plataformaSeleccionada: number | undefined;
  regionSeleccionada: number | undefined;
  tipoRomSeleccionado: number | undefined;


  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.utilService.getListaIdiomas(true).subscribe(idiomas => this.listaIdiomas = idiomas);
      this.utilService.getListaPlataformas(false).subscribe(plataformas => this.listaPlataformas = plataformas);
      this.utilService.getListaRegiones(true).subscribe(regiones => this.listaRegiones = regiones);
      this.utilService.getListaTiposRom(true).subscribe(tiposRom => this.listaTiposRom = tiposRom);

      const id = params['id'];
      if (id && id == "new") {
        this.modoAlta = true;
      } else if (id) {
        this.modoAlta = false;
        this.getRom(id);
      }
    });
  }

  modoModificacion(id: number): void {
    this.modoAlta = false;
    this.getRom(id);
  }

  getRom(id: number): void {
    this.romService.getRom(id).subscribe(rom => {
      this.rom = rom;
      this.plataformaSeleccionada = this.rom.plataforma?.id;
      this.idiomaSeleccionado = this.rom.idioma?.id;
      this.baseSeleccionado = this.rom.base?.id;
      this.regionSeleccionada = this.rom.region?.id;
      this.tipoRomSeleccionado = this.rom.tipo_rom?.id;
      this.refreshBases();
    });
  }

  refreshBases(): void {
    this.listaBases = [];
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

  save(auto: boolean): void {
    if (this.rom) {
      this.rom.idioma = this.listaIdiomas.find((idioma) => idioma.id === Number(this.idiomaSeleccionado));
      this.rom.base = this.listaBases.find((base) => base.id === Number(this.baseSeleccionado));
      this.rom.plataforma = this.listaPlataformas.find((plataforma) => plataforma.id === Number(this.plataformaSeleccionada));
      this.rom.region = this.listaRegiones.find((region) => region.id === Number(this.regionSeleccionada));
      this.rom.tipo_rom = this.listaTiposRom.find((tipoRom) => tipoRom.id === Number(this.tipoRomSeleccionado));

      if (this.baseSeleccionado == undefined || this.rom.base == undefined || this.plataformaSeleccionada == undefined || this.rom.plataforma == undefined) {
        if (auto == false) {
          this.errorService.printError('Plataforma y base deben estar rellenos');
        }
      }
      else if (this.modoAlta) {
        this.modoAlta = false;
        this.romService.addRom(this.rom).subscribe((rom) => {
          if (auto == false) {
            this.back();
          }
          this.modoModificacion(rom.id)
        });
      } else {
        this.romService.updateRom(this.rom).subscribe((rom) => {
          if (auto == false) {
            this.back();
          }
          this.rom.nombre_rom = rom.nombre_rom;
        });
      }
    }
  }

  delete(): void {
    if (this.rom.id == undefined) {
      this.errorService.printError('La rom no se ha genereado aún');
    } else {
      const confirmacion = window.confirm('¿Eliminar la rom?');
      if (confirmacion) {
        this.romService.deleteRom(this.rom.id).subscribe((res) => {
          if (res.success) {
            this.back();
          } else {
            this.errorService.printError('Se ha producido un error eliminando la rom ' + this.rom.id);
          }
        });
      }
    }
  }

  back(): void {
    this.location.back();
  }
}