import { Component, Output, EventEmitter,  } from '@angular/core';
import { Subscription } from 'rxjs';
import { DjangoDataService } from '../django-data.service';
import { CommonService } from '../common-service.service';

@Component({
  selector: 'app-buy-sell',
  templateUrl: './buy-sell.component.html',
  styleUrls: ['./buy-sell.component.css']
})

export class BuySellComponent {
  // properties of this class
  whichTicker = ''
  tickerInfo = [] // this empty array will be populated from the end-point API
  dataName: any = {}
  dataMeta: any = {}
  dataValues: any = {}
  whichSymbolId: any
  whichVolume: any
  portfolio = []
  stocks = []
  stockID: any
  stockName: string = ''
  subscription: any

  // constructor which is an instance of our service
  constructor(private djangoData: DjangoDataService, private commonService: CommonService) {
    this.subscription = this.commonService.getUpdate().subscribe(message => { 
        console.log(message)   
        this.updateVisuals.emit();     
      });
   }

   ngOnDestroy(){
    this.subscription.unsubscribe();
   }

  @Output("updateVisuals") updateVisuals: EventEmitter<any> = new EventEmitter();

  // methods of this class
  getQuote() {
    // make a call to our djangoData service
    this.djangoData.getTickerQuote(this.whichTicker).subscribe(this.handleTickerSearch())
  }

  sell() {
    // make a call to the django data service
    this.djangoData.doSellAction(this.stockID, this.whichVolume).subscribe((response: any) => {
      this.updateVisuals.emit();
    });
    this.clearInputQty();
  }

  buy() {
    // make a call to the django data service
    this.djangoData.doBuyAction(this.stockID, this.whichVolume).subscribe((response: any) => {
      this.updateVisuals.emit();
    });
    this.clearInputQty();
  }

  clearInputQty(){
    const input = <HTMLInputElement>document.getElementsByClassName("input-qty")[0]
    if (input && input.value){
      input.value = "";
    }
  }

  // put the recieved holding details from the endpoint API into holdings array
  handleTickerSearch() {
    return (recieved: any) => {
      this.tickerInfo = recieved
      this.dataValues = this.tickerInfo
      this.stockName = this.dataValues.full_name
      this.stockID = this.dataValues.symbolID
      console.log(this.stockName)
    }
  }
}
