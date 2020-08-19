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


class Documento(db.Model):
    __tablename__ = 'documento'


    id = db.Column(db.Integer, primary_key=True)
    id_tipo_documento = db.Column(db.Integer, nullable=False)
    id_orden = db.Column(db.Integer, nullable=False)
    folio = db.Column(db.Integer, nullable=False)
    fecha_emision = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    estado = db.Column(db.Integer, nullable=False)
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
        query = Documento( 
            id_tipo_documento = dataJson['id_tipo_documento'],
            id_orden = dataJson['id_orden'],
            folio = dataJson['folio'],
            fecha_emision = dataJson['fecha_emision'],
            estado = dataJson['estado'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        Documento.guardar(query)
        if query.id:                            
            return  query.id 
        return  False

    @classmethod
    def update_data(cls, _id, dataJson):
        try:
            db.session.rollback()
            query = cls.query.filter_by(id=_id).first()
            if query:
                if 'id_tipo_documento' in dataJson:
                    query.id_tipo_documento = dataJson['id_tipo_documento']
                if 'id_orden' in dataJson:
                    query.id_orden = dataJson['id_orden']
                if 'folio' in dataJson:
                    query.folio = dataJson['folio']
                if 'fecha_emision' in dataJson:
                    query.fecha_emision = dataJson['fecha_emision']
                if 'estado' in dataJson:
                    query.estado = dataJson['estado']
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