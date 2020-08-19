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


class Orden(db.Model):
    __tablename__ = 'orden'


    id = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.String(128), nullable=False)
    id_tipo_entrega = db.Column(db.Integer, nullable=False)
    id_sucursal = db.Column(db.Integer, nullable=False)
    id_creador = db.Column(db.Integer, nullable=False)
    hora_recepcion = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    hora_salida = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    id_direccion = db.Column(db.Integer, nullable=True)
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
        query = Orden( 
            id_persona = dataJson['id_persona'],
            id_tipo_entrega = dataJson['id_tipo_entrega'],
            id_sucursal = dataJson['id_sucursal'],
            id_creador = dataJson['id_creador'],
            id_direccion = dataJson['id_direccion'],
            hora_recepcion = func.NOW(),
            hora_salida = dataJson['hora_salida'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        Orden.guardar(query)
        if query.id:                            
            return  query.id 
        return  False

    @classmethod
    def update_data(cls, _id, dataJson):
        try:
            db.session.rollback()
            query = cls.query.filter_by(id=_id).first()
            if query:
                if 'id_persona' in dataJson:
                    query.id_persona = dataJson['id_persona']
                if 'id_tipo_entrega' in dataJson:
                    query.id_tipo_entrega = dataJson['id_tipo_entrega']
                if 'id_sucursal' in dataJson:
                    query.id_sucursal = dataJson['id_sucursal']
                if 'id_creador' in dataJson:
                    query.id_creador = dataJson['id_creador']
                if 'id_direccion' in dataJson:
                    query.id_direccion = dataJson['id_direccion']
                if 'hora_salida' in dataJson:
                    query.hora_salida = dataJson['hora_salida']
                if 'hora_recepcion' in dataJson:
                    query.hora_recepcion = dataJson['hora_recepcion']
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

    @classmethod
    def ordenFullInfo(cls, _id):
        sql =   'SELECT \
                	p.nombre, p.apellido_paterno, t.numero as telefono,c.nombre as comuna, d.direccion_escrita, td.nombre as tipo, d.numero, d.departamento \
                FROM orden o \
                JOIN persona p ON p.id = o.id_persona \
                JOIN telefono t ON t.id_persona = p.id \
                JOIN direccion d ON d.id = o.id_direccion \
                JOIN comuna c ON c.id = d.id_comuna \
                JOIN tipo_direccion td ON td.id = d.id_tipo_direccion where o.id = '+ str(_id) +' '
       
        query = db.session.execute(sql)
        res = []
        if query:
            for x in query:
                temp = {
                    "nombre": x.nombre + " " + x.apellido_paterno,
                    "telefono": x.telefono,
                    "direccion" : x.direccion_escrita + " " + x.numero + " " + x.tipo + " " + x.departamento + ", " + x.comuna
                }
                res.append(temp)
        return  res