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


class Recepcion(db.Model):
    __tablename__ = 'recepcion'


    id = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(128), nullable=False)
    id_tipo_documento = db.Column(db.Integer, nullable=False)
    id_sucursal = db.Column(db.Integer, nullable=False)
    id_creador = db.Column(db.Integer, nullable=False)
    observacion = db.Column(db.String(128), nullable=False)
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
        query = Recepcion( 
            documento = dataJson['documento'],
            id_tipo_documento = dataJson['id_tipo_documento'],
            id_sucursal = dataJson['id_sucursal'],
            id_creador = dataJson['id_creador'],
            observacion = dataJson['observacion'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        Recepcion.guardar(query)
        if query.id:                            
            return  query.id 
        return  False

    @classmethod
    def update_data(cls, _id, dataJson):
        try:
            db.session.rollback()
            query = cls.query.filter_by(id=_id).first()
            if query:
                if 'documento' in dataJson:
                    query.documento = dataJson['documento']
                if 'id_tipo_documento' in dataJson:
                    query.id_tipo_documento = dataJson['id_tipo_documento']
                if 'id_sucursal' in dataJson:
                    query.id_sucursal = dataJson['id_sucursal']
                if 'id_creador' in dataJson:
                    query.id_sucursal = dataJson['id_creador']
                if 'observacion' in dataJson:
                    query.observacion = dataJson['observacion']
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
