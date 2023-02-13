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


class EtheriumClp(db.Model):
    __tablename__ = 'etherium_clp'


    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    eth = db.Column(db.Float, nullable=False)
    clpinicial = db.Column(db.Float, nullable=False)
    valoreth = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
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
        query = EtheriumClp( 
            valor = dataJson['valor'],
            eth = dataJson['eth'],
            clpinicial = dataJson['clpinicial'],
            valoreth = dataJson['valoreth'],
            created_at = func.NOW(),
            )
        EtheriumClp.guardar(query)
        if query.id:                            
            return  query.id 
        return  False

    

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
