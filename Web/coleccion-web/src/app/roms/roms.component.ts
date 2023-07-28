import { Component, OnInit } from '@angular/core';

import { JuegoService } from '../services/juego.service';
import { PlataformaService } from '../services/plataforma.service';
import { Rom } from '../models/rom.model';
import { RomService } from '../services/rom.service';

@Component({
  selector: 'app-roms',
  templateUrl: './roms.component.html'
})

export class RomsComponent implements OnInit {
  constructor(
    private romService: RomService
  ) { }

  ngOnInit(): void {
    this.getRoms();
  }

  roms: Rom[] = [];

  setRom?: Rom;
  onSelect(rom: Rom): void {
    this.setRom = rom;
  }

  getRoms(): void {
    this.romService.getRoms().subscribe(roms => this.roms = roms);
  }
}