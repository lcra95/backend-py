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


class Direccion(db.Model):
    __tablename__ = 'direccion'


    id = db.Column(db.Integer, primary_key=True)
    direccion_escrita = db.Column(db.String(128), nullable=False)
    numero = db.Column(db.String(128), nullable=False)
    departamento = db.Column(db.String(128), nullable=False)
    id_comuna = db.Column(db.Integer, nullable=False)
    id_tipo_direccion = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    id_place = db.Column(db.String(128), nullable=False)
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
        numero = None
        id_comuna = None
        if "numero" in dataJson:
            numero = dataJson['numero']
        if "id_comuna" in dataJson:
            id_comuna = dataJson['id_comuna']
        query = Direccion( 
            direccion_escrita = dataJson['direccion_escrita'],
            numero = numero,
            departamento = dataJson['departamento'],
            id_comuna = id_comuna,
            id_tipo_direccion = dataJson['id_tipo_direccion'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            id_place = dataJson['id_place'],
            )
        Direccion.guardar(query)
        if query.id:                            
            return  query.id 
        return  False

    @classmethod
    def update_data(cls, _id, dataJson):
        try:
            db.session.rollback()
            query = cls.query.filter_by(id=_id).first()
            if query:
                if 'direccion_escrita' in dataJson:
                    query.direccion_escrita = dataJson['direccion_escrita']
                if 'numero' in dataJson:
                    query.numero = dataJson['numero']
                if 'departamento' in dataJson:
                    query.departamento = dataJson['departamento']
                if 'id_comuna' in dataJson:
                    query.id_comuna = dataJson['id_comuna']
                if 'id_tipo_direccion' in dataJson:
                    query.id_tipo_direccion = dataJson['id_tipo_direccion']
                if 'created_at' in dataJson:
                    query.created_at = dataJson['created_at']         
                if 'id_place' in dataJson:
                    query.id_place = dataJson['id_place']         
               
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
    def getPlaces(cls,_id):
        sql =   "SELECT \
                    id_place as dir \
                FROM direccion d \
                LEFT JOIN comuna c on c.id = d.id_comuna \
                WHERE d.id = " + str(_id)
        
        query = db.session.execute(sql)

        if query:
            for x in query:               
                return str(x.dir)

        return None
    @classmethod
    def getMonto(cls, distance):
        sql =   "select * from rango_delivery WHERE "+ str(distance) +" between desde and hasta;"
        
        query = db.session.execute(sql)

        if query:
            for x in query:               
                return str(x.monto)

        return None
