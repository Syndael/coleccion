import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ColeccionComponent } from './components/coleccion/coleccion.component';
import { ColeccionTemplateComponent } from './components/coleccion-template/coleccion-template.component';
import { ProgresoComponent } from './components/progreso/progreso.component';
import { ProgresoTemplateComponent } from './components/progreso-template/progreso-template.component';
import { BaseComponent } from './components/base/base.component';
import { BaseTemplateComponent } from './components/base-template/base-template.component';
import { RomsTemplateComponent } from './components/roms-template/roms-template.component';
import { RomsComponent } from './components/roms/roms.component';

const routes: Routes = [
  { path: '', redirectTo: '/coleccion', pathMatch: 'full' },
  { path: 'coleccion', component: ColeccionComponent },
  { path: 'coleccion/:id', component: ColeccionTemplateComponent },
  { path: 'coleccion/new', component: ColeccionTemplateComponent },
  { path: 'progreso', component: ProgresoComponent },
  { path: 'progreso/:id', component: ProgresoTemplateComponent },
  { path: 'progreso/new', component: ProgresoTemplateComponent },
  { path: 'bases', component: BaseComponent },
  { path: 'base/:id', component: BaseTemplateComponent },
  { path: 'base/new', component: BaseTemplateComponent },
  { path: 'rom/:id', component: RomsTemplateComponent },
  { path: 'rom/new', component: RomsTemplateComponent },
  { path: 'roms', component: RomsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }