import { Component, OnInit } from '@angular/core';
import { Juego } from '../models/juego.model';
import { JuegoService } from '../services/juego.service';
import { UtilService } from '../services/util.service';

@Component({
  selector: 'app-juegos',
  templateUrl: './juego.component.html'
})

export class JuegosComponent implements OnInit {
  constructor(
    private juegoService: JuegoService,
    private utilService: UtilService
  ) { }

  ngOnInit(): void {
    this.getJuegos();
  }

  juegos: Juego[] = [];

  setJuego?: Juego;
  onSelect(juego: Juego): void {
    this.setJuego = juego;
  }

  getJuegos(): void {
    this.juegoService.getJuegos().subscribe(juegos => { this.juegos = juegos; this.utilService.setListaJuegos(juegos) });
  }
}