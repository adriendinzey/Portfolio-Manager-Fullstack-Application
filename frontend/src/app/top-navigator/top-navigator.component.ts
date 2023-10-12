import { Component, Output, EventEmitter } from '@angular/core';
import { DjangoDataService } from '../django-data.service';
import { CommonService } from '../common-service.service';

@Component({
  selector: 'app-topnavigator',
  templateUrl: './top-navigator.component.html',
  styleUrls: ['./top-navigator.component.css']
})
export class TopnavigatorComponent {
  // properties of this class
  whichVolume: any

  // constructor which is an instance of our service
  constructor(private djangoData: DjangoDataService, private commonService: CommonService) { }

  @Output("updateVisuals") updateVisuals: EventEmitter<any> = new EventEmitter();

  fund(){    
    this.djangoData.doFundingTransaction(this.whichVolume).subscribe((response: any) => {
      this.commonService.sendUpdate("Cash Balance Updated.");
    });
    this.clearInputQty();
  }

  clearInputQty(){
    const input = <HTMLInputElement>document.getElementsByClassName("input-qty")[0]
    if (input && input.value){
      input.value = "";
    }
  }
}
