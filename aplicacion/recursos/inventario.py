#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import os
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from aplicacion.modelos.Banco import Banco


class InventarioResource(Resource):

    def get(self):
        menu = []
        try:
            return {
                "productos": [
                    {
                        "id": 1,
                        "nombre_producto": "Lechuga",
                        "estado": "Disponible"
                    },
                    {
                        "id": 2,
                        "nombre_producto": "Repollo",
                        "estado": "Disponible"
                    },
                    {
                        "id": 3,
                        "nombre_producto": "Tomate",
                        "estado": "Disponible"
                    },
                    {
                        "id": 4,
                        "nombre_producto": "Cebolla",
                        "estado": "Disponible"
                    },
                    {
                        "id": 5,
                        "nombre_producto": "Pepinillos",
                        "estado": "Disponible"
                    },
                    {
                        "id": 6,
                        "nombre_producto": "Queso Cheddar",
                        "estado": "Disponible"
                    },
                    {
                        "id": 7,
                        "nombre_producto": "Queso Americano",
                        "estado": "Disponible"
                    },
                    {
                        "id": 8,
                        "nombre_producto": "Queso Suizo",
                        "estado": "Disponible"
                    },
                    {
                        "id": 9,
                        "nombre_producto": "Queso Azul",
                        "estado": "Disponible"
                    },
                    {
                        "id": 10,
                        "nombre_producto": "Tocino",
                        "estado": "Disponible"
                    },
                    {
                        "id": 11,
                        "nombre_producto": "Huevo",
                        "estado": "Disponible"
                    },
                    {
                        "id": 12,
                        "nombre_producto": "Salsa de tomate",
                        "estado": "Disponible"
                    },
                    {
                        "id": 13,
                        "nombre_producto": "Mayonesa",
                        "estado": "Disponible"
                    },
                    {
                        "id": 14,
                        "nombre_producto": "Mostaza",
                        "estado": "Disponible"
                    },
                    {
                        "id": 15,
                        "nombre_producto": "Ketchup",
                        "estado": "Disponible"
                    },
                    {
                        "id": 16,
                        "nombre_producto": "Salsa BBQ",
                        "estado": "Disponible"
                    },
                    {
                        "id": 17,
                        "nombre_producto": "Pan de hamburguesa",
                        "estado": "Disponible"
                    },
                    {
                        "id": 18,
                        "nombre_producto": "Pan integral de hamburguesa",
                        "estado": "Disponible"
                    },
                    {
                        "id": 19,
                        "nombre_producto": "Pan sin gluten",
                        "estado": "Disponible"
                    },
                    {
                        "id": 20,
                        "nombre_producto": "Carne de res",
                        "estado": "Disponible"
                    },
                    {
                        "id": 21,
                        "nombre_producto": "Carne de pollo",
                        "estado": "Disponible"
                    },
                    {
                        "id": 22,
                        "nombre_producto": "Carne de cerdo",
                        "estado": "Disponible"
                    },
                    {
                        "id": 23,
                        "nombre_producto": "Carne de pavo",
                        "estado": "Disponible"
                    },
                    {
                        "id": 24,
                        "nombre_producto": "Carne vegana",
                        "estado": "Disponible"
                    },
                    {
                        "id": 25,
                        "nombre_producto": "Pan de sésamo",
                        "estado": "Disponible"
                    },
                    {
                        "id": 26,
                        "nombre_producto": "Pan de trigo",
                        "estado": "Disponible"
                    },
                    {
                        "id": 27,
                        "nombre_producto": "Pan de centeno",
                        "estado": "Disponible"
                    },
                    {
                        "id": 28,
                        "nombre_producto": "Pan de maíz",
                        "estado": "Disponible"
                    },
                    {
                        "id": 29,
                        "nombre_producto": "Pan sin levadura",
                        "estado": "Disponible"
                    },
                    {
                        "id": 30,
                        "nombre_producto": "Aguacate",
                        "estado": "Disponible"
                    },
                    {
                        "id": 31,
                        "nombre_producto": "Champiñones",
                        "estado": "Disponible"
                    },
                    {
                        "id": 32,
                        "nombre_producto": "Cebolla caramelizada",
                        "estado": "Disponible"
                    },
                    {
                        "id": 33,
                        "nombre_producto": "Aros de cebolla",
                        "estado": "Disponible"
                    },
                    {
                        "id": 34,
                        "nombre_producto": "Pimiento verde",
                        "estado": "Disponible"
                    },
                    {
                        "id": 35,
                        "nombre_producto": "Pimiento rojo",
                        "estado": "Disponible"
                    },
                    {
                        "id": 36,
                        "nombre_producto": "Aceitunas",
                        "estado": "Disponible"
                    },
                    {
                        "id": 37,
                        "nombre_producto": "Pepinillos en vinagre",
                        "estado": "Disponible"
                    },
                    {
                        "id": 38,
                        "nombre_producto": "Salsa de queso",
                        "estado": "Disponible"
                    },
                    {
                        "id": 39,
                        "nombre_producto": "Salsa tártara",
                        "estado": "Disponible"
                    },
                    {
                        "id": 40,
                        "nombre_producto": "Salsa de ajo",
                        "estado": "Disponible"
                    },
                    {
                        "id": 41,
                        "nombre_producto": "Salsa ranch",
                        "estado": "Disponible"
                    },
                    {
                        "id": 42,
                        "nombre_producto": "Salsa de chipotle",
                        "estado": "Disponible"
                    },
                    {
                        "id": 43,
                        "nombre_producto": "Salsa de mostaza y miel",
                        "estado": "Disponible"
                    },
                    {
                        "id": 44,
                        "nombre_producto": "Salsa barbacoa",
                        "estado": "Disponible"
                    },
                    {
                        "id": 45,
                        "nombre_producto": "Salsa de jalapeños",
                        "estado": "Disponible"
                    },
                    {
                        "id": 46,
                        "nombre_producto": "Queso rallado",
                        "estado": "Disponible"
                    },
                    {
                        "id": 47,
                        "nombre_producto": "Queso fundido",
                        "estado": "Disponible"
                    },
                    {
                        "id": 48,
                        "nombre_producto": "Hojas de albahaca",
                        "estado": "Disponible"
                    },
                    {
                        "id": 49,
                        "nombre_producto": "Hojas de cilantro",
                        "estado": "Disponible"
                    }
                ]
            }
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
            print("------------------")
            print(dataJson)
            print("------------------")
            return dataJson
        except Exception as e:
            print(" ## Error ## \n")
            print(e)
            print("\n")
            return {"message": "Ha ocurrido un error de conexión."}, 500
