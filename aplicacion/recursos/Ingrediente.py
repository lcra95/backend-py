#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Ingrediente import Ingrediente
from aplicacion.modelos.TipoIngrediente import TipoIngrediente

class IngredienteResource(Resource):

    def get(self):
        menu = []
        try:
            datos = Ingrediente.getAll()
            if datos:
                for row in datos:
                    data = {
                        "id": row.id,
                        "nombre": row.nombre,
                        "id_tipo_ingrediente": row.id_tipo_ingrediente,
                        "created_at": str(row.created_at),
                        "updated_at": str(row.updated_at),
                        "tipo_ingrediente" : TipoIngrediente.get_data(row.id_tipo_ingrediente)
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
            insert = Ingrediente.insert(dataJson)
            return insert
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500