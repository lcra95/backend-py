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


class ProductoIngrediente(db.Model):
    __tablename__ = 'producto_ingrediente'


    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, nullable=False)
    id_ingrediente = db.Column(db.Integer, nullable=False)
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
        query = ProductoIngrediente( 
            id_producto = dataJson['id_producto'],
            id_ingrediente = dataJson['id_ingrediente'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        ProductoIngrediente.guardar(query)
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
                if 'id_ingrediente' in dataJson:
                    query.id_ingrediente = dataJson['id_ingrediente']
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

    # @classmethod
    # def IngredienteByProducto(cls, id_producto):
    #     sql =   "SELECT \
    #                 i.id, \
    #                 i.nombre, \
    #                 ti.nombre as tipo \
    #             FROM producto p \
    #             JOIN producto_ingrediente pi ON pi.id_producto = p.id \
    #             JOIN ingrediente i ON i.id = pi.id_ingrediente \
    #             JOIN tipo_ingrediente ti ON ti.id = i.id_tipo_ingrediente \
    #             WHERE p.id = " + str(id_producto) + " "
        
    #     query = db.session.execute(sql)
    #     result = []
    #     if query:
    #         for x in query:
    #             temp = {
    #                 "id": x.id,
    #                 "nombre": x.nombre,
    #                 "tipo" : x.tipo
    #             }
    #             result.append(temp)
        
    #     return  result




    @classmethod
    def IngredienteByProducto(cls, id_producto):
        sql =   "SELECT \
                    i.id, i.nombre \
                FROM producto_ingrediente pi \
                JOIN ingrediente i ON i.id = pi.id_ingrediente and i.estado = 1  \
                JOIN tipo_ingrediente ti ON ti.id = i.id_tipo_ingrediente \
                WHERE pi.id_producto = "+ str(id_producto) + " group by ti.id, i.id, i.nombre, ti.nombre"
        
        query = db.session.execute(sql)
        result = []
        if query:
            for x in query:
                temp = {
                    "id": x.id,
                    "nombre": x.nombre,
                    # "tipo" : x.tipo,
                    # "ingrediente" : ProductoIngrediente.ingredienteByTipoAndProducto(id_producto, x.tipo)
                }
                result.append(temp)
        
        return  result

    @classmethod 
    def ingredienteByTipoAndProducto(cls, id_producto, id_tipo_ingrediente):
        sql =   "SELECT \
                    i.id, i.nombre \
                FROM producto_ingrediente pi \
                JOIN ingrediente i ON i.id = pi.id_ingrediente \
                JOIN tipo_ingrediente ti ON ti.id = i.id_tipo_ingrediente \
                WHERE pi.id_producto = "+ str(id_producto) +" and ti.id = "+ str(id_tipo_ingrediente) +" group by ti.id, i.id, i.nombre, ti.nombre"

        query = db.session.execute(sql)
        result = []
        if query:
            for x in query:
                temp = {

                    "nombre": x.nombre,
                    "tipo" : x.id
                }
                result.append(temp)
        
        return  result
