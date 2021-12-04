#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Persona import Persona
from aplicacion.modelos.Telefono import Telefono
from aplicacion.modelos.Correo import Correo
from aplicacion.modelos.Direccion import Direccion
from aplicacion.modelos.Usuario import Usuario
from aplicacion.modelos.PersonaDireccion import PersonaDireccion
from aplicacion.modelos.Cliente import Cliente


class PersonaResource(Resource):

    def get(self):
        menu = []
        try:
            datos = Persona.getAll()
            if datos:
                for row in datos:
                    data = {
                        "id": row.id,
                        "nombre": row.nombre,
                        "apellido_paterno": row.apellido_paterno,
                        "apellido_materno": row.apellido_materno,
                        "genero": row.genero,
                        "tipo_persona": row.tipo_persona,
                        "identificacion": row.identificacion,
                        "fecha_nacimiento": str(row.fecha_nacimiento),
                        "estado": row.estado,
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
            apellido = None
            tipo_persona = 1
            depto = None
            departamento = None
            numerod = None
            dataJson = request.get_json()

            if 'apellido' in dataJson and dataJson["apellido"]:
                apellido = dataJson["apellido"]
            if 'tipo_persona' in dataJson and dataJson["tipo_persona"]:
                apellido = dataJson["tipo_persona"]
            if 'numerod' in dataJson and dataJson["numerod"]:
                numerod = dataJson["numerod"]
            if 'departamento' in dataJson and dataJson["departamento"]:
                depto = dataJson["departamento"]

            identificacion =None
            if "identificacion" in dataJson:
                identificacion = dataJson["identificacion"]

            jsoPersona = {
                "identificacion": identificacion,
                "nombre": dataJson["nombre"],
                "apellido_paterno": apellido,
                "apellido_materno": None,
                "genero": None,
                "tipo_persona" : tipo_persona,
                "fecha_nacimiento" : None,
                "estado": 1
            }

            insert = Persona.insert(jsoPersona)

            if insert:
                jsonTelefono = {
                    "id_persona" : insert,
                    "numero" : dataJson["numero"]
                }
                telInsert = Telefono.insert(jsonTelefono)

                jsonEmail = {
                   "id_persona" : insert,
                   "direccion" : dataJson["email"] 
                }
                corInsert = Correo.insert(jsonEmail)
                comuna = None
                insertDir = None
                pdInser = None
                if "id_place" in dataJson and dataJson["id_place"] != "":
                    if "id_comuna" in dataJson:
                        comuna = dataJson["id_comuna"]
                    jsonDireccion = {
                        "id_comuna" : comuna,
                        "id_tipo_direccion": dataJson["id_tipo_direccion"],
                        "direccion_escrita": dataJson["direccion"],
                        "numero": numerod,
                        "departamento": depto,
                        "id_place" : dataJson["id_place"]
                    }
                    insertDir = Direccion.insert(jsonDireccion)
                
                if insertDir is not None:
                    jsonDireccionPersona = {
                        "id_persona" : insert,
                        "id_direccion": insertDir
                    }
                    pdInser = PersonaDireccion.insert(jsonDireccionPersona)
            else:
                return { "estado_response" : 0, "msj": "Ha ocurrido un error en el registro" }


            if dataJson["registro"] == 1:
                if telInsert is not None and corInsert is not None:
                    jsonReg = {
                        "id_persona" : insert,
                        "correo":  dataJson["email"],
                        "telefono":  dataJson["numero"],
                        "password" : dataJson["password"]
                    }
                    jsonUser = Usuario.insert(jsonReg)
                    user = Persona.personaFullInfo(insert)
                    response = {"estado": 1, "msj": "Bienvenido", "data": user}
            if dataJson["registro"] == 2:
                if telInsert is not None and corInsert is not None:
                    jsonReg = {
                        "id_persona" : insert,
                        "nombre":  dataJson["nombre"],
                        "giro":  dataJson["giro"],
                    }
                    jsonUser = Cliente.insert(jsonReg)
                    user = Persona.personaFullInfo(insert)
                    response = {"estado": 1, "msj": "Bienvenido", "data": user}
                else:
                    
                    return { "estado_response" : 0, "msj": "Ha ocurrido un error en el registro" }
            else:
                if telInsert is not None and corInsert is not None:
                    user = Persona.personaFullInfo(insert)
                    response = {"estado": 1, "msj": "Bienvenido", "data": user}
                else:
                   return {"estado" : 0 , "msj": "Ha ocurrido un error en el registro"} 
            return response
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj)},500

class personaFullResource(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id',
                                type=str,
                                required=False,
                                help="Debe indicar id prestador",
                                
                                )
            parser.add_argument('correo',
                                type=str,
                                required=False,
                                help="Debe indicar id Sucursal",
                                
                                )   
            parser.add_argument('telefono',
                                type=str,
                                required=False,
                                help="Debe indicar id Sucursal",
                                
                                )   
            data = parser.parse_args()
            
            info = Persona.personaFullInfo(data["id"], data["correo"], data["telefono"])
            return info
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {"message": msj}, 500