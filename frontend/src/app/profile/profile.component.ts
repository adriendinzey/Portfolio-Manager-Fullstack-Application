import { Component } from '@angular/core';

import {DjangoDataService} from '../django-data.service'

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {
  account = null;
  constructor(private djangoData: DjangoDataService) { }

  ngOnInit(): void {
    this.djangoData.getAccountsDetails().subscribe(this.handleAccounts())
  }

  handleAccounts() {
    return (received: any) => {
      this.account = received
    }
  }
}
