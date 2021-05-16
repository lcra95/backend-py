#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Se establece enviroment como argumento importado
from aplicacion.enviroment import env
enviroment = env

import sys,os,click,json
import requests
import time
from time import ctime
import datetime
import threading
import base64
from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from flask_mail import Mail
from ftplib import FTP
# from flask_analytics import Analytics

from aplicacion.config import app_config
from aplicacion.db import db
from aplicacion.redis import redis


# IMPORTACIÓN DE RECURSOS
from aplicacion.recursos.TipoDireccion import TipoDireccionResource
from aplicacion.recursos.Direccion import DireccionResource, GetPlacesResource
from aplicacion.recursos.PersonaDireccion import PersonaDireccionResource
from aplicacion.recursos.TipoIngrediente import TipoIngredienteResource
from aplicacion.recursos.TipoPersona import TipoPersonaResource
from aplicacion.recursos.TipoEntrega import TipoEntregaResource
from aplicacion.recursos.TipoProducto import TipoProductoResource
from aplicacion.recursos.Region import RegionResource
from aplicacion.recursos.Persona import PersonaResource, personaFullResource
from aplicacion.recursos.Ingrediente import IngredienteResource
from aplicacion.recursos.Cliente import ClienteResource, SearchClienteResource
from aplicacion.recursos.Producto import ProductoResource, ProductoDetalleResource, ProductoFilterResource, SkuProductResource,redisResource
from aplicacion.recursos.ProductoIngrediente import ProductoIngredienteResource
from aplicacion.recursos.ProductoImagen import ProductoImagenResource
from aplicacion.recursos.Telefono import TelefonoResource
from aplicacion.recursos.Correo import CorreoResource
from aplicacion.recursos.Comuna import ComunaResource, ComunabyprovinciaResource
from aplicacion.recursos.Provincia import ProvinciaResource
from aplicacion.recursos.Repartidor import RepartidorResource
from aplicacion.recursos.Orden import OrdenResource, OrdenFullResource
from aplicacion.recursos.OrdenRepartidor import OrdenRepartidorResource
from aplicacion.recursos.TipoPago import TipoPagoResource
from aplicacion.recursos.Sucursal import SucursalResource
from aplicacion.recursos.OrdenPago import OrdenPagoResource
from aplicacion.recursos.RangoDelivery import RangoDeliveryResource
from aplicacion.recursos.Usuario import UsuarioResource, logInResource
from aplicacion.recursos.Iva import IvaResource
from aplicacion.recursos.TipoCuenta import TipoCuentaResource
from aplicacion.recursos.Banco import BancoResource
from aplicacion.recursos.ClienteCuenta import ClienteCuentaResource
from aplicacion.recursos.TipoDocumento import TipoDocumentoResource
from aplicacion.recursos.Recepcion import RecepcionResource
from aplicacion.recursos.ProductoStock import ProductoStockResource
from aplicacion.recursos.movimiento import MovimientoResource
#Inicializacion de flask
app = Flask(__name__, 
static_url_path='/api_static',
static_folder='api_static',
template_folder='templates')

#habilitacion de CORS
CORS(app)

#Inicializacion de datos de BD
db.init_app(app)

#Se setean variables de configuracion segun ambiente(env)
print("### AMBIENTE: " + enviroment + "###")
app.config.from_object(app_config[enviroment])
redis.init_app(app)

#Inicializacion de servicios api
api = Api(app)

# SE DEFINEN LOS ENDPOINTS Y LA CLASE QUE SE ENCARGARÁ DE PROCESAR CADA SOLICITUD
## ORDEN
api.add_resource(OrdenResource, '/orden')
api.add_resource(OrdenRepartidorResource, '/ordenrepartidor')
api.add_resource(ClienteResource, '/cliente')
api.add_resource(SearchClienteResource, '/searchcliente')
api.add_resource(TipoEntregaResource, '/tipoentrega')
api.add_resource(RepartidorResource, '/repartidor')
api.add_resource(TipoPagoResource, '/tipopago')
api.add_resource(OrdenPagoResource, '/ordenpago')
# api.add_resource(PagoOnLineResource, '/pagoenlinea')

