#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Usuario import Usuario
from aplicacion.modelos.Persona import Persona
import hashlib 

class UsuarioResource(Resource):

    def get(self):
        menu = []
        try:
            datos = Usuario.getAll()
            if datos:
                for row in datos:
                    data = {
                        "id": row.id,
                        "correo": row.correo,
                        "telefono": row.telefono,
                        "password": row.password,
                        "id_persona": row.id_persona,
                        "created_at": str(row.created_at),
                        "updated_at": str(row.updated_at),
                        "datos_persona" : Persona.get_data(row.id_persona)
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
            insert = Usuario.insert(dataJson)
            return insert
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500

class logInResource(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user',
                                type=str,
                                required=True,
                                help="Debe indicar id prestador",
                                
                                )
            parser.add_argument('password',
                                type=str,
                                required=True,
                                help="Debe indicar id Sucursal",
                                
                                )   
            data = parser.parse_args()
            user = Usuario.get_user_login(data['user'], data['password'])
            if user:
                
                return {"estado": 1, "msj": "Bienvenido", "data": user}
            else:
                return {"estado": 0, "msj": "Usuario no existe"}
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500    