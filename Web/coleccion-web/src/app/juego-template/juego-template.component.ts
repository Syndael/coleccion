import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';
import { Juego } from '../models/juego.model';
import { JuegoService } from '../services/juego.service';

@Component({
  selector: 'app-juego-template',
  templateUrl: './juego-template.component.html'
})
export class JuegoTemplateComponent {
  constructor(
    private route: ActivatedRoute,
    private juegoService: JuegoService,
    private location: Location,
    private router: Router
  ) { }

  private modoAlta: Boolean | undefined;
  juego: Juego = {
    id: undefined,
    nombre: undefined,
    saga: undefined,
    fecha_salida: undefined
  };

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const id = params['id'];
      if (id && id == "new") {
        this.modoAlta = true;
      } else if (id) {
        this.modoAlta = false;
        this.getJuego(id);
      }
    });
  }

  getJuego(id: number): void {
    this.juegoService.getJuego(id).subscribe(juego => this.juego = juego);
  }

  save(): void {
    if (this.juego) {
      if (this.modoAlta) {
        this.juegoService.addJuego(this.juego).subscribe(() => this.back());
      } else {
        this.juegoService.updateJuego(this.juego).subscribe(() => this.back());
      }
    }
  }

  back(): void {
    this.location.back();
  }
}
