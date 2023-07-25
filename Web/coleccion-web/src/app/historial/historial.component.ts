import { Component, OnInit } from '@angular/core';
import { Historial } from '../models/historial.model';
import { HistorialService } from '../services/historial.service';

@Component({
  selector: 'app-historial',
  templateUrl: './historial.component.html'
})

export class HistorialComponent implements OnInit {
  constructor(private historialService: HistorialService) { }

  ngOnInit(): void {
    this.getHistoriales();
  }

  historiales: Historial[] = [];

  setHistorial?: Historial;
  onSelect(historial: Historial): void {
    this.setHistorial = historial;
  }

  getHistoriales(): void {
    this.historialService.getHistoriales().subscribe(historiales => this.historiales = historiales);
  }
}