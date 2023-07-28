import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent {
  constructor(
    private route: ActivatedRoute
  ) { }

  menuItems = [
    { id: 1, name: 'Colección', route: '/coleccion', selected: false },
    { id: 2, name: 'Historial', route: '/historial', selected: false },
    { id: 3, name: 'ROMs', route: '/roms', selected: false },
    { id: 4, name: 'Juegos', route: '/juegos', selected: false }
  ];

  onMenuItemClick(item: any): void {
    this.menuItems.forEach(menuItem => {
      menuItem.selected = menuItem === item;
    });
  }
}
