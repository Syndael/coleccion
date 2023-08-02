import { Component, OnInit } from '@angular/core';

import { Plataforma } from '../../models/plataforma.model';
import { Rom } from '../../models/rom.model';

import { FiltroRom } from '../../filters/roms.filter';

import { RomService } from '../../services/rom.service';
import { UtilService } from '../../services/util.service';

@Component({
  selector: 'app-roms',
  templateUrl: './roms.component.html'
})

export class RomsComponent implements OnInit {
  constructor(
    private romService: RomService,
    private utilService: UtilService
  ) { }
  listaPlataformas: Plataforma[] = [];

  filtro: FiltroRom = this.getFiltroVacio();


  ngOnInit(): void {
    this.utilService.getListaPlataformas(true).subscribe(plataformas => this.listaPlataformas = plataformas);

    let filtro = this.utilService.getFiltroRom();
    if (filtro) {
      this.filtro = filtro;
    }

    this.getRoms();
  }

  roms: Rom[] = [];

  setRom?: Rom;
  onSelect(rom: Rom): void {
    this.setRom = rom;
  }

  getFiltroVacio(): FiltroRom {
    return {
      idRom: undefined,
      plataformaSeleccionada: undefined,
      nombreJuego: undefined,
      sagaJuego: undefined
    };
  }

  limpiarFiltro(): void {
    this.filtro = this.getFiltroVacio();
    this.getRoms();
  }

  getRoms(): void {
    this.utilService.setFiltroRom(this.filtro);
    this.romService.getRoms(this.filtro).subscribe(roms => this.roms = roms);
  }
}