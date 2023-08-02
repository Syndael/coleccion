import { Component, OnInit } from '@angular/core';

import { Juego } from '../../models/juego.model';

import { FiltroJuego } from '../../filters/juego.filter';

import { JuegoService } from '../../services/juego.service';
import { UtilService } from '../../services/util.service';

@Component({
  selector: 'app-juegos',
  templateUrl: './juego.component.html'
})

export class JuegosComponent implements OnInit {
  constructor(
    private juegoService: JuegoService,
    private utilService: UtilService
  ) { }

  filtro: FiltroJuego = this.getFiltroVacio();

  ngOnInit(): void {
    let filtro = this.utilService.getFiltroJuego();
    if (filtro) {
      this.filtro = filtro;
    }

    this.getJuegos();
  }

  juegos: Juego[] = [];

  setJuego?: Juego;
  onSelect(juego: Juego): void {
    this.setJuego = juego;
  }

  getFiltroVacio(): FiltroJuego {
    return {
      idJuego: undefined,
      nombreJuego: undefined,
      sagaJuego: undefined
    };
  }

  limpiarFiltro(): void {
    this.filtro = this.getFiltroVacio();
    this.getJuegos();
  }

  getJuegos(): void {
    this.utilService.setFiltroJuego(this.filtro);
    this.juegoService.getJuegos(this.filtro).subscribe(juegos => { this.juegos = juegos; this.utilService.setListaJuegos(juegos) });
  }
}