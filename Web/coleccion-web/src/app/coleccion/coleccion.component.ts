import { Component, OnInit } from '@angular/core';
import { Coleccion } from '../models/coleccion.model';
import { ColeccionService } from '../services/coleccion.service';

@Component({
  selector: 'app-coleccion',
  templateUrl: './coleccion.component.html'
})

export class ColeccionComponent implements OnInit {
  constructor(private coleccionService: ColeccionService) { }

  ngOnInit(): void {
    this.getColecciones();
  }

  colecciones: Coleccion[] = [];

  setColeccion?: Coleccion;
  onSelect(coleccion: Coleccion): void {
    this.setColeccion = coleccion;
  }

  getColecciones(): void {
    this.coleccionService.getColecciones().subscribe(colecciones => this.colecciones = colecciones);
  }
}