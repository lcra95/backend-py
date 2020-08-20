#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.UsuarioSucusrsal import UsuarioSucusrsal
from aplicacion.modelos.Cliente import Cliente


class UsuarioSucusrsalResource(Resource):

    def get(self):
        menu = []
        try:
            datos = UsuarioSucusrsal.getAll()
            if datos:
                for row in datos:
                    data = {
                        "id": row.id,
                        "id_usuario": row.id_usuario,
                        "id_usuario": row.id_usuario,
                        "estado": row.estado,
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
            insert = UsuarioSucusrsal.insert(dataJson)
            return insert
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500