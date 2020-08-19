#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Comuna import Comuna


class ComunaResource(Resource):

    def get(self):
        menu = []
        try:
            datos = Comuna.getAll()
            if datos:
                for row in datos:
                    data = {
                        "id": row.id,
                        "nombre": row.nombre,
                        "codigo": row.codigo,
                        "id_provincia": row.id_provincia,
                        "created_at": str(row.created_at),
                        "updated_at": str(row.updated_at),
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
            insert = Comuna.insert(dataJson)
            return insert
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500

class ComunabyprovinciaResource(Resource):

    def get(self):
        menu = []
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('provincia',
                                type=str,
                                required=True,
                                help="Debe indicar id prestador",
                                
                                )
            data = parser.parse_args()
            datos = Comuna.getByRegion(data["provincia"])
            if datos:
                for row in datos:
                    data = {
                        "id": row.id,
                        "nombre": row.nombre,
                        "codigo": row.codigo,
                        "id_provincia": row.id_provincia,
                        "created_at": str(row.created_at),
                        "updated_at": str(row.updated_at),
                    }
                    
                    menu.append(data)
                        
            return {  "response":{"data": { "info": menu }}}, 200
            

        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
        