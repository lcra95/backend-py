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
class ClienteResource(Resource):

    def get(self):
        menu = []
        try:
            datos = Cliente.getAll()
            if datos:
                for row in datos:
                    data = {
                        "id": row.id,
                        "nombre": row.nombre,
                        "id_persona": row.id_persona,
                        "giro": row.giro,
                        "created_at": str(row.created_at),
                        "updated_at": str(row.updated_at),
                        "datos_persona" : Persona.get_data(row.id_persona)
                    }
                    
                    menu.append(data)
                        
            return {  "response":{"data": { "info": menu }}}, 200
            

        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500

    def post(self):
        try:
            # parser = reqparse.RequestParser()
            # parser.add_argument('idPrestador',
            #                     type=str,
            #                     required=True,
            #                     help="Debe indicar id prestador",
                                
            #                     )
            # parser.add_argument('idSucursal',
            #                     type=str,
            #                     required=False,
            #                     help="Debe indicar id Sucursal",
                                
            #                     )   
            # data = parser.parse_args()
            dataJson = request.get_json()
            insert = Cliente.insert(dataJson)
            return insert
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500

class SearchClienteResource(Resource):

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('identificacion',
                                type=str,
                                required=True,
                                help="Debe indicar identificacion",
                                
                                )  
            data = parser.parse_args()
            info = Persona.personaFullInfo(None, None, None, data["identificacion"])
            if info:
                return {"estado": 1,"data":info}
            return {"estado": 0, "msj": "No se encontro la información solicitada"}
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500
    def post(self):
        try:
            msj ="Hola, Son RyPInfo, ¿como puedo ayudarte?"
            bot.send_message(1059755500, msj)
            return 'okis'
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500

    def put(self):
        exist = None
        try:            
            first = 'Hola, que orden deseas consultar'
            r = requests.get(
                'https://api.telegram.org/bot1285646573:AAG8TM4f1ghE9rCU8DoP66s-SWVN63NcFYM/getUpdates')
            
            info = r.json()
            for x in info["result"]:

                orden = x["message"]["text"].split(" ")
                if len(orden) > 1:
                    if orden[1]:
                        try:
                            exist = Orden.ordenFullInfo(orden[1])
        
                        except Exception as e:
                            print (e)

                        if exist:
                            first ="Nombre= " + str(exist[0]["nombre"]) +" \n"
                            first +="Teléfono= " + str(exist[0]["telefono"]) +" \n"
                            first +="Dirección= " + str(exist[0]["direccion"]) +" \n"
                            llamar = exist[0]["telefono"]
                        if orden[0] == 'o' or orden[0] == 'O' and exist:
                            indicador = x["message"]["from"]["id"]
                            respondido = Telegram.get_data(x["update_id"])
                            
                            if not respondido:
                                bot.send_message(indicador, first)
                                bot.send_message(indicador, llamar)
                                ins = {
                                    "id_update" : x["update_id"],
                                    "id_chat" : x["message"]["from"]["id"]
                                }
                                Telegram.insert(ins)

            return r.json()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500