#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.ProductoStock import ProductoStock
from aplicacion.modelos.Cliente import Cliente


class ProductoStockResource(Resource):

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('sku',
                                type=str,
                                required=False,
                                help="Debe indicar id prestador",
                                
                                )
            parser.add_argument('id_sucursal',
                                type=str,
                                required=False,
                                help="Debe indicar id Sucursal",
                        
                                )           
            parser.add_argument('producto',
                                type=str,
                                required=False,
                                help="Debe indicar id Sucursal",
                        
                                )           
            data = parser.parse_args()
            sku = None
            suc = None
            pro = None
            
            if 'sku' in data and data['sku'] is not None:
                sku = data['sku']
            if 'id_sucursal' in data and data['id_sucursal'] is not None:
                suc = data['id_sucursal']
            if 'producto' in data and data['producto'] is not None:
                pro = data['producto']

            datos = ProductoStock.filtroStock(sku, suc, pro)
                
            return {  "response":{"data": { "info": datos }}}, 200
            

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
            insert = ProductoStock.insert(dataJson)
            return insert
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500