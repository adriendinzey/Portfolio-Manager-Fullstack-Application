from django.shortcuts import get_list_or_404
from django.http.response import JsonResponse
from rest_framework import viewsets

from PortfolioManagementApp.models import Symbol, StockTransaction, PortfolioValue, PortfolioEntry, AccountTransaction, UserAccount, CurrentStockPrice
from PortfolioManagementApp.seriealizers import SymbolSerializer, StockTransactionSerializer, PortfolioValueSerializer, PortfolioEntrySerializer, AccountTransactionSerializer, UserAccountSerializer, CurrentStockPriceSerializer
import yfinance as yf
from decimal import Decimal

# Create your views here.

class SymbolViewSet(viewsets.ViewSet):
    def getAll(self, request):   
        symbolID = request.GET.get('symbolID','')
        if symbolID != '':
            symbol = get_list_or_404(Symbol,pk=symbolID)
            symbolsSerializer = SymbolSerializer(symbol, many=True)
        else:
            symbols = Symbol.objects.all()
            symbolsSerializer = SymbolSerializer(symbols, many=True)
        return JsonResponse(symbolsSerializer.data,safe=False)
    
    def getByTicker(self,request):
        ticker = request.GET.get('ticker','')
        symbol = Symbol.objects.get(ticker=ticker)     
        symbolsSerializer = SymbolSerializer(symbol, many=True)
        return JsonResponse(symbolsSerializer.data,safe=False)
    
    def getByFullname(self,request):
        full_name = request.GET.get('full_name','')
        symbol = Symbol.objects.filter(full_name__exact=full_name)
        symbolsSerializer = SymbolSerializer(symbol, many=True)
        return JsonResponse(symbolsSerializer.data,safe=False)
        
    def addSymbol(self, request):
        symbolsSerializer = SymbolSerializer(data=request.data)
        if symbolsSerializer.is_valid():
            symbolsSerializer.save()
            return JsonResponse({'message':"Symbol inserted successfully."})
        else:            
            return JsonResponse({'message':"Symbol insertion failed."})
        
    def deleteSymbol(self, request):
        symbolID = request.GET.get('symbolID','')
        symbol = Symbol.objects.get(pk = symbolID)
        symbol.delete()
        return JsonResponse({'message':"Symbol deleted successfully."})
    
    def updateName(self,request):
        symbolID = request.data['symbolID']
        full_name = request.data['full_name']
        symbol = Symbol.objects.get(pk=symbolID)
        symbol.full_name = full_name
        symbol.save()
        return JsonResponse({'message':"Name updated successfully."})




class StockTransactionViewSet (viewsets.ViewSet):
    def getAll(self, request):        
        transactionID = request.GET.get('transactionID','')
        if transactionID != '':
            transaction = get_list_or_404(StockTransaction,pk=transactionID)
            stockTransactionsSerializer = StockTransactionSerializer(transaction, many=True)
        else:            
            transactions = StockTransaction.objects.all()
            stockTransactionsSerializer = StockTransactionSerializer(transactions, many=True)
        return JsonResponse(stockTransactionsSerializer.data,safe=False)
    
    def addStockTransaction(self, request):   
        data=dict()
        data['symbolID'] = request.data['symbolID']
        data['volume'] = request.data['volume']   
        data['isBuy'] = request.data['isBuy']
        ticker = Symbol.objects.get(pk=request.data['symbolID']).ticker
        price=yf.Ticker(ticker).info["currentPrice"]
        data['price'] = round((float)(price),10)
        data['total'] = round((data['price'] * (float)(data['volume'])),10)
        try:
            data['transactionDateTime'] = request.data['transactionDateTime']
        except:
            pass
        stockTransactionsSerializer = StockTransactionSerializer(data=data)
        if stockTransactionsSerializer.is_valid():
            portfolioResponse = PortfolioValueViewSet.updatePortfolio(data)
            if portfolioResponse == True:
                stockTransactionsSerializer.save()
                return JsonResponse({'message':"Stock Transaction inserted successfully. "})
            else:
                return JsonResponse({'message':"Stock Transaction insertion failed."})
        else:            
            print(stockTransactionsSerializer.errors)
            return JsonResponse({'message':"Stock Transaction insertion failed."})
        
    def deleteStockTransaction(self, request):
        transactionID = request.GET.get('transactionID','')
        transaction = StockTransaction.objects.get(pk = transactionID)
        transaction.delete()
        return JsonResponse({'message':"Stock Transaction deleted successfully."})



