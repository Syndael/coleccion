import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { JuegoTemplateComponent } from './juego-template/juego-template.component';
import { JuegosComponent } from './juego/juego.component';
import { ColeccionComponent } from './coleccion/coleccion.component';
import { HistorialComponent } from './historial/historial.component';
import { RomsTemplateComponent } from './roms-template/roms-template.component';
import { RomsComponent } from './roms/roms.component';

const routes: Routes = [
  { path: '', redirectTo: '/coleccion', pathMatch: 'full' },
  { path: 'coleccion', component: ColeccionComponent },
  { path: 'historial', component: HistorialComponent },
  { path: 'rom/:id', component: RomsTemplateComponent },
  { path: 'rom/new', component: RomsTemplateComponent },
  { path: 'roms', component: RomsComponent },
  { path: 'juego/:id', component: JuegoTemplateComponent },
  { path: 'juego/new', component: JuegoTemplateComponent },
  { path: 'juegos', component: JuegosComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }