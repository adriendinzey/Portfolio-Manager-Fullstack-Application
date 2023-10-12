import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { HoldingsComponent } from './holdings/holdings.component';
import { VisualizationsComponent } from './visualizations/visualizations.component';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { ProfileComponent } from './profile/profile.component';
import { BuySellComponent } from './buy-sell/buy-sell.component';
import { TopnavigatorComponent } from './top-navigator/top-navigator.component';

@NgModule({
  declarations: [
    AppComponent,
    HoldingsComponent,
    VisualizationsComponent,
    ProfileComponent,
    BuySellComponent,
    TopnavigatorComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
