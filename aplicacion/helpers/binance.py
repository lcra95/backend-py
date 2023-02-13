#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.telegram import bot
from aplicacion.modelos.Teleg import Telegram
import requests
from aplicacion.modelos.Orden import Orden
from datetime import date, datetime


class Binance():
    
    @staticmethod
    def credenciales():
        credentials ={
                        "url" : "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search",
                        "apiKey": "X3mF4XZj3aZEbeQHrXxA0a5Ll10BVK763RiOksF1L1xEjRa9Jfjvu1HjA0jwcElW",
                        "secretKey": "TcTjrTinyFoWyDa5IaOViWsmu4gHQMBhUzuhkbzji2gp0OAU3YRmpWNlV88F65cd",
                        "comment": "gestionTasa"
                    }
        
        return credentials
    

    staticmethod
    def consulta_bs(bs = None):
        if bs is None:
            bs = 500
        import http.client

        conn = http.client.HTTPSConnection("p2p.binance.com")

        payload = {
            "proMerchantAds": False,
            "page": 1,
            "rows": 1,
            "payTypes": ["BancoDeVenezuela"
            ],
            "countries": [],
            "publisherType": "merchant",
            "transAmount": str(bs),
            "asset": "USDT",
            "fiat": "VES",
            "tradeType": "SELL"
        }

        headers = {
            'cookie': "cid=1mnKK17m",
            'authority': "p2p.binance.com",
            'accept': "*/*",
            'accept-language': "es-CL,es-419;q=0.9,es;q=0.8",
            'bnc-uuid': "9d0e0910-7aac-49fd-aab1-437d4f1097f8",
            'c2ctype': "c2c_merchant",
            'clienttype': "web",
            'content-type': "application/json",
            'lang': "es",
            'origin': "https://p2p.binance.com",
            'referer': "https://p2p.binance.com/es/trade/sell/USDT?fiat=VES&payment=BancoDeVenezuela",
            'sec-ch-ua': "^\^Not?A_Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^108^^, ^\^Google",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "^\^Windows^^",
            'sec-fetch-dest': "empty",
            'sec-fetch-mode': "cors",
            'sec-fetch-site': "same-origin",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }

        conn.request("POST", "/bapi/c2c/v2/friendly/c2c/adv/search", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read()

        return json.loads(data)
    staticmethod
    def consulta_clp(clp = None):
        if clp is None:
            clp = 20000

        print(clp)
        import http.client

        conn = http.client.HTTPSConnection("p2p.binance.com")

        payload = {
            "proMerchantAds": False,
            "page": 1,
            "rows": 1,
            "payTypes": [],
            "countries": [],
            "publisherType": None,
            "transAmou": str(int(clp)),
            "asset": "USDT",
            "fiat": "CLP",
            "tradeType": "BUY"
        }
        print(payload)
        headers = {
            'cookie': "cid=1mnKK17m",
            'authority': "p2p.binance.com",
            'accept': "*/*",
            'accept-language': "es-CL,es-419;q=0.9,es;q=0.8",
            'bnc-uuid': "9d0e0910-7aac-49fd-aab1-437d4f1097f8",
            'c2ctype': "c2c_merchant",
            'clienttype': "web",
            'content-type': "application/json",
            'lang': "es",
            'origin': "https://p2p.binance.com",
            'referer': "https://p2p.binance.com/es/trade/all-payments/USDT?fiat=CLP",
            'sec-ch-ua': "^\^Not?A_Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^108^^, ^\^Google",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "^\^Windows^^",
            'sec-fetch-dest': "empty",
            'sec-fetch-mode': "cors",
            'sec-fetch-site': "same-origin",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }

        conn.request("POST", "/bapi/c2c/v2/friendly/c2c/adv/search", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read()

        return json.loads(data)
    def consulta_eth():

        import http.client

        conn = http.client.HTTPSConnection("p2p.binance.com")

        payload = {
            "proMerchantAds": False,
            "page": 1,
            "rows": 1,
            "payTypes": [],
            "countries": [],
            "publisherType": None,
            "transAmount": "",
            "asset": "ETH",
            "fiat": "CLP",
            "tradeType": "SELL"
        }

        headers = {
            'cookie': "cid=1mnKK17m",
            'authority': "p2p.binance.com",
            'accept': "*/*",
            'accept-language': "es-CL,es-419;q=0.9,es;q=0.8",
            'c2ctype': "c2c_merchant",
            'clienttype': "web",
            'content-type': "application/json",
            'lang': "es",
            'origin': "https://p2p.binance.com",
            'referer': "https://p2p.binance.com/es/trade/sell/ETH?fiat=CLP&payment=ALL",
            'sec-ch-ua': "^\^Not_A",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "^\^Windows^^",
            'sec-fetch-dest': "empty",
            'sec-fetch-mode': "cors",
            'sec-fetch-site': "same-origin",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
            }

        conn.request("POST", "/bapi/c2c/v2/friendly/c2c/adv/search", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read()

        return json.loads(data)