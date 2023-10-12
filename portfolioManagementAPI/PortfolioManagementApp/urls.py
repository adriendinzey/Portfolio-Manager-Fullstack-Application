from django.urls import path

from PortfolioManagementApp import views

urlpatterns = [
    path('symbol/',views.SymbolViewSet.as_view({'get': 'getAll','delete': 'deleteSymbol'})),
    path('symbol/ticker/',views.SymbolViewSet.as_view({'get': 'getByTicker'})),
    path('symbol/fullname/',views.SymbolViewSet.as_view({'get': 'getByFullname'})),    
    path('symbol/create/symbol/',views.SymbolViewSet.as_view({'post': 'addSymbol'})),
    path('stocktransaction/',views.StockTransactionViewSet.as_view({'get': 'getAll','delete': 'deleteStockTransaction','post': 'addStockTransaction'})),
    path('portfoliovalue/',views.PortfolioValueViewSet.as_view({'get': 'getAllEntries'})),
    path('portfoliovalue/portfolioentry/',views.PortfolioValueViewSet.as_view({'get': 'getEntriesWithFullDetails'})),
    path('accounttransaction/',views.AccountTransactionViewSet.as_view({'get': 'getAll','post':'addTransaction','delete': 'deleteTransaction'})),
    path('useraccount/',views.UserAccountViewSet.as_view({'get': 'getAccount','post':'addAccount','delete': 'deleteAccount', 'patch':'updateName'})),
    path('useraccount/portfoliobalance/',views.UserAccountViewSet.as_view({'patch':'updateStockBalanceAPI'})),
    path('currentstockprice/',views.CurrentStockPriceViewSet.as_view({'get':'getAll'})),
    path('yfinance/',views.yFinanceViewSet.as_view({'get': 'getCurrentPriceByTicker','patch':'updateStock'})),
    path('yfinance/initSymbolAndPriceDB/',views.yFinanceViewSet.as_view({'get':'initializeData'})),
    path('yfinance/loadSymbolAndPriceDB/',views.yFinanceViewSet.as_view({'get':'loadData'})),
]