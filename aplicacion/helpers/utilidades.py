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

    @staticmethod
    def send_mail(email_destino, asunto, body_mensaje, adjunto=None):

        try:
            msg = MIMEMultipart('alternative')
            msg.set_charset('utf8')
            msg['Subject'] = asunto
            msg['From'] = "requenalc@gmail.com"
            msg['To'] = email_destino

            if adjunto is not None:

                if isinstance(adjunto, list):
                    if adjunto is not None:
                        for file_name in adjunto:
                            try:
                                filename = file_name.split("/")[-1]
                                f = file_name
                                with open(f, "rb") as fil:
                                    part = MIMEApplication(
                                        fil.read(),
                                        Name=basename(f)
                                    )
                                part.add_header(
                                    'Content-Disposition', 'attachment', filename=filename)
                                msg.attach(part)
                            except Exception as e:
                                print(e)
                else:
                    f = adjunto
                    with open(f, "rb") as fil:
                        part = MIMEApplication(
                            fil.read(),
                            Name=basename(f)
                        )
                    # After the file is closed
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(
                        f)
                    msg.attach(part)

            html_tmp = MIMEText(body_mensaje, 'html')
            msg.attach(html_tmp)

            # server = smtplib.SMTP('smtp-relay.sendinblue.com', 587)  # 587 - 25
            # server.login("requenalc@gmail.com",
            #              "VMtZGQgHXaCzJh1r")
            # rs = server.sendmail("requenalc@gmail.com",
            #                      email_destino, msg.as_string().encode("utf8"))
            server = smtplib.SMTP('smtp.sendgrid.net', 587)  # 587 - 25
            server.login("apikey",
                         "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")
            rs = server.sendmail("requenalc@gmail.com",
                                 email_destino, msg.as_string().encode("utf8"))

            server.quit()

            return True

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # exc_type, fname, exc_tb.tb_lineno
            msj = "Error: " + str(exc_obj) + " File: " + \
                fname + " linea: " + str(exc_tb.tb_lineno)
            print(msj)
            return False
