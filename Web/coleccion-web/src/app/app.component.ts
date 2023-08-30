import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { Environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent {
  constructor(
    private route: ActivatedRoute
  ) { }

  cintaEntorno = Environment.TAG;
  menuItems = [
    { id: 1, name: 'Colección', route: '/coleccion', selected: false },
    { id: 2, name: 'Progresos', route: '/progreso', selected: false },
    { id: 3, name: 'ROMs', route: '/roms', selected: false },
    { id: 4, name: 'Juegos/Consolas/Otros', route: '/bases', selected: false },
    { id: 5, name: 'Estadísticas', route: '/estadisticas', selected: false }
  ];

  onMenuItemClick(item: any): void {
    this.menuItems.forEach(menuItem => {
      menuItem.selected = menuItem === item;
    });
  }
}
