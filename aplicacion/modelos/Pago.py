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


class Pago(db.Model):
    __tablename__ = 'pago'


    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Integer, nullable=True)
    hash = db.Column(db.String(128), nullable=False)
    estado = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    
    #CRUD

    @classmethod
    def get_data(cls, _id):
        query =  cls.query.filter_by(hash=_id, estado = 0).first()
        return  Utilidades.obtener_datos(query)

    @classmethod
    def insert(cls, dataJson):
        query = Pago( 
            monto = dataJson['monto'],
            estado = 0,
            hash = None,
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        Pago.guardar(query)
        if query.id:         
            _hash = Pago.gethash(query.id)
            return  _hash 
        return  False

    @classmethod
    def update_data(cls, _id, dataJson):
        try:
            db.session.rollback()
            query = cls.query.filter_by(id=_id).first()
            if query:
                if 'nombre' in dataJson:
                    query.nombre = dataJson['nombre']
                if 'hash' in dataJson:
                    query.hash = dataJson['hash']
                if 'estado' in dataJson:
                    query.estado = dataJson['estado']
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
    @classmethod
    def gethash(cls, _id):
        sql ="SELECT md5("+ str(_id) +") as cod from dual"
        query = db.session.execute(sql)
        _hash = ''
        if query:
            for x in query:
                json = {
                    "hash": x.cod
                }
                _hash =x.cod
                pagou = Pago.update_data(_id, json)
            if pagou:
                return _hash
        return False