class PortfolioValueViewSet(viewsets.ViewSet):
    def getAllEntries(self, request):
        transactions = PortfolioValue.objects.all()
        portfolioValueSerializer = PortfolioValueSerializer(transactions, many=True)
        return JsonResponse(portfolioValueSerializer.data,safe=False)
    
    def getEntriesWithFullDetails(self,request):
        transactions = PortfolioEntry.objects.all()
        portfolioEntrySerializer = PortfolioEntrySerializer(transactions, many=True)
        return JsonResponse(portfolioEntrySerializer.data,safe=False)
    
    def updatePortfolio(stockTransaction):
        try:
            entry = PortfolioValue.objects.get(symbolID=stockTransaction['symbolID'])
            detailedEntry = PortfolioEntry.objects.get(symbolID=stockTransaction['symbolID'])
        except:
            entry = None
            detailedEntry = None
        
        if stockTransaction['isBuy'] == 'False':
            if entry == None or entry.totalVolume<(int)(stockTransaction['volume']):
                print((int)(stockTransaction['volume']))
                print(entry.totalVolume)
                return False #"Sell failure, attempting to sell more than the available quantity."
            entry.totalVolume -= (int)(stockTransaction['volume'])
            entry.totalPrice -= (Decimal)(stockTransaction['volume']) * (Decimal)(stockTransaction['price'])
            detailedEntry.totalVolume -= (int)(stockTransaction['volume'])
            detailedEntry.totalPrice -= (Decimal)(stockTransaction['volume']) * (Decimal)(stockTransaction['price'])
            if entry.totalVolume == 0:
                entry.delete()
                detailedEntry.delete()
            else:
                entry.save()
                detailedEntry.save()
            UserAccountViewSet.updateCashBalance(stockTransaction['total'],True)
            UserAccountViewSet.updateStockBalance(-stockTransaction['total'])
            return True #"Stock sold successfully."   
        elif entry != None:
            entry.totalVolume += (int)(stockTransaction['volume'])
            entry.totalPrice += (Decimal)(entry.totalVolume) * (Decimal)(stockTransaction['price'])
            detailedEntry.totalVolume += (int)(stockTransaction['volume'])
            detailedEntry.totalPrice += (Decimal)(entry.totalVolume) * (Decimal)(stockTransaction['price'])
            if UserAccountViewSet.updateCashBalance(stockTransaction['total'],False):
                entry.save()      
                detailedEntry.save()          
                UserAccountViewSet.updateStockBalance(stockTransaction['total'])
                return True #"Portfolio entry updated successfully."
            else:
                return False #"Portfolio entry update failed due to insufficient funds."
        else:
            data = dict()
            data['symbolID'] = stockTransaction['symbolID']
            data['totalPrice'] = stockTransaction['total']
            data['totalVolume'] = stockTransaction['volume']
            symbol = Symbol.objects.get(pk=data['symbolID'])
            data['ticker'] = symbol.ticker
            data['full_name'] = symbol.full_name
            portfolioValueSerializer = PortfolioValueSerializer(data=data)
            portfolioEntrySerializer = PortfolioEntrySerializer(data=data)
            if portfolioValueSerializer.is_valid() and UserAccountViewSet.updateCashBalance(data['totalPrice'],False) and portfolioEntrySerializer.is_valid():
                portfolioValueSerializer.save()
                portfolioEntrySerializer.save()
                UserAccountViewSet.updateStockBalance(data['totalPrice'])
                return "Portfolio entry created successfully."
            else:
                return "Portfolio entry creation failed."