## PRODUCTOS
api.add_resource(ProductoResource, '/producto')
api.add_resource(ProductoFilterResource, '/productos')
api.add_resource(ProductoIngredienteResource, '/productoingrediente')
api.add_resource(ProductoImagenResource, '/productoimagen')
api.add_resource(TipoProductoResource, '/tipoproducto')
api.add_resource(TipoIngredienteResource, '/tipoingrediente')
api.add_resource(IngredienteResource, '/ingrediente')
api.add_resource(ProductoDetalleResource,'/producto/detalle')
api.add_resource(SkuProductResource, '/sku')
api.add_resource(RecepcionResource, '/recepcion')
api.add_resource(ProductoStockResource, '/stock')
api.add_resource(OrdenFullResource, '/ordenfull')

## PERSONALES
api.add_resource(PersonaResource, '/persona')
api.add_resource(TelefonoResource, '/telefono')
api.add_resource(CorreoResource, '/correo')
api.add_resource(TipoPersonaResource, '/tipopersona')
api.add_resource(PersonaDireccionResource, '/personadireccion')
api.add_resource(personaFullResource, '/personafull')

## UBICACION
api.add_resource(RegionResource, '/region')
api.add_resource(ComunaResource, '/comuna')
api.add_resource(ComunabyprovinciaResource, '/comunaprovincia')
api.add_resource(ProvinciaResource, '/provincia')
api.add_resource(TipoDireccionResource, '/tipodireccion')
api.add_resource(DireccionResource, '/direccion')
api.add_resource(SucursalResource, '/sucursal')
api.add_resource(RangoDeliveryResource, '/rangodelivery')
api.add_resource(GetPlacesResource,'/getplace')

#usuarios
api.add_resource(UsuarioResource, '/usuario')
api.add_resource(logInResource, '/login')

#Varios
api.add_resource(IvaResource, '/iva')
api.add_resource(TipoCuentaResource, '/tipocuenta')
api.add_resource(BancoResource, '/banco')
api.add_resource(ClienteCuentaResource, '/clientecuenta')
api.add_resource(TipoDocumentoResource, '/tipodocumento')
api.add_resource(MovimientoResource, '/movimiento')
#ROUTES
@app.route('/')
def index():
    return "Hola =)", 200
@app.route('/imagen/<path:path>')
def getimagen(path):
    from aplicacion.modelos.ProductoImagen import ProductoImagen  
    from aplicacion.config import app_config

    ruta = ProductoImagen.get_data(path)
    path = ruta[0]['imagen']
    # print("------------------")
    # print(app.config['ROOT_PATH']+ '/backend-py/aplicacion/clients/01/'+path)
    # print("------------------")
    return send_file(app.config['ROOT_PATH']+ '/backend-py/aplicacion/clients/01/'+path)

@app.route('/pagoenlinea', methods=['GET', 'POST'] )
def pagoscallback():
    print("############### PAGOS CALLBACK ##################")
    from aplicacion.modelos.OrdenPago import OrdenPago
    data = {}
    try:
        data["form_data"] = request.form.to_dict()
        data["dataJson"] = request.get_json()
        print("----------------------------")
        print(data["dataJson"]["order"])
        print("----------------------------")
        jsonUp ={
            "estado": 1
        }
        vari = OrdenPago.update_data(data["dataJson"]["order"],jsonUp )
        print("******************")
        print(vari)
        print("******************")
    except Exception as e:
        print(e)
    print("############### FIN PAGOS CALLBACK ##################")
    return data, 200

@app.route('/imprimir-orden/<int:_id>')
def imprime(_id):
    from aplicacion.modelos.Orden import Orden
    info = Orden.ordenFullInfo(_id)
    deff = 0
    for tot in info[0]["detalle"]:
        deff = deff + tot["precio_total"]
    
    info[0]["total_orden"] = deff
    
    # return info[0]

    return render_template("orden.html", data = info)
#INICIAMOS LA APLICACIÓN
app.run(host='0.0.0.0', port=5000, debug=True )
    
        
