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
baseUrl = "https://api.exchange.cryptomkt.com/api/3" #PROD
#baseUrl = "https://webpay3gint.transbank.cl" #QA

class CryptoMarcket():
    @staticmethod
    def credenciales():
        # Prod
        credenciales = {
            "Tbk-Api-Key-Id":"597043648829",
            "Tbk-Api-Key-Secret": "73726a87661cb3b6d8e1663c19a2cd9c"
        }
        # QA
        # credenciales = {
        #     "Tbk-Api-Key-Id":"597055555532",
        #     "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
        # }
        return credenciales

    @staticmethod
    def rateCryto():
               
        url = baseUrl + '/public/price/rate?from=ETH,BTC,SOL,BNB&to=CLP'
    
        r = requests.request("GET", url, )
        res = r.json()
        return res