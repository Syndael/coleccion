import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ColeccionComponent } from './components/coleccion/coleccion.component';
import { ColeccionTemplateComponent } from './components/coleccion-template/coleccion-template.component';
import { HistorialComponent } from './components/historial/historial.component';
import { HistorialTemplateComponent } from './components/historial-template/historial-template.component';
import { JuegosComponent } from './components/juego/juego.component';
import { JuegoTemplateComponent } from './components/juego-template/juego-template.component';
import { RomsTemplateComponent } from './components/roms-template/roms-template.component';
import { RomsComponent } from './components/roms/roms.component';

const routes: Routes = [
  { path: '', redirectTo: '/coleccion', pathMatch: 'full' },
  { path: 'coleccion', component: ColeccionComponent },
  { path: 'coleccion/:id', component: ColeccionTemplateComponent },
  { path: 'coleccion/new', component: ColeccionTemplateComponent },
  { path: 'progreso', component: HistorialComponent },
  { path: 'progreso/:id', component: HistorialTemplateComponent },
  { path: 'progreso/new', component: HistorialTemplateComponent },
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