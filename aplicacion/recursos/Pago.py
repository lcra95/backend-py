#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Pago import Pago

class PagoResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',
                                type=str,
                                required=True,
                                help="Debe indicar una fecha",
                                
                                )
        
        data = parser.parse_args() 
        menu = []
        try:
            datos = Pago.get_data(data["id"])
            print(datos)
            # if datos:
            #     for row in datos:
            #         data = {
            #             "id": row.id,
            #             "monto": row.monto,
            #             "estado": row.estado,
            #             "hash": row.hash,
            #             "created_at": str(row.created_at),
            #             "updated_at": str(row.updated_at),
            #         }
                    
            #         menu.append(data)
                        
            return datos, 200
            

        except Exception as e:
            print("=======================E")
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500

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
            insert = Pago.insert(dataJson)
            return insert
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500