#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Orden import Orden
from aplicacion.modelos.Sucursal import Sucursal
from aplicacion.modelos.Persona import Persona
from aplicacion.modelos.TipoEntrega import TipoEntrega
from aplicacion.modelos.OrdenRepartidor import OrdenRepartidor
from aplicacion.modelos.PersonaDireccion import PersonaDireccion
from aplicacion.modelos.OrdenDetalle import OrdenDetalle
from aplicacion.modelos.OrdenPago import OrdenPago
from aplicacion.modelos.Telefono import Telefono
from aplicacion.modelos.Correo import Correo
from aplicacion.modelos.Documento import Documento
from datetime import date, datetime
from random import random
from aplicacion.telegram import bot
class OrdenResource(Resource):

    def get(self):
        menu = []
        try:
            datos = Orden.getAll()
            if datos:
                for row in datos:
                    sucursal = Sucursal.get_data(row.id_sucursal)
                    data = {
                        "id": row.id,
                        "id_persona": row.id_persona,
                        "id_sucursal": row.id_sucursal,
                        "id_creador": row.id_creador,
                        "id_direccion": row.id_direccion,
                        "id_tipo_entrega": row.id_tipo_entrega,
                        "hora_recepcion": str(row.hora_recepcion),
                        "hora_salida": str(row.hora_salida),
                        "created_at": str(row.created_at),
                        "updated_at": str(row.updated_at),
                        "datos_sucursal" : sucursal,
                        "empresa_full_data" : Persona.get_data(sucursal[0]["id_cliente"]),
                        "datos_creador" : Persona.get_data(row.id_creador),
                        "datos_tipo_entrega" : TipoEntrega.get_data(row.id_tipo_entrega),
                        "datos_cliente": Persona.get_data(row.id_persona),
                        "direccion_cliente" : PersonaDireccion.DireccionByPersona(row.id_persona),
                        "telefono_cliente" : Telefono.get_data_by_persona(row.id_persona),
                        "correo_cliente" : Correo.get_data_by_persona(row.id_persona),
                        "datos_repartidor" : OrdenRepartidor.RepartidorByOrden(row.id),
                        "detalle_orden" : OrdenDetalle.DetalleByOrden(row.id)
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

            documento = 39
            fecha_emision = datetime.now()
            id_comprador = None
            estado = 2
            dataJson = request.get_json()
            if 'id_tipo_documento' in dataJson and dataJson["id_tipo_documento"]:
                documento = dataJson["id_tipo_documento"]
            if 'fecha_emision' in dataJson and dataJson["fecha_emision"]:
                fecha_emision = dataJson["fecha_emision"]
            if 'id_comprador' in dataJson and dataJson["id_comprador"]:
                id_comprador = dataJson["id_comprador"]
            
            jsonOrden = {
                "id_persona" : dataJson["id_persona"],
                "id_creador" : dataJson["id_creador"],
                "id_tipo_entrega" : dataJson["id_tipo_entrega"],
                "id_sucursal" : dataJson["id_sucursal"],
                "id_direccion" : dataJson["id_direccion"],           
                "hora_salida" : None,  
                "delivery": dataJson["delivery"],
                "kilometros": dataJson["kilometros"]

            }
            insert = Orden.insert(jsonOrden)
            if insert:
                for producto in dataJson["detalle"]:
                    sin =None
                    eleccion = None            
                    if 'detalle' in producto and producto['detalle'] is not None:
                        sin = producto["detalle"]
                    if 'eleccion' in producto and producto['eleccion'] is not None:
                        eleccion = producto["eleccion"]

                    jsonOrdenDetalle = {
                        "id_orden": insert,
                        "id_producto": producto['id'],
                        "cantidad" : producto['cantidad'],
                        "detalle" : sin,
                        "eleccion": eleccion,
                        "precio_unitario" :  producto['precio'],
                        "precio_extendido" :  producto['precio_bruto'],
                        "precio_total" : producto['sub_total'],
                        "precio_iva" : producto['iva']
                    }
                    insertDetalle = OrdenDetalle.insert(jsonOrdenDetalle)
                if "estado" in dataJson["pago"]:
                    estado = dataJson["pago"]['estado']

                if dataJson["pago"]['id_tipo_pago'] == 1 or dataJson["pago"]['id_tipo_pago'] == "1":
                    estado = 3

                if 'vuelto' not in dataJson["pago"] or dataJson["pago"]["vuelto"] is None:
                    vuelto = 0
                else:
                    vuelto = dataJson["pago"]['vuelto']

                jsonOrdenPago = {
                    "id_orden" : insert,
                    "id_tipo_pago" : dataJson["pago"]['id_tipo_pago'],
                    "monto":  dataJson["pago"]['monto'],
                    "voucher" : dataJson["pago"]['voucher'],
                    "comprobante" : dataJson["pago"]['comprobante'],
                    "vuelto" : vuelto,
                    "estado" : estado
                }

                insertOrdenPago = OrdenPago.insert(jsonOrdenPago)

                jsonDocumento = {
                    "folio" : 84555,
                    "id_orden": insert,
                    "id_tipo_documento" : documento,
                    "fecha_emision" : fecha_emision,
                    "estado": 1,
                    "id_persona" : id_comprador
                }
                insertDocu = Documento.insert(jsonDocumento)

                return {"estado" : 1, "orden" : insert}
                
            return {"estado" : 0, "msj": "Ha ocurrido un error"}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj)},500
    def put(self):
        try:
           
            dataJson = request.get_json()      
            edit = Orden.update_data(dataJson["id"], dataJson)
            if edit:
                return {"estado" : 1, "orden" : edit}
               
            return {"estado" : 0, "msj": "Ha ocurrido un error"}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj)},500


# class PagoOnLineResource(Resource):
#     def post(self):
#         try:
#             dataJson = request.get_json()
#             print("###################### ladata #######################")
#             print (dataJson)
#             print("###################### ladata #######################")
#             return dataJson
#         except Exception as e:
#             print(" ## Error ## \n")
#             print(e)
#             print("\n")
#             return {"message": "Ha ocurrido un error de conexión."}, 500      
class OrdenFullResource(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('fecha',
                                type=str,
                                required=True,
                                help="Debe indicar id prestador",
                                
                                )
            parser.add_argument('id_sucursal',
                                type=str,
                                required=True,
                                help="Debe indicar id prestador",
                                
                                )
            parser.add_argument('estado',
                                type=str,
                                required=True,
                                help="Debe indicar id prestador",
                                
                                )
            data = parser.parse_args()
            Info = Orden.ordenFullInfoData(data["id_sucursal"], data["fecha"], data["estado"])

            return Info
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500      
class notificaOrdenResourse(Resource):
    def post(self):
        try:
            ordenes = Orden.ordenToNotify()
            if len(ordenes) > 0:
                for x in ordenes:
                    msj ="Hola, tienes una orden pendiente por atender "
                    msj+="https://rypsystems.cl/imprimir-orden/"+str(x["id"])+"?api_key=tPWoZWD8v3ezld1yomtesvGRCKqtoDAgHGWYVL2O"
                    bot.send_message(5036077655, msj)
                    bot.send_message(5090328284, msj)

                    Orden.update_data(x["id"], {"informada": 1})
                    
            return ordenes
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500      