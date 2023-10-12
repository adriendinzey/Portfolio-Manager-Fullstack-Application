import { Component } from '@angular/core';
import Chart from 'chart.js/auto';

import {DjangoDataService} from '../django-data.service'

@Component({
  selector: 'app-visualizations',
  templateUrl: './visualizations.component.html',
  styleUrls: ['./visualizations.component.css']
})
export class VisualizationsComponent {
  account = null;
  portfolioBalance = 0;
  cashBalance = 100000;
  stockTotals = 0;
  accountTotals = 0;
  weeklyTransactions: any[] = [];

  public chart: any;
  createChart(){
    this.chart = new Chart("myChart", {
      type: 'bar',
      data: {
          labels: this.weeklyTransactions.map((transaction:any) => transaction.date),
          datasets: [{
              label: 'Total Cost',
              data: this.weeklyTransactions.map((transaction:any) => transaction.income),
              barThickness: 12,
              backgroundColor: [
                '#90ee90',
              ],
          },
          {
            label: 'Realized Gains',
            barThickness: 12,
            data: this.weeklyTransactions.map((transaction:any) => transaction.expenses),
            backgroundColor: [
                '#fff',
            ],
        }]
      },
      options: {
          scales: {
              y: {
                  beginAtZero: true
              }
          },
          aspectRatio: 5,
      }
  });
  }

  constructor(private djangoData: DjangoDataService) { }

  ngOnInit(): void {
    this.accountTotals = 0;
    this.stockTotals = 0;
    this.portfolioBalance = 0;

    this.djangoData.getAccountsDetails().subscribe(this.handleAccounts())
    this.djangoData.getStockTransactions().subscribe(this.handleStockTransactions())
    this.djangoData.getAccountTransactions().subscribe(this.handleAccountTransactions())
    this.djangoData.getPortfolioDetails().subscribe(this.handlePortfolio())
    this.djangoData.getAccountDetails().subscribe(this.handleAccountDetails())
  }

  handleAccountDetails(){
    return (received: any) => {
      this.cashBalance = received.cashBalance
    }
  }

  handlePortfolio(){
    return (recieved: any) =>{
      recieved.forEach((entry:any) =>{
        this.portfolioBalance += parseFloat(entry.totalPrice)
      })
      this.djangoData.updatePortfolioBalance(this.portfolioBalance)
    }
  }

  handleAccounts() {
    return (received: any) => {
      this.account = received
    }
  }

  handleStockTransactions() {
    return (received: any) => {
      const today = new Date()
      const week = new Date(today.getTime() - (7*24*60*60*1000)); //get the date one week ago

      var weeklyTransactions = received.filter((transaction: any) => {
        transaction.transactionDateTime = new Date(transaction.transactionDateTime)
        if (transaction.transactionDateTime && transaction.transactionDateTime > week){
          return transaction
        }
      })
      this.getWeeklyStockTotal(weeklyTransactions)
      this.getWeeklyAccountTotal(weeklyTransactions)
      this.getLastWeekTotals(weeklyTransactions)
    }
  }
  
  getWeeklyStockTotal(weeklyTransactions:any){
    weeklyTransactions.forEach((transaction:any) => {
      if (transaction.isBuy){
        this.stockTotals += parseFloat(transaction.total)
      }
      else{
        this.stockTotals -= parseFloat(transaction.total)
      }
    })
  }

  getLastWeekTotals(weeklyTransactions:any){
    const today = new Date()
    this.weeklyTransactions = [];

    for (let i = 5; i >= 0; i--){
      let thisDate = new Date(today.getTime()-(i*24*3600000));
      const month = thisDate.getMonth() + 1
      const date = thisDate.getDate();
      let day = {date: `${month}/${date}`, income: 0, expenses: 0}

      weeklyTransactions.forEach((transaction:any) => {
        let transactionDate = new Date(transaction.transactionDateTime)
        if (transactionDate.getDate() == date && transactionDate.getMonth() + 1 == month){
          if (transaction.isBuy){
            day.income += parseFloat(transaction.total)
          }
          else{
            day.expenses += parseFloat(transaction.total)
          }
        }
      })

      this.weeklyTransactions.push(day)
    }
    if (!this.chart){
      this.createChart();
    }
    else {
      this.chart.data = {
        labels: this.weeklyTransactions.map((transaction:any) => transaction.date),
        datasets: [{
            label: 'Total Cost',
            data: this.weeklyTransactions.map((transaction:any) => transaction.income),
            barThickness: 12,
            backgroundColor: [
              '#90ee90',
            ],
        },
        {
          label: 'Realized Gains',
          barThickness: 12,
          data: this.weeklyTransactions.map((transaction:any) => transaction.expenses),
          backgroundColor: [
              '#fff',
          ],
      }]
    }
  this.chart.update();
    }
  }

  handleAccountTransactions() {
    return (received: any) => {
      const today = new Date()
      const week = new Date(today.getTime() - (7*24*60*60*1000)); //get the date one week ago
      var weeklyTransactions = received.filter((transaction: any) => {
        if (transaction.transactionDateTime && new Date(transaction.transactionDateTime) > week){
          return transaction
        }
      })

      this.getWeeklyAccountTotal(weeklyTransactions)
    }
  }

  getWeeklyAccountTotal(weeklyTransactions:any){
    weeklyTransactions.forEach((transaction:any) => {
      if (transaction.isBuy){
        this.accountTotals -= parseFloat(transaction.total)
      }
      else{
        this.accountTotals += parseFloat(transaction.total)
      }
    })    
  }
}
