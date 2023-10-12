from django.db import models
# Create your models here.

class Symbol(models.Model):
    symbolID = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
 
class StockTransaction (models.Model):
    transactionID = models.AutoField(primary_key=True)
    symbolID = models.ForeignKey(Symbol, on_delete=models.PROTECT)
    volume = models.IntegerField()
    price = models.DecimalField(max_digits=65, decimal_places=10)
    transactionDateTime = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=65, decimal_places=10)
    isBuy = models.BooleanField()

class PortfolioValue(models.Model):
    portfolioID = models.AutoField(primary_key=True)
    symbolID = models.ForeignKey(Symbol, on_delete=models.PROTECT)
    totalPrice = models.DecimalField(max_digits=65, decimal_places=10)
    totalVolume = models.IntegerField()

class PortfolioEntry(models.Model):
    portfolioID = models.AutoField(primary_key=True)
    symbolID = models.ForeignKey(Symbol, on_delete=models.PROTECT)
    totalPrice = models.DecimalField(max_digits=65, decimal_places=10)
    totalVolume = models.IntegerField()
    ticker = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)

class AccountTransaction(models.Model):
    accountTransactionID = models.AutoField(primary_key=True)
    total = models.DecimalField(max_digits=65, decimal_places=10)
    currencyCode = models.CharField(max_length=3, default='USD')
    isFundingTransaction = models.BooleanField()
    transactionDateTime = models.DateTimeField(auto_now_add=True)

class UserAccount(models.Model):
    userID = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=200)
    cashBalance = models.DecimalField(max_digits=65, decimal_places=10, default=0)
    stockBalance = models.DecimalField(max_digits=65, decimal_places=10, default=0)

class CurrentStockPrice(models.Model):
    stockPriceID = models.AutoField(primary_key=True)
    symbolID = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    currentPrice = models.DecimalField(max_digits=65, decimal_places=10)
    currentDateTime = models.DateTimeField(auto_now=True)

