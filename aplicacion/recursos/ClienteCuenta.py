#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.ClienteCuenta import ClienteCuenta

class ClienteCuentaResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_cliente',
                            type=str,
                            required=True,
                            help="Debe indicar id cliente",
                            
                            )
        data = parser.parse_args()
        
        try:
            datos = ClienteCuenta.infoCuenta(data["id_cliente"])
            if datos:                        
                return {  "response":{"data": { "info": datos }}}, 200
            return None

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
            insert = ClienteCuenta.insert(dataJson)
            return insert
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500