class AccountTransactionViewSet(viewsets.ViewSet):
    def getAll(self,request):
        transactionID = request.GET.get('accountTransactionID','')
        if transactionID != '':
            transaction = get_list_or_404(AccountTransaction,pk=transactionID)
            accountTransactionSerializer = AccountTransactionSerializer(transaction, many=True)
        else:
            transactions = AccountTransaction.objects.all()
            accountTransactionSerializer = AccountTransactionSerializer(transactions, many=True)            
        return JsonResponse(accountTransactionSerializer.data,safe=False)
    
    def deleteTransaction(self,request):
        transactionID = request.GET.get('accountTransactionID','')
        transaction = AccountTransaction.objects.get(pk = transactionID)
        transaction.delete()
        return JsonResponse({'message':"Account Transaction deleted successfully."})
    
    def addTransaction(self,request):
        print(request.data)
        accountTransactionSerializer = AccountTransactionSerializer(data=request.data)
        if accountTransactionSerializer.is_valid() and UserAccountViewSet.updateCashBalance((Decimal)(request.data['total']),request.data['isFundingTransaction']=='True'):
            accountTransactionSerializer.save()
            return JsonResponse({'message':"Account Transaction inserted successfully."})
        else:            
            return JsonResponse({'message':"Account Transaction insertion failed."})



class UserAccountViewSet(viewsets.ViewSet):
    def getAccount(self, request):        
        userAccounts = UserAccount.objects.get(pk=1)
        userAccountSerializer = UserAccountSerializer(userAccounts)
        return JsonResponse(userAccountSerializer.data, safe=False)
    
    def addAccount(self, request):
        userAccountSerializer = UserAccountSerializer(data=request.data)
        if userAccountSerializer.is_valid():
            userAccountSerializer.save()
            return JsonResponse({'message':"User Account created successfully."})
        else:            
            return JsonResponse({'message':"User Account creation failed."})
        
    def deleteAccount(self, request):
        userID = request.GET.get('userID','')
        account = UserAccount.objects.get(pk = userID)
        account.delete()
        return JsonResponse({'message':"User Account deleted successfully."})

    def updateName(self,request):
        userID = request.PATCH.get('userID','')
        account = UserAccount.objects.get(pk=userID)
        account.fullname=request.data['fullname']
        account.save()
        return JsonResponse({'message':"Name updated successfully."})
    
    def updateStockBalance(amount):
        account = UserAccount.objects.get(pk=1)
        account.stockBalance+=(Decimal)(amount)
        account.save()
        return "Stock Balance updated."
    
    def updateStockBalanceAPI(self,request):
        account = UserAccount.objects.get(pk=1)
        account.stockBalance+=(Decimal)(request.data['amount'])
        account.save()
        return "Stock Balance updated."

    def updateCashBalance(amount,isFund):
        account = UserAccount.objects.get(pk=1)
        if not isFund:
            if account.cashBalance < (Decimal)(amount):
                return False
            account.cashBalance -= (Decimal)(amount)
        else:
            account.cashBalance += (Decimal)(amount)
        account.save()
        return True



class CurrentStockPriceViewSet(viewsets.ViewSet):
    def getAll(self,request):
        symbolID = request.GET.get('symbolID','')
        if symbolID != '':
            stockPrice = get_list_or_404(CurrentStockPrice,pk=symbolID)
            currentStockPriceSerializer = CurrentStockPriceSerializer(stockPrice, many=True)
        else:
            stockPrices = CurrentStockPrice.objects.all()
            currentStockPriceSerializer = CurrentStockPriceSerializer(stockPrices, many=True)
        return JsonResponse(currentStockPriceSerializer.data,safe=False)
    
    def updatePrice(symbolID):
        stockPrice = CurrentStockPrice.objects.get(symbolID=symbolID)
        ticker = Symbol.objects.get(pk=symbolID).ticker
        price = yf.Ticker(ticker).info["currentPrice"]
        stockPrice.currentPrice = price
        stockPrice.save()
        return "Price updated."
    
    def addSymbol(data):
        currentStockPriceSerializer = CurrentStockPriceSerializer(data=data)
        if currentStockPriceSerializer.is_valid():
            currentStockPriceSerializer.save()
            return "succ"
        else:
            return "err"





