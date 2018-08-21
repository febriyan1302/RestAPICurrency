from rest_framework import serializers
from .models import TbCurrency, TbExchange

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbExchange
        fields = ('id', 'c_from', 'c_to')

class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = TbCurrency
        fields = ('rate', 'tanggal', 'exchange_id')