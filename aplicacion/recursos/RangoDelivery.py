#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.RangoDelivery import RangoDelivery
from aplicacion.modelos.Persona import Persona
from aplicacion.modelos.Cliente import Cliente

class RangoDeliveryResource(Resource):

    def get(self):
        menu = []
        try:
            datos = RangoDelivery.getAll()
            if datos:
                for row in datos:
                    data = {
                        "id": row.id,
                        "desde": row.desde,
                        "hasta": row.hasta,
                        "monto": row.monto,
                        "id_cliente": row.id_cliente,
                        "created_at": str(row.created_at),
                        "updated_at": str(row.updated_at)
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
            # parser.add_argument('idRangoDelivery',
            #                     type=str,
            #                     required=False,
            #                     help="Debe indicar id RangoDelivery",
                                
            #                     )   
            # data = parser.parse_args()
            dataJson = request.get_json()
            insert = RangoDelivery.insert(dataJson)
            return insert
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500