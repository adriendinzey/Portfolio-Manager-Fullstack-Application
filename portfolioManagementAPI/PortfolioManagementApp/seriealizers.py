from rest_framework import serializers
from PortfolioManagementApp.models import Symbol, StockTransaction, PortfolioValue, PortfolioEntry, AccountTransaction, UserAccount, CurrentStockPrice

class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ("symbolID",
                "ticker",
                "full_name")
class StockTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransaction
        fields = ("transactionID",
                "symbolID",
                "volume",
                "price",
                "transactionDateTime",
                "total",
                "isBuy")
    
class PortfolioValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioValue
        fields = ("portfolioID",
                "symbolID",
                "totalPrice",
                "totalVolume")
    
class PortfolioEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioEntry
        fields = ("portfolioID",
                "symbolID",
                "totalPrice",
                "totalVolume",
                "ticker",
                "full_name"
                )

class AccountTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTransaction
        fields = ("accountTransactionID",
                "total",
                "currencyCode",
                "isFundingTransaction",
                "transactionDateTime")

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ("userID",
                "fullname",
                "cashBalance",
                "stockBalance")
    
class CurrentStockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentStockPrice
        fields = ("stockPriceID",
                "symbolID",
                "currentPrice",
                "currentDateTime")
    