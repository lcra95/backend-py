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


class PersonaDireccion(db.Model):
    __tablename__ = 'persona_direccion'


    id = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, nullable=False)
    id_direccion = db.Column(db.Integer, nullable=False)
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
        query = PersonaDireccion( 
            id_persona = dataJson['id_persona'],
            id_direccion = dataJson['id_direccion'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        PersonaDireccion.guardar(query)
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
                if 'id_direccion' in dataJson:
                    query.id_direccion = dataJson['id_direccion']
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
    def DireccionByPersona(cls, id_persona):
        sql =   "SELECT \
                    d.* \
                FROM persona p \
                JOIN persona_direccion pd ON pd.id_persona = p.id \
                JOIN direccion d ON d.id = pd.id_direccion \
                JOIN tipo_direccion td ON td.id = d.id_tipo_direccion \
                where p.id = "+ str(id_persona) + " "
        
        query = db.session.execute(sql)
        result = []
        if query:
            for x in query:
                temp = {
                    "id": x.id,
                    "id_comuna": x.id_comuna,
                    "direccion_escrita": x.direccion_escrita,
                    "numero": x.numero,
                    "departamento": x.departamento,
                    "id_tipo_direccion" : x.id_tipo_direccion,
                }
                result.append(temp)
        
        return  result
    @classmethod
    def get_data_persona(cls, _id):
        query =  cls.query.filter_by(id_persona=_id).all()
        return  Utilidades.obtener_datos(query)

    @classmethod
    def dirByUser(cls, id_persona):
        sql =   "SELECT \
                	d.id AS direccion_id, d.direccion_escrita,  d.numero,td.nombre as tipo, d.departamento, c.id AS comuna_id, c.nombre as comuna, p.nombre as provincia \
                FROM persona_direccion pd \
                JOIN direccion d ON d.id = pd.id_direccion \
                JOIN comuna c ON c.id = d.id_comuna \
                JOIN tipo_direccion td ON td.id = d.id_tipo_direccion \
                JOIN provincia p ON p.id = c.id_provincia \
                WHERE pd.id_persona =" + str(id_persona)

        query = db.session.execute(sql)
        result = []
        if query:
            for x in query:
                temp = {
                    "id": x.direccion_id,
                    "id_comuna": x.comuna_id,
                    "comuna": x.comuna,
                    "provincia": x.provincia,
                    "direccion_escrita": x.direccion_escrita,
                    "numero": x.numero,
                    "departamento": x.departamento,
                    "tipo_direccion" : x.tipo,
                }
                result.append(temp)
        
        return  result