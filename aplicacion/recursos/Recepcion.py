#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Recepcion import Recepcion
from aplicacion.modelos.RecepcionProducto import RecepcionProducto
from aplicacion.modelos.ProductoStock import ProductoStock

from datetime import date, datetime
from random import random

class RecepcionResource(Resource):

    def get(self):
        menu = []
        try:
            datos = Recepcion.getAll()
            if datos:
                for row in datos:
                    data = {
                        "id": row.id,
                        "id_persona": row.id_tipo_documento,
                        "id_sucursal": row.id_sucursal,
                        "id_creador": row.documento,
                        "id_direccion": row.observacion,
                        
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
            dataJson = request.get_json()
            
            jsonRecepcion = {
                "id_tipo_documento" : dataJson["id_tipo_documento"],
                "id_creador" : dataJson["id_creador"],
                "id_sucursal": dataJson["id_sucursal"],
                "documento": dataJson["documento"],
                "observacion": dataJson["observacion"]
            }
            recepcion = Recepcion.insert(jsonRecepcion)
            if recepcion:
                for prod in dataJson["detalle"]:
                    jsonProd = {
                        "id_producto" : prod["id"],
                        "id_recepcion" : recepcion,
                        "cantidad" : prod["cantidad"],
                        "precio_neto": prod["precio_neto"]
                    }
                    produ = RecepcionProducto.insert(jsonProd)
                    if prod:
                        stock = 0
                        info = ProductoStock.prodSucursalStock(prod["id"], dataJson["id_sucursal"])
                        if len(info) > 0:
                            stock = info[0]["cantidad"]
                            stock = stock + prod["cantidad"]
                            json_updateStock = {
                                "cantidad" : stock
                            }
                            ProductoStock.update_data(info[0]['id'], json_updateStock)
                        else:
                            insertProdStock = {
                                "id_producto": prod["id"],
                                "id_sucursal": dataJson["id_sucursal"],
                                "cantidad" : prod["cantidad"]
                            }
                            ProductoStock.insert(insertProdStock)
                return {"estado": 1, "msj": "Data registrada con exito"}
            return {"estado": 0, "msj": "Ha ocurrido un error"}

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj)},500