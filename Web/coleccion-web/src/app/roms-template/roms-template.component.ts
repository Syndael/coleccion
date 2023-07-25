import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';
import { Rom } from '../models/rom.model';
import { Juego } from '../models/juego.model';
import { Plataforma } from '../models/plataforma.model';
import { Idioma } from '../models/idioma.model';
import { Region } from '../models/region.model';
import { TipoRom } from '../models/tipo-rom.model';
import { RomService } from '../services/rom.service';

@Component({
  selector: 'app-roms-template',
  templateUrl: './roms-template.component.html'
})
export class RomsTemplateComponent {
  constructor(
    private route: ActivatedRoute,
    private romService: RomService,
    private location: Location,
    private router: Router
  ) { }

  private modoAlta: Boolean | undefined;
  rom: Rom = {
    id: undefined,
    juego: new Juego(),
    plataforma: new Plataforma(),
    nombre_rom: undefined,
    nombre_rom_ext: undefined,
    idioma: new Idioma(),
    region: new Region(),
    tipo_rom: new TipoRom(),
    fecha_descarga: undefined
  };

  ngOnInit(): void {
    this.route.params.subscribe(params => {
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
    this.romService.getRom(id).subscribe(rom => {this.rom = rom; console.log(this.rom)});
  }

  save(): void {
    if (this.rom) {
      if (this.modoAlta) {
        this.romService.addRom(this.rom).subscribe(() => this.router.navigate([this.router.url]));
      } else {
        this.romService.updateRom(this.rom).subscribe(() => this.router.navigate([this.router.url]));
      }
    }
  }

  back(): void {
    this.location.back();
  }
}
