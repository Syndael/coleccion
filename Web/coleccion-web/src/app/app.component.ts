import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent {
  menuItems = [
    { id: 1, name: 'Colección', route: '/coleccion', selected: true },
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
