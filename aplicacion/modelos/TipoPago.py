# coding: utf-8

import sys, os, re
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Table, Text, Time
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
from aplicacion.helpers.utilidades import Utilidades
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func


# db = SQLAlchemy()

from aplicacion.db import db


class TipoPago(db.Model):
    __tablename__ = 'tipo_pago'


    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    id_perfil = db.Column(db.Integer, nullable=True)
    #CRUD


    @classmethod
    def getAll(cls):
        query =  cls.query.filter_by(id_perfil= 1).all()
        return query

    @classmethod
    def get_data(cls, _id):
        query =  cls.query.filter_by(id=_id).first()
        return  Utilidades.obtener_datos(query)

    @classmethod
    def insert(cls, dataJson):
        query = TipoPago( 
            nombre = dataJson['nombre'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        TipoPago.guardar(query)
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
                if 'created_at' in dataJson:
                    query.created_at = dataJson['created_at']         
                if 'estado' in dataJson:
                    query.estado = dataJson['estado']
               
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
