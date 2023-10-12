import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DjangoDataService {
  // properties
  apiUrl =
    'http://127.0.0.1:8000';

  // we need access to the http clients
  constructor(private http: HttpClient) {}

  // methods
  // every angular service must return an Observable()
  getPortfolioDetails() {
    const portfolioUrl = `${this.apiUrl}/portfoliovalue/`;
    try {
      return this.http.get(portfolioUrl);
    } catch (error) {
      return new Observable();
    }
  }

  getHoldingsDetails() {
    const holdingUrl = `${this.apiUrl}/portfoliovalue/portfolioentry/`;
    try {
      return this.http.get(holdingUrl);
    } catch (error) {
      return new Observable();
    }
  }

  getAccountsDetails() {
    const accountsUrl = `${this.apiUrl}/useraccount/`;
    try {
      return this.http.get(accountsUrl);
    } catch (error) {
      return new Observable();
    }
  }

  getStockTransactions() {
    const transactionsUrl = `${this.apiUrl}/stocktransaction/`;
    try {
      return this.http.get(transactionsUrl);
    } catch (error) {
      return new Observable();
    }
  }

  getAccountTransactions() {
    const transactionsUrl = `${this.apiUrl}/accounttransaction/`;
    try {
      return this.http.get(transactionsUrl);
    } catch (error) {
      return new Observable();
    }
  }

  getTickerQuote(whichTicker: string) {
    const tickerUrl = `${this.apiUrl}/yfinance/?ticker=${whichTicker}`;
    try {
      return this.http.get(tickerUrl);
    } catch (error) {
      return new Observable();
    }
  }

  getStock() {
    const stockUrl = `${this.apiUrl}/symbol/`;
    try {
      return this.http.get(stockUrl);
    } catch (error) {
      return new Observable();
    }
  }

  getStockName(whichTicker: string) {
    const stockNameUrl = `${this.apiUrl}/symbol/ticker/?ticker=${whichTicker}`;
    try {
      return this.http.get(stockNameUrl);
    } catch (error) {
      return new Observable();
    }
  }

  getTickerFromID(symbolID: any){
    const stockNameUrl = `${this.apiUrl}/symbol/?symbolID=${symbolID}`;
    try {
      return this.http.get(stockNameUrl);
    } catch (error) {
      return new Observable();
    }
  }

  doBuyAction(whichSymbolId: any, whichVolume: any) {
    const sellUrl = `${this.apiUrl}/stocktransaction/`;
    const body = {symbolID:whichSymbolId,volume:whichVolume,isBuy:'True'}
    try {
      let post = this.http.post(sellUrl, body);
      return post;
    } catch (error) {
      return new Observable();
    }
  }

  doSellAction(whichSymbolId: any, whichVolume: any) {
    const sellUrl = `${this.apiUrl}/stocktransaction/`;
    const body = {symbolID:whichSymbolId,volume:whichVolume,isBuy:'False'}
    try {
      let post = this.http.post(sellUrl, body);
      return post;
    } catch (error) {
      return new Observable();
    }
  }

  doAddSymbol(whichName: string, whichTicker: string) {
    const addSymbolUrl = `${this.apiUrl}/symbol/create/symbol/`;
    const body = {full_name:whichName,ticker:whichTicker}
    try {
      let post = this.http.post(addSymbolUrl, body);
      return post;
    } catch (error) {
      return new Observable();
    }
  }

  doFundingTransaction(amount: any){
    const transactionsUrl = `${this.apiUrl}/accounttransaction/`;    
    const body = {total:amount,isFundingTransaction: 'True'}
    try {
      let post = this.http.post(transactionsUrl, body);
      return post;
    } catch (error) {
      return new Observable();
    }
  }

  getAccountDetails(){
    const getAccountUrl = `${this.apiUrl}/useraccount/?userID=1`;
    try {
      return this.http.get(getAccountUrl);
    } catch (error) {
      return new Observable();
    }
  }

  updatePortfolioBalance(amount: any){
    const transactionsUrl = `${this.apiUrl}/useraccount/portfoliobalance/`;    
    const body = {amount:amount}
    try {
      let post = this.http.post(transactionsUrl, body);
      return post;
    } catch (error) {
      return new Observable();
    }
  }

}