class yFinanceViewSet(viewsets.ViewSet):
    def getCurrentPriceByTicker(self,request):
        ticker = request.GET.get('ticker','')
        try:
            symbol = Symbol.objects.get(ticker=ticker)
            CurrentStockPriceViewSet.updatePrice(symbol.symbolID)
        except:
            stock = yf.Ticker(ticker).info
            data = dict()
            data['ticker'] = ticker
            data['full_name'] = stock['longName']
            data['currentPrice'] = stock['currentPrice']
            symbolsSerializer = SymbolSerializer(data=data)
            if symbolsSerializer.is_valid():
                symbolsSerializer.save()
            symbol = Symbol.objects.get(ticker=ticker)   
            data['symbolID'] = symbol.symbolID         
            CurrentStockPriceViewSet.addSymbol(data) 
        stockPrice = CurrentStockPrice.objects.get(pk=symbol.symbolID)
        data = dict()
        data['full_name'] = symbol.full_name
        data['ticker'] = symbol.ticker
        data['symbolID'] = symbol.symbolID
        data['stockPriceID'] = stockPrice.stockPriceID
        data['currentPrice'] = stockPrice.currentPrice
        data['currentDateTime'] = stockPrice.currentDateTime
        return JsonResponse(data)

    def updateStock(self,request):
        stringList = request.data['symbolIDs']
        stringList= stringList[1:len(stringList)-1]
        ids = map(int,stringList.split(','))
        for symbolID in ids:
            symbol = Symbol.objects.get(pk=symbolID)
            ticker = symbol.ticker
            updatedInfo = yf.Ticker(ticker)
            price = updatedInfo.info["currentPrice"]
            name = updatedInfo.info["longName"]
            symbol = Symbol.objects.get(pk=symbolID)
            symbol.full_name = name
            symbol.save()
            stockPrice = CurrentStockPrice.objects.get(symbolID=symbolID)
            stockPrice.currentPrice = price
            stockPrice.save()
        return "Successfully updated stocks info."
'''
    def initializeData(self,request):
        tickers = pd.read_csv("list of tickers.csv")
        tickers = tickers[["Symbol","Name"]]
        tickers['Price']= ''
        x=-1
        for ticker in tickers["Symbol"]:
            x+=1
            try:
                stock = yf.Ticker(ticker)    
                price = stock.info["currentPrice"]
                tickers['Price'][x]=price
            except:
                pass
        tickers.index += 1 
        tickers = tickers[tickers['Price'].notna()]
        tickers.to_csv("prices.csv")
        self.loadData(request)
        return JsonResponse({'message':"Databases intitialized."})

    def loadData(self,request): 
        tickers = pd.read_csv("prices.csv")
        tickers = tickers[tickers['Price'].notna()]
        symbol = pd.DataFrame()
        symbol['ticker'] = tickers['Symbol'] 
        symbol['full_name'] = tickers['Name']
        symbol['currentPrice'] = tickers['Price']
        x=1
        for row in symbol.iterrows():
            symbolData = {'ticker': row[1]['ticker'],'full_name': row[1]['full_name']}   
            symbolsSerializer = SymbolSerializer(data=symbolData)
            if symbolsSerializer.is_valid():
                symbolsSerializer.save()
        for row in symbol.iterrows():                   
            priceData = {'symbolID': x,'currentPrice': row[1]['currentPrice']}   
            x+=1          
            currentStockPriceSerializer = CurrentStockPriceSerializer(data=priceData)
            if currentStockPriceSerializer.is_valid():
                currentStockPriceSerializer.save()
        symbol.to_csv("symbol db.csv", index=False)
        return JsonResponse({'message':"Database loaded."})
'''