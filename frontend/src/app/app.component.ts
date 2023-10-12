import { Component, ViewChild} from '@angular/core';
import { VisualizationsComponent } from './visualizations/visualizations.component';
import { HoldingsComponent } from './holdings/holdings.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';

  @ViewChild(VisualizationsComponent) visualizations!:VisualizationsComponent;
  @ViewChild(HoldingsComponent) holdings!:HoldingsComponent;

  updateVisuals(){
    this.visualizations.ngOnInit();
    this.holdings.ngOnInit();
  }
}
