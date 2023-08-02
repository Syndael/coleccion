import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Rom } from '../../models/rom.model';
import { Juego } from '../../models/juego.model';
import { Plataforma } from '../../models/plataforma.model';
import { Idioma } from '../../models/idioma.model';
import { Region } from '../../models/region.model';
import { TipoRom } from '../../models/tipo-rom.model';

import { ErrorService } from '../../services/error.service';
import { RomService } from '../../services/rom.service';
import { UtilService } from '../../services/util.service';

@Component({
  selector: 'app-roms-template',
  templateUrl: './roms-template.component.html'
})
export class RomsTemplateComponent {
  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private romService: RomService,
    private utilService: UtilService,
    private errorService: ErrorService
  ) { }

  private modoAlta: Boolean | undefined;
  rom: Rom = {
    id: undefined,
    juego: undefined,
    plataforma: undefined,
    nombre_rom: undefined,
    nombre_rom_ext: undefined,
    idioma: undefined,
    region: undefined,
    tipo_rom: undefined,
    fecha_descarga: this.utilService.formatDate(new Date())
  };
  listaIdiomas: Idioma[] = [];
  listaJuegos: Juego[] = [];
  listaPlataformas: Plataforma[] = [];
  listaRegiones: Region[] = [];
  listaTiposRom: TipoRom[] = [];

  idiomaSeleccionado: number | undefined;
  juegoSeleccionado: number | undefined;
  plataformaSeleccionada: number | undefined;
  regionSeleccionada: number | undefined;
  tipoRomSeleccionado: number | undefined;


  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.utilService.getListaIdiomas(true).subscribe(idiomas => this.listaIdiomas = idiomas);
      this.utilService.getListaJuegos().subscribe(juegos => this.listaJuegos = juegos);
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

  getRom(id: number): void {
    this.romService.getRom(id).subscribe(rom => {
      this.rom = rom;
      this.idiomaSeleccionado = this.rom.idioma?.id;
      this.juegoSeleccionado = this.rom.juego?.id;
      this.plataformaSeleccionada = this.rom.plataforma?.id;
      this.regionSeleccionada = this.rom.region?.id;
      this.tipoRomSeleccionado = this.rom.tipo_rom?.id;
    });
  }

  save(): void {
    if (this.rom) {
      this.rom.idioma = this.listaIdiomas.find((idioma) => idioma.id === Number(this.idiomaSeleccionado));
      this.rom.juego = this.listaJuegos.find((juego) => juego.id === Number(this.juegoSeleccionado));
      this.rom.plataforma = this.listaPlataformas.find((plataforma) => plataforma.id === Number(this.plataformaSeleccionada));
      this.rom.region = this.listaRegiones.find((region) => region.id === Number(this.regionSeleccionada));
      this.rom.tipo_rom = this.listaTiposRom.find((tipoRom) => tipoRom.id === Number(this.tipoRomSeleccionado));

      if (this.juegoSeleccionado == undefined || this.rom.juego == undefined || this.plataformaSeleccionada == undefined || this.rom.plataforma == undefined) {
        this.errorService.printError('Plataforma y juego deben estar rellenos');
      }
      else if (this.modoAlta) {
        this.romService.addRom(this.rom).subscribe(() => this.back());
      } else {
        this.romService.updateRom(this.rom).subscribe(() => this.back());
      }
    }
  }

  back(): void {
    this.location.back();
  }
}