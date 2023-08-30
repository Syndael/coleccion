import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { ToastrModule } from 'ngx-toastr';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BaseComponent } from './components/base/base.component';
import { BaseTemplateComponent } from './components/base-template/base-template.component';
import { ColeccionComponent } from './components/coleccion/coleccion.component';
import { EllipsisPipe, FormatPipe } from './pipes';
import { ProgresoComponent } from './components/progreso/progreso.component';
import { RomsComponent } from './components/roms/roms.component';
import { RomsTemplateComponent } from './components/roms-template/roms-template.component';
import { ProgresoTemplateComponent } from './components/progreso-template/progreso-template.component';
import { ColeccionTemplateComponent } from './components/coleccion-template/coleccion-template.component';
import { EstadisticasComponent } from './components/estadisticas/estadisticas.component';

@NgModule({
  declarations: [
    AppComponent,
    BaseComponent,
    BaseTemplateComponent,
    ColeccionComponent,
    ProgresoComponent,
    RomsComponent,
    RomsTemplateComponent,
    ProgresoTemplateComponent,
    ColeccionTemplateComponent,
    EllipsisPipe,
    FormatPipe,
    EstadisticasComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    HttpClientModule,
    ToastrModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
