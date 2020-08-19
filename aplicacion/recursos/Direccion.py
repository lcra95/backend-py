#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys,os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Direccion import Direccion
from aplicacion.modelos.TipoDireccion import TipoDireccion
from aplicacion.modelos.Comuna import Comuna
from aplicacion.modelos.PersonaDireccion import PersonaDireccion

class DireccionResource(Resource):

    def get(self):
        menu = []
        try:
            datos = Direccion.getAll()
            if datos:
                for row in datos:
                    data = {
                        "id": row.id,
                        "direccion_escrita": row.direccion_escrita,
                        "numero": row.numero,
                        "departamento": row.departamento,
                        "id_comuna": row.id_comuna,
                        "id_tipo_direccion": row.id_tipo_direccion,
                        "created_at": str(row.created_at),
                        "updated_at": str(row.updated_at),
                        "datos_tipo_direccion": TipoDireccion.get_data(row.id_tipo_direccion),
                        "datos_comuna" : Comuna.get_data(row.id_comuna),
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
            depto = None        
            dataJson = request.get_json()

            if 'departamento' in dataJson and dataJson["departamento"]:
                depto = dataJson["departamento"]
            
            dataJson["departamento"] = depto
            
            insert = Direccion.insert(dataJson)
            if insert:
                jsonPersonaDirecion ={
                    "id_direccion": insert,
                    "id_persona" : dataJson["id_persona"]
                }
                PdInsert = PersonaDireccion.insert(jsonPersonaDirecion)
                if PdInsert:
                    return {"estado": 1, "msj":"Registro exitoso", "id_direccion": insert }
            return {"estado": 0, "msj": "Ha ocurrido un error"}
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500