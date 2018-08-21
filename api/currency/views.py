# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import TbCurrency, TbExchange
from .serializers import CurrencySerializer, ExchangeSerializer


@api_view(['GET'])
def index(request):
    currency = TbCurrency.objects.all()
    if request.GET:
        currency = TbCurrency.objects.filter(tanggal=request.GET['date'])

    serializers = CurrencySerializer(currency, many=True)
    return Response(serializers.data)

@api_view(['GET','POST'])
def price(request):

    if request.method == 'GET':

        # currency = TbCurrency.objects.all().values()
        #
        # if request.GET:
        #     currency = TbCurrency.objects.filter(tanggal=request.GET['date'])

        data = {}
        #for i in range(len(currency)):
            # print(currency[i].c_from)

            # get exchange detail
            # exchange_data = TbExchange.objects.filter(id=currency[i].exchange_id)

            # get 7 day average rate


            # data[int(i)] = {
            #     "date": currency[i].tanggal,
            #     "from": exchange_data[0].c_from,
            #     "to": exchange_data[0].c_to,
            #     "rate": currency[i].rate
            # }


        # serializers = CurrencySerializer(currency, many=True)
        # return Response(JSONRenderer().render(serializers.data), status=status.HTTP_200_OK)
        sql = "SELECT c.tanggal, c.rate, e.c_from, e.c_to, e.id FROM tb_exchange AS e LEFT JOIN tb_currency AS c ON e.id = c.exchange_id"
        if request.GET:
            sql = "SELECT c.tanggal, c.rate, e.c_from, e.c_to, e.id FROM tb_exchange AS e LEFT JOIN tb_currency AS c ON e.id = c.exchange_id WHERE c.tanggal = '%s'" % (request.GET['date'])

        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()

        data = {}
        for i in range(len(row)):
            # count 7 days average
            count = TbCurrency.objects.filter(exchange_id=row[i][4]).order_by('-tanggal').count()
            # print(count)
            data_avg = "insufficient data"
            if count >= 6:
                data_avg = TbCurrency.objects.filter(exchange_id=row[i][4]).order_by('-tanggal')[:7]

                data_avg_tmp = 0
                for rate in data_avg:
                    data_avg_tmp = data_avg_tmp + int(rate.rate)

                data_avg = data_avg_tmp/7

            if row[i][0] is None:
                d_tanggal = "insufficient data"
            else:
                d_tanggal = row[i][0]

            if row[i][1] is None:
                d_rate = "insufficient data"
            else:
                d_rate = row[i][0]

            data[int(i)] = {
                "date": d_tanggal,
                "from": row[i][2],
                "to": row[i][3],
                "rate": d_rate,
                "avg7days": data_avg
            }

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        #check exchange list if exist
        list_exchange = TbExchange.objects.filter(c_from=request.data['c_from'], c_to=request.data['c_to'])
        if list_exchange:
            append_data = {"exchange_id":list_exchange[0].id}
            append_data.update(request.data)
            serializer = CurrencySerializer(data=append_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                warn = {"error": "Not Valid Parameters !"}
                return Response(warn, status=status.HTTP_400_BAD_REQUEST)

        else:
            warn = {"error": "Exchange list Not Found, Add Exchange List First !"}
            return Response(warn, status=status.HTTP_400_BAD_REQUEST)

    else:
        Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['POST','DELETE'])
def exchange(request, c_from=None, c_to=None):

    try:
        exchange = TbExchange.objects.filter(c_from=c_from, c_to=c_to)
    except exchange.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = ExchangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        exchange.delete()
        return Response(status=status.HTTP_200_OK)

    else:
        Response(status=status.HTTP_403_FORBIDDEN)
