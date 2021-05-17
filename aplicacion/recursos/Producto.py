#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Producto import Producto
from aplicacion.modelos.Cliente import Cliente
from aplicacion.modelos.Persona import Persona
from aplicacion.modelos.TipoProducto import TipoProducto
from aplicacion.modelos.ProductoIngrediente import ProductoIngrediente
from aplicacion.modelos.ProductoImagen import ProductoImagen
from aplicacion.modelos.Iva import Iva
from aplicacion.redis import redis
import base64
class ProductoResource(Resource):

    def get(self):
        menu = []
        try:
            datos = Producto.getAll()
            return 'he'
            if datos:
                for row in datos:
                    imagen = ProductoImagen.get_data_id(row.id)

                    iva = Iva.get_data(row.id_iva)
                    fix_iva = row.precio - round(row.precio/iva[0]["valor"],0)
                    fix_precio_bruto = row.precio - fix_iva
                    
                    data = {
                        "id": row.id,
                        "nombre": row.nombre,
                        "id_cliente": row.id_cliente,
                        "id_tipo_producto": row.id_tipo_producto,
                        "precio": row.precio,
                        "cantidad" : 1,
                        "created_at": str(row.created_at),
                        "updated_at": str(row.updated_at),
                        "descripcion" : row.descripcion,
                        "imagen" : imagen[0]['id'],
                        "iva" : int (iva[0]['valor']),
                        "fix_iva" :int(fix_iva),
                        "fix_precio_bruto": fix_precio_bruto
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
            ruta = "/app/backend-py/aplicacion/clients/01/"
            # ruta = app.config['ROOT_PATH']+ '/backend-py/aplicacion/clients/01/'
            
            imagen = "noimage.png"
            if  request.files["imagen"]:
                imagen = request.files["imagen"]
                filename = imagen.filename
                imagen.save(os.path.join(ruta, filename))
                params = request.form.to_dict()
                dataJson = params
                dataJson["imagen"] = imagen.filename
                dataJson["estado"] = 1
            insert = Producto.insert(dataJson)
            if insert:
                if 'imagen' in dataJson and dataJson["imagen"]:
                    imagen = dataJson["imagen"]
                
                jsonImagen = {
                    "imagen": imagen,
                    "id_producto" : insert
                }
                Ima = ProductoImagen.insert(jsonImagen)
                response = {
                    "producto" : insert,
                    "imagen": Ima,
                    "estado": 1,
                    "msj": "Registro exitoso"
                }
                return response
            return {
                "estado": 0,
                "msj": "ha ocurrido un error"
            }
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {"message": msj}, 500

class ProductoDetalleResource(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id',
                                type=str,
                                required=True,
                                help="Debe indicar id producto",
                                
                                )
            data = parser.parse_args()
                     
            Prod = Producto.get_data(data['id'])
            if Prod:  
                iva = Iva.get_data(Prod[0]["id_iva"])
                imagen = ProductoImagen.get_data_id(Prod[0]['id'])
                cliente = Cliente.get_data(Prod[0]['id_cliente'])

                Prod[0]["fix_iva"] =Prod[0]["precio"] - round(Prod[0]["precio"]/iva[0]["valor"],0)
                Prod[0]["cantidad"] = 1
                Prod[0]["fix_iva"] = int (Prod[0]["fix_iva"])
                Prod[0]["fix_precio_bruto"] = int( Prod[0]["precio"] - Prod[0]["fix_iva"])
                Prod[0]['iva'] = int (iva[0]['valor'])
                Prod[0]["cantidad"] = 1
                Prod[0]["datos_cliente"] = cliente,
                Prod[0]["cliente_full_data"] = Persona.get_data(cliente[0]["id_persona"]),
                Prod[0]["datos_tipo_producto"] = TipoProducto.get_data(Prod[0]['id_tipo_producto']),
                Prod[0]["ingredientes"] = ProductoIngrediente.IngredienteByProducto(Prod[0]['id']),
                Prod[0]['imagen'] = imagen[0]['id']
                return Prod
            
            return None
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {"message": msj}, 500
class ProductoFilterResource(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id_cliente',
                                type=str,
                                required=False,
                                help="Debe indicar id producto",
                                
                                )
            
            parser.add_argument('id_tipo_producto',
                                type=str,
                                required=False,
                                help="Debe indicar id producto",
                                
                                )
            parser.add_argument('nombre',
                                type=str,
                                required=False,
                                help="Debe indicar id producto",
                                
                                )
            
            data = parser.parse_args()
            iva = Iva.get_data(1)
            menu = []
            if 'id_cliente'in data and data['id_cliente'] is not None:
                datos = Producto.get_data_cliente(data['id_cliente'])
            elif 'id_tipo_producto' in data and data['id_tipo_producto'] is not None:
                datos = Producto.get_data_producto(data['id_tipo_producto'])
            elif 'nombre' in data and data['nombre'] is not None:
                datos = Producto.get_data_producto_name(data['nombre'])
            else:
                datos = Producto.getAll()

            if datos:
                for row in datos:
                    img = None
                    imagen = ProductoImagen.get_data_id(row.id)
                    if imagen:
                        img = imagen[0]['id']
                    iva = Iva.get_data(row.id_iva)
                    fix_iva = row.precio - round(row.precio/iva[0]["valor"],2)
                    fix_precio_bruto = row.precio - fix_iva
                    data = {
                        "id": row.id,
                        "sku": row.sku,
                        "nombre": row.nombre,
                        "id_cliente": row.id_cliente,
                        "id_tipo_producto": row.id_tipo_producto,
                        "precio": row.precio,
                        "cantidad" : 1,
                        "created_at": str(row.created_at),
                        "updated_at": str(row.updated_at),
                        "descripcion" : row.descripcion,
                        "imagen" : img,
                        "iva" : str(iva[0]['valor']),
                        "fix_iva" :str(fix_iva),
                        "fix_precio_bruto": str(fix_precio_bruto)

                    }
                    
                    menu.append(data)
                        
            return {  "response":{"data": { "info": menu }}}, 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {"message": msj}, 500

class SkuProductResource(Resource):
    def get(self):
        try:

            parser = reqparse.RequestParser()
            parser.add_argument('sku',
                                type=str,
                                required=True,
                                help="Debe indicar id producto",
                                
                                )
            
            
            data = parser.parse_args()
            prod = Producto.get_data_barcode(data["sku"])
            
            if len(prod) == 0:
                prod = Producto.get_data_sku(data["sku"])
            
            if prod:
                iva = Iva.get_data(prod[0]["id_iva"])
                
                prod[0]["fix_iva"] =prod[0]["precio"] - round(prod[0]["precio"]/iva[0]["valor"],2)
                bruto = prod[0]["precio"] - prod[0]["fix_iva"]
                prod[0]["cantidad"] = 1
                prod[0]["fix_iva"] = str (prod[0]["fix_iva"])
                prod[0]["fix_precio_bruto"] = str( bruto )
                            
            return prod, 200
           
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {"message": msj}, 500

class redisResource(Resource):
    def post(self):
        try:
            key = 1
            var = {"data": [1,2,3]}
            redis.hset(key, "carro", var)
            return "ready"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {"message": msj}, 500