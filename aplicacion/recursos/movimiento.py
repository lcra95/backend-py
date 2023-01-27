#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.movimiento import Movimiento

from datetime import date, datetime
from random import random

class MovimientoResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fecha_ini',
                            type=str,
                            required=True,
                            help="Debe indicar una fecha",
                            
                            )
        parser.add_argument('fecha_fin',
                            type=str,
                            required=False,
                            help="Debe indicar id Sucursal",
                            
                            )   
        parser.add_argument('tipo_movimiento',
                            type=str,
                            required=False,
                            help="Debe indicar id Sucursal",
                            
                            )   
        data = parser.parse_args()
        menu = []
        try:
            datos = Movimiento.get_data_fecha(data["fecha_ini"], data["fecha_fin"], data["tipo_movimiento"])
            
                        
            return {  "response":{"data": { "info": datos }}}, 200
            

        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500

    def post(self):
        try:
           
            dataJson = request.get_json()
            d1 = dataJson
            if "tipo_egreso" in dataJson and  dataJson["tipo_egreso"] is not None and dataJson["id_tipo_movimiento"] == "2":
                print("hello")
                if dataJson["tipo_egreso"] == "1" or dataJson["tipo_egreso"] == 1:
                    valor = Movimiento.insert(dataJson)                    
                    if valor:
                       return {"estado": 1, "msj": "registro Exitoso"}
                
                elif dataJson["tipo_egreso"] == "2" or dataJson["tipo_egreso"] == 2:
                    ins1 = {
                        "fecha" :dataJson["fecha"],
                        "monto" :dataJson["monto"] * 0.3,
                        "id_centro_costo" :dataJson["id_centro_costo"],
                        "id_tipo_movimiento" :dataJson["id_tipo_movimiento"],
                        "concepto" :dataJson["concepto"],
                    }                    
                    ins2 = {
                        "fecha" :dataJson["fecha"],
                        "monto" :dataJson["monto"] * 0.7,
                        "id_centro_costo" : 7 ,
                        "id_tipo_movimiento" :dataJson["id_tipo_movimiento"],
                        "concepto" :dataJson["concepto"],
                    }                    

                    valor = Movimiento.insert(ins1)                    
                    valor1 = Movimiento.insert(ins2)                    
                    if valor1:
                       return {"estado": 1, "msj": "registro Exitoso"}

                elif dataJson["tipo_egreso"] == "3" or dataJson["tipo_egreso"] == 3:
                    ins1 = {
                        "fecha" :dataJson["fecha"],
                        "monto" :dataJson["monto"] * 0.5,
                        "id_centro_costo" :dataJson["id_centro_costo"],
                        "id_tipo_movimiento" :dataJson["id_tipo_movimiento"],
                        "concepto" :dataJson["concepto"],
                    }                    
                    ins2 = {
                        "fecha" :dataJson["fecha"],
                        "monto" :dataJson["monto"] * 0.5,
                        "id_centro_costo" : 7 ,
                        "id_tipo_movimiento" :dataJson["id_tipo_movimiento"],
                        "concepto" :dataJson["concepto"],
                    } 
                    valor = Movimiento.insert(ins1)                    
                    valor1 = Movimiento.insert(ins2)                    
                    if valor1:
                       return {"estado": 1, "msj": "registro Exitoso"}       
            
            else:
                valor = Movimiento.insert(dataJson)                    
                if valor:
                    return {"estado": 1, "msj": "registro Exitoso"}

        
        
        
            return {"estado" : 0, "msj": "Ha ocurrido un error"}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj)},500