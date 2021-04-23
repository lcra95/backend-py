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

            valor = Movimiento.insert(dataJson)                    
            if valor:
                return {"estado": 1, "msj": "registro Exitoso"}

            return {"estado" : 0, "msj": "Ha ocurrido un error"}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj)},500