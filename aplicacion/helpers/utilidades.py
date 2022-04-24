import decimal
import time
import datetime
import base64
import binascii
import requests
import sys
import os
import os.path
import shutil
import re
import json
import smtplib
# import xlsxwriter
from flask import Flask, request, jsonify, render_template, session, redirect, send_from_directory
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from aplicacion.redis import redis
from aplicacion.enviroment import env


# from suds.sax.text import Raw
# from suds.sudsobject import asdict

# from aplicacion.db import db, dbMonitorWs
# from suds.sudsobject import asdict
from email.mime.application import MIMEApplication
from os.path import basename


class Utilidades():

    @staticmethod
    def obtener_datos(query):
        jsonData = []
        if query:
            """
            Esta funcion sirve solo cuando la query es de tipo sql 1 model list  o sql model(first)
            """
            if isinstance(query, list):
                for datos in query:
                    d = {}
                    for column in datos.__table__.columns:
                        data = getattr(datos, column.name)
                        if isinstance(data, bytes):
                            Bi = binascii.hexlify(data)
                            Bi = str(Bi.decode('ascii'))
                            data = Bi
                        if isinstance(data, datetime.datetime):
                            data = Utilidades.formatoFechaHora(data)

                        if isinstance(data, datetime.date):
                            data = Utilidades.formatoFecha(data)

                        d[column.name] = data
                    jsonData.append(d)
            else:
                d = {}
                for column in query.__table__.columns:
                    data = getattr(query, column.name)
                    if isinstance(data, bytes):
                        Bi = binascii.hexlify(data)
                        Bi = str(Bi.decode('ascii'))
                        data = Bi
                    if isinstance(data, datetime.datetime):
                        data = Utilidades.formatoFechaHora(data)
                    if isinstance(data, datetime.date):
                        data = Utilidades.formatoFecha(data)
                    d[column.name] = data
                jsonData.append(d)
        return jsonData

    @staticmethod
    def formatoFechaHora(fecha):
        return str(fecha.strftime("%d-%m-%Y %H:%M"))

    @staticmethod
    def formatoFecha(fecha):
        dia = str(fecha.day)
        dia = "0"+dia if len(dia) == 1 else dia
        mes = str(fecha.month)
        mes = "0"+mes if len(mes) == 1 else mes
        anio = str(fecha.year)

        fechaFormateada = dia + "-" + mes + "-" + anio
        return fechaFormateada
