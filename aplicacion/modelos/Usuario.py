# coding: utf-8

import sys, os, re
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Table, Text, Time
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from aplicacion.helpers.utilidades import Utilidades
from aplicacion.modelos.Persona import Persona
# db = SQLAlchemy()

from aplicacion.db import db


class Usuario(db.Model):
    __tablename__ = 'usuario'


    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(128), nullable=False)
    telefono = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    id_persona = db.Column(db.Integer, nullable=False)
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
        query = Usuario( 
            correo = dataJson['correo'],
            telefono = dataJson['telefono'],
            password = Usuario.get_user_hash(dataJson['password']),
            id_persona = dataJson['id_persona'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        Usuario.guardar(query)
        if query.id:                            
            return  query.id 
        return  False

    @classmethod
    def update_data(cls, _id, dataJson):
        try:
            db.session.rollback()
            query = cls.query.filter_by(id=_id).first()
            if query:
                if 'correo' in dataJson:
                    query.correo = dataJson['correo']
                if 'telefono' in dataJson:
                    query.telefono = dataJson['telefono']
                if 'password' in dataJson:
                    query.nombre = dataJson['password']
                if 'id_persona' in dataJson:
                    query.id_persona = dataJson['id_persona']
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
    def get_user_hash(cls, password):
        sql = 'select md5('+ str(password) +') as password from dual'
        query = db.session.execute(sql)
        if query:
            for x in query:
                return x.password 
        return  None
    @classmethod
    def get_user_login(cls,user, password):
        sql = "select * from usuario where correo = '"+ str(user) +"' or telefono ='"+ str(user) +"' and password = md5("+ str(password) +")"
        query = db.session.execute(sql)
        if query:
            for x in query:
                return Persona.personaFullInfo(x.id_persona) 
        return  None