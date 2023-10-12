import { Component } from '@angular/core';
import { DjangoDataService } from '../django-data.service';

@Component({
  selector: 'app-holdings',
  templateUrl: './holdings.component.html',
  styleUrls: ['./holdings.component.css']
})
export class HoldingsComponent {
  // properties of this class
  portfolio = [] // this empty array will be populated from the end-point API

  // constructor which is an instance of our service
  constructor(private djangoData: DjangoDataService) { }

  // methods of this class

  // when the component first loads, it will run ngOnInit()
  ngOnInit() {
    // make a call to our djangoData service
    this.djangoData.getHoldingsDetails().subscribe(this.handleAllHoldings())
  }

  // put the recieved holding details from the endpoint API into holdings array
  handleAllHoldings() {
    return (recieved: any) => {
      this.portfolio = recieved
    }
  }

}
