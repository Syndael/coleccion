import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ColeccionComponent } from './coleccion/coleccion.component';
import { ColeccionTemplateComponent } from './coleccion-template/coleccion-template.component';
import { HistorialComponent } from './historial/historial.component';
import { HistorialTemplateComponent } from './historial-template/historial-template.component';
import { JuegosComponent } from './juego/juego.component';
import { JuegoTemplateComponent } from './juego-template/juego-template.component';
import { RomsTemplateComponent } from './roms-template/roms-template.component';
import { RomsComponent } from './roms/roms.component';

const routes: Routes = [
  { path: '', redirectTo: '/coleccion', pathMatch: 'full' },
  { path: 'coleccion', component: ColeccionComponent },
  { path: 'coleccion/:id', component: ColeccionTemplateComponent },
  { path: 'coleccion/new', component: ColeccionTemplateComponent },
  { path: 'historial', component: HistorialComponent },
  { path: 'historial/:id', component: HistorialTemplateComponent },
  { path: 'historial/new', component: HistorialTemplateComponent },
  { path: 'juegos', component: JuegosComponent },
  { path: 'juego/:id', component: JuegoTemplateComponent },
  { path: 'juego/new', component: JuegoTemplateComponent },
  { path: 'rom/:id', component: RomsTemplateComponent },
  { path: 'rom/new', component: RomsTemplateComponent },
  { path: 'roms', component: RomsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }