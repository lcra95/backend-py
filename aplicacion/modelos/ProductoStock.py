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


class ProductoStock(db.Model):
    __tablename__ = 'producto_stock'


    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, nullable=False)
    id_sucursal = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
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
        query = ProductoStock( 
            id_producto = dataJson['id_producto'],
            id_sucursal = dataJson['id_sucursal'],
            cantidad = dataJson['cantidad'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        ProductoStock.guardar(query)
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
                if 'id_sucursal' in dataJson:
                    query.id_sucursal = dataJson['id_sucursal']
                if 'cantidad' in dataJson:
                    query.cantidad = dataJson['cantidad']
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
    
    @classmethod
    def prodSucursalStock(cls, id_producto, id_sucursal):
        query =  cls.query.filter_by(id_producto = id_producto, id_sucursal = id_sucursal ).first()
        return  Utilidades.obtener_datos(query)


    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def filtroStock(cls, sku = None, id_sucursal = None, producto = None):
        filt_sku = ''
        filt_suc = ''
        filt_pro = ""
        if sku: 
            filt_sku = " AND p.sku = "+ str(sku) +" "
        if id_sucursal:
            filt_suc = " AND ps.id_sucursal = " + str(id_sucursal)
        if producto:
            filt_pro = " AND p.nombre LIKE '%" + str(producto) +"%'"   

        sql =   "SELECT \
                	p.sku, p.nombre, ps.cantidad, s.nombre as sucursal \
                FROM producto_stock ps \
                JOIN producto p ON p.id = ps.id_producto" + str(filt_sku) + " \
                JOIN sucursal s ON s.id = ps.id_sucursal \
                WHERE 1 = 1 " + filt_suc + filt_pro

        
        query = db.session.execute(sql)
        result = []
        if query:
            for x in query:
                temp = {

                    "nombre": x.nombre,
                    "sku" : x.sku,
                    "cantidad" : x.cantidad,
                    "sucursal" : x.sucursal
                }
                result.append(temp)
        
        return  result
