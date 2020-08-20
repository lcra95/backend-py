# coding: utf-8

import sys, os, re
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Table, Text, Time
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from aplicacion.helpers.utilidades import Utilidades
from aplicacion.modelos.PersonaDireccion import PersonaDireccion
from aplicacion.modelos.UsuarioSucursal import UsuarioSucusrsal

# db = SQLAlchemy()

from aplicacion.db import db


class Persona(db.Model):
    __tablename__ = 'persona'


    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    apellido_paterno = db.Column(db.String(128))
    apellido_materno = db.Column(db.String(128))
    genero = db.Column(db.String(1))
    tipo_persona = db.Column(db.Integer, nullable=False)
    identificacion = db.Column(db.String(128), nullable=True)
    fecha_nacimiento = db.Column(db.Date)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    estado = db.Column(db.Integer)
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
        query = Persona( 
            nombre = dataJson['nombre'],
            apellido_paterno = dataJson['apellido_paterno'],
            apellido_materno = dataJson['apellido_materno'],
            genero = dataJson['genero'],
            tipo_persona = dataJson['tipo_persona'],
            identificacion = dataJson['identificacion'],
            fecha_nacimiento = dataJson['fecha_nacimiento'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            estado = dataJson['estado']
            )
        Persona.guardar(query)
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
                if 'apellido_paterno' in dataJson:
                    query.apellido_paterno = dataJson['apellido_paterno']
                if 'apellido_materno' in dataJson:
                    query.apellido_materno = dataJson['apellido_materno']
                if 'genero' in dataJson:
                    query.genero = dataJson['genero']
                if 'tipo_persona' in dataJson:
                    query.tipo_persona = dataJson['tipo_persona']
                if 'identificacion' in dataJson:
                    query.identificacion = dataJson['identificacion']
                if 'fecha_nacimiento' in dataJson:
                    query.fecha_nacimiento = dataJson['fecha_nacimiento']
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
    def personaFullInfo(cls, _id= None, correo = None, telefono = None, identificacion = None):
        filtro = ''

        if _id is not None:
            filtro = str(filtro) + ' AND p.id = '+str(_id)
        if correo is not None:
            filtro = str(filtro) + ' AND c.direccion = '+str(correo)
        if telefono is not None:
            filtro = str(filtro) + ' AND f.numero = '+str(telefono)
        if identificacion is not None:
            filtro = str(filtro) + " AND p.identificacion = '"+str(identificacion)+"' "
        
        
        sql =   'SELECT \
                	cl.nombre as razon, cl.giro, p.identificacion, p.id, p.nombre, p.apellido_paterno,  f.numero, c.direccion, u.correo, u.telefono, u.id as user_id \
                FROM persona p \
                JOIN telefono f ON f.id_persona = p.id \
                JOIN correo c ON c.id_persona = p.id \
                LEFT JOIN usuario u ON u.id_persona = p.id \
                LEFT JOIN cliente cl ON cl.id_persona = p.id \
                WHERE 1 = 1 '+ str(filtro) +' '
       
        query = db.session.execute(sql)
        res = []
        if query:
            for x in query:
                temp = {
                    "identificacion": x.identificacion,
                    "giro" : x.giro,
                    "razon" : x.razon,
                    "id" : x.id,
                    "nombre": x.nombre,
                    "apellido_paterno": x.apellido_paterno,
                    "telefono" : x.numero,
                    "correo" : x.correo,
                    "id_usuario" : x.user_id,
                    "direcciones" :  PersonaDireccion.dirByUser(x.id),
                    "sucursales" : UsuarioSucusrsal.get_data_user(x.user_id)
                } 
                res.append(temp)
        return  res