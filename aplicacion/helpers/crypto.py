#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Cliente import Cliente
from aplicacion.modelos.Persona import Persona
from aplicacion.telegram import bot
from aplicacion.modelos.Teleg import Telegram
import requests
from aplicacion.modelos.Orden import Orden
from datetime import date, datetime
from cryptomarket.client import Client, args
from cryptomarket.exceptions import CryptomarketSDKException




# get currencies


baseUrl = "https://api.exchange.cryptomkt.com/api/3" #PROD
#baseUrl = "https://webpay3gint.transbank.cl" #QA

class CryptoMarcket():
    @staticmethod
    def credenciales():
        api_key='dxLG5WJEHgGHOH9F2pDD9isxA0NHHMAM'
        api_secret='AHuGK94clpEeS06NhPXAoYwxUTnSfoNl'
        client = Client(api_key, api_secret) 
        return client
    
    @staticmethod
    def rateCryto():
        junta = ","
        currencies = ''
        balance = CryptoMarcket.account_balance()
        arr = []
        for x in balance:
            if x["currency"] != 'CLP':
                arr.append(x["currency"])
                currencies = junta.join(arr)
    
        url = baseUrl + f'/public/price/rate?from={currencies}&to=CLP'
        r = requests.request("GET", url )
        res = r.json()
        total = 0
        for y in balance:
            if y["currency"] in res:
                y["price"] = res[y["currency"]]["price"]
                y["CLP"] = round(float(y["available"]) * float(y["price"]))
                total = total + y["CLP"]
        
        return {"balance": balance, "Total_CLP" : total }

    @staticmethod
    def account_balance():
        cliente = CryptoMarcket.credenciales()
        account_balance = cliente.get_account_balance()
        temp = []
        for x in account_balance:
            if float(x["available"]) > 0:
                # cliente.transfer_money_from_bank_balance_to_trading_balance(x["currency"],x["available"])
                temp.append(x)
        
        return temp
    @staticmethod
    def trading_balance():
        cliente = CryptoMarcket.credenciales()
        trading_balance = cliente.get_trading_balance()
        temp = []
        for x in trading_balance:
            if float(x["available"]) > 0:
                cliente.transfer_money_from_trading_balance_to_bank_balance(x["currency"],x["available"])
                temp.append(x)
        
        return { "balance" : temp}
    @staticmethod
    def currencies():
        cliente = CryptoMarcket.credenciales()
        currencies = cliente.get_currencies()

        
        return { "currencies" :currencies}
    @staticmethod
    def order():
        cliente = CryptoMarcket.credenciales()
        currencies = cliente.create_order('ETHCLP', 'buy', '0.0017201', order_type=args.ORDER_TYPE.MARKET)

        

        return { "currencies" :currencies}
    
    @staticmethod
    def banktoExchange():
        cliente = CryptoMarcket.credenciales()
        currencies = cliente.transfer_money_from_bank_balance_to_trading_balance('CLP', '3000')

        

        return { "currencies" :currencies}
    @staticmethod
    def exchangetoBank():
        cliente = CryptoMarcket.credenciales()
        currencies = cliente.transfer_money_from_trading_balance_to_bank_balance('CLP', '2360')

        

        return { "currencies" :currencies}

