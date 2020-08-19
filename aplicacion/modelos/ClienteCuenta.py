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


class ClienteCuenta(db.Model):
    __tablename__ = 'cliente_cuenta'


    id = db.Column(db.Integer, primary_key=True)
    id_tipo_cuenta = db.Column(db.Integer, nullable=False)
    id_cliente = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(128), nullable=False)
    id_banco = db.Column(db.Integer, nullable=False)
    identificacion = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    numero = db.Column(db.String(256), nullable=False)
    correo = db.Column(db.String(256), nullable=False)
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
        query = ClienteCuenta( 
            nombre = dataJson['nombre'],
            id_tipo_cuenta = dataJson['id_tipo_cuenta'],
            id_cliente = dataJson['id_cliente'],
            id_banco = dataJson['id_cliente'],
            identificacion = dataJson['identificacion'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            numero = dataJson['numero'],
            correo= dataJson["correo"]
            )
        ClienteCuenta.guardar(query)
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
                if 'id_tipo_cuenta' in dataJson:
                    query.id_tipo_cuenta = dataJson['id_tipo_cuenta']
                if 'id_cliente' in dataJson:
                    query.id_cliente = dataJson['id_cliente']
                if 'id_banco' in dataJson:
                    query.id_banco = dataJson['id_banco']
                if 'identificacion' in dataJson:
                    query.identificacion = dataJson['identificacion']
                if 'created_at' in dataJson:
                    query.created_at = dataJson['created_at']         
                if 'numero' in dataJson:
                    query.numero = dataJson['numero']         
                if 'correo' in dataJson:
                    query.correo = dataJson['correo']         
               
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
    def infoCuenta(cls, id_cliente):
        sql = 'SELECT \
                	cc.nombre, cc.identificacion, b.nombre as banco, tc.nombre as tipo_cuenta, cc.numero, cc.correo \
                FROM cliente_cuenta cc \
                JOIN cliente c ON c.id = cc.id_cliente \
                JOIN banco b ON b.id = cc.id_banco \
                JOIN tipo_cuenta tc ON tc.id = cc.id_tipo_cuenta \
                WHERE cc.id_cliente =' +str(id_cliente)
        query = db.session.execute(sql)
        result = []
        if query:
            for x in query:
                temp = {
                    "nombre": x.nombre,
                    "identificacion": x.identificacion,
                    "banco": x.banco,
                    "tipo_cuenta": x.tipo_cuenta,
                    "numero": x.numero,
                    "correo": x.correo
                }
                result.append(temp)
        
        return  result