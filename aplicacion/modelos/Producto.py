# coding: utf-8

import sys, os, re
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Table, Text, Time
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from aplicacion.helpers.utilidades import Utilidades

# db = SQLAlchemy()

from aplicacion.db import db


class Producto(db.Model):
    __tablename__ = 'producto'


    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    id_tipo_producto = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    id_cliente = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    descripcion = db.Column(db.String(256), nullable=False)
    sku = db.Column(db.String(256), nullable=False)
    id_iva = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(256), nullable=True)
    #CRUD


    @classmethod
    def getAll(cls):
        query =  cls.query.all()
        return query

    @classmethod
    def get_data(cls, _id):
        query =  cls.query.filter_by(id=_id).first()
        return  Utilidades.obtener_datos(query)

    @classmethod
    def insert(cls, dataJson):
        query = Producto( 
            nombre = dataJson['nombre'],
            id_tipo_producto = dataJson['id_tipo_producto'],
            id_cliente = dataJson['id_cliente'],
            precio = dataJson['precio'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            descripcion = dataJson['descripcion'],
            sku = dataJson['sku'],
            id_iva = dataJson['id_iva'],
            barcode = dataJson['barcode'],
            )
        Producto.guardar(query)
        if query.id:                            
            return  query.id 
        return  False

    @classmethod
    def update_data(cls, _id, dataJson):
        try:
            db.session.rollback()
            query = cls.query.filter_by(id=_id).first()
            if query:
                if 'nombre' in dataJson:
                    query.nombre = dataJson['nombre']
                if 'id_tipo_producto' in dataJson:
                    query.id_tipo_producto = dataJson['id_tipo_producto']
                if 'id_cliente' in dataJson:
                    query.id_cliente = dataJson['id_cliente']
                if 'precio' in dataJson:
                    query.precio = dataJson['precio']
                if 'created_at' in dataJson:
                    query.created_at = dataJson['created_at']         
                if 'descripcion' in dataJson:
                    query.descripcion = dataJson['descripcion']         
                if 'sku' in dataJson:
                    query.sku = dataJson['sku']         
                if 'id_iva' in dataJson:
                    query.id_iva = dataJson['id_iva']         
                if 'barcode' in dataJson:
                    query.barcode = dataJson['barcode']         
               
                query.updated_at = func.NOW()
                db.session.commit()
                if query.id:                            
                    return query.id
            return  None
        except Exception as e:
            print("=======================E")
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            return {'mensaje': str(msj) }, 500



    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_data_cliente(cls, _id):
        query =  cls.query.filter_by(id_cliente=_id).all()
        return  query
    @classmethod
    def get_data_producto(cls, _id):
        query =  cls.query.filter_by(id_tipo_producto=_id).all()
        return  query
    @classmethod
    def get_data_producto_name(cls, _id):
        search = "%{}%".format(_id)
        query =  cls.query.filter(Producto.nombre.like(search)).all()
        return  query
    @classmethod
    def get_data_sku(cls, sku):
        query =  cls.query.filter_by(sku=sku).first()
        return  Utilidades.obtener_datos(query)
    @classmethod
    def get_data_barcode(cls, barcode):
        query =  cls.query.filter_by(barcode=barcode).first()
        return  Utilidades.obtener_datos(query)