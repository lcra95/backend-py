# coding: utf-8

import sys, os, re
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Table, Text, Time
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from aplicacion.helpers.utilidades import Utilidades
from aplicacion.modelos.Producto import Producto
# db = SQLAlchemy()

from aplicacion.db import db


class OrdenDetalle(db.Model):
    __tablename__ = 'orden_detalle'


    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, nullable=False)
    id_orden = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    detalle = db.Column(db.String(128), nullable=False)
    precio_unitario = db.Column(db.Integer, nullable=False)
    precio_extendido = db.Column(db.Integer, nullable=False)
    precio_iva = db.Column(db.Integer, nullable=False)
    precio_total = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
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
        query = OrdenDetalle( 
            id_producto = dataJson['id_producto'],
            id_orden = dataJson['id_orden'],
            cantidad = dataJson['cantidad'],
            detalle = dataJson['detalle'],
            precio_unitario = dataJson['precio_unitario'],
            precio_extendido = dataJson['precio_extendido'],
            precio_iva = dataJson['precio_iva'],
            precio_total = dataJson['precio_total'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        OrdenDetalle.guardar(query)
        if query.id:                            
            return  query.id 
        return  False

    @classmethod
    def update_data(cls, _id, dataJson):
        try:
            db.session.rollback()
            query = cls.query.filter_by(id=_id).first()
            if query:
                if 'id_producto' in dataJson:
                    query.id_producto = dataJson['id_producto']
                if 'id_orden' in dataJson:
                    query.id_orden = dataJson['id_orden']
                if 'cantidad' in dataJson:
                    query.cantidad = dataJson['cantidad']
                if 'detalle' in dataJson:
                    query.detalle = dataJson['detalle']
                if 'precio_unitario' in dataJson:
                    query.precio_unitario = dataJson['precio_unitario']
                if 'precio_extendido' in dataJson:
                    query.precio_extendido = dataJson['precio_extendido']
                if 'precio_iva' in dataJson:
                    query.precio_iva = dataJson['precio_iva']
                if 'precio_total' in dataJson:
                    query.precio_total = dataJson['precio_total']
                if 'created_at' in dataJson:
                    query.created_at = dataJson['created_at']         
               
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
    def DetalleByOrden(cls, id_orden):
        sql =  "SELECT 	* FROM orden o JOIN  orden_detalle od ON od.id_orden = o.id WHERE o.id = "+ str(id_orden) + " "
        
        query = db.session.execute(sql)
        result = []
        if query:
            for x in query:
                temp = {
                    "id": x.id,
                    "id_producto": x.id_producto,
                    "id_orden": x.id_orden,
                    "cantidad" : x.cantidad,
                    "detalle" : x.detalle,
                    "precio_unitario" : x.precio_unitario,
                    "precio_extendido" : x.precio_extendido,
                    "precio_iva" : x.precio_iva,
                    "precio_total" : x.precio_total,
                    "data_repartidor": Producto.get_data(x.id_producto)
                }
                result.append(temp)
        
        return  result