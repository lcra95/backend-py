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


class Tasa(db.Model):
    __tablename__ = 'tasa'


    id = db.Column(db.Integer, primary_key=True)
    tasa = db.Column(db.String(90), nullable=False)
    #CRUD

    @classmethod
    def get_data(cls):
        query =  cls.query.filter_by(id=1).first()
        return  Utilidades.obtener_datos(query)

    @classmethod
    def insert(cls, dataJson):
        query = TipoProducto( 
                tasa = dataJson["tasa"],
            )
        TipoProducto.guardar(query)
        if query.id:                            
            return  query.id 
        return  False

    @classmethod
    def update_data(cls, dataJson):
        try:
            db.session.rollback()
            query = cls.query.filter_by(id=1).first()
            if query:
                if "tasa" in dataJson:
                    query.tasa = dataJson["tasa"]
               
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
