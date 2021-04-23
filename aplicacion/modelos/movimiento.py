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


class Movimiento(db.Model):
    __tablename__ = 'movimiento'


    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(128), nullable=False)
    id_tipo_movimiento = db.Column(db.Integer, nullable=False)
    monto = db.Column(db.Integer, nullable=False)
    id_centro_costo = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    fecha = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
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
        query = Movimiento( 
            concepto = dataJson['concepto'],
            id_tipo_movimiento = dataJson['id_tipo_movimiento'],
            monto = dataJson['monto'],
            id_centro_costo = dataJson['id_centro_costo'],
            fecha = dataJson['fecha'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            )
        Movimiento.guardar(query)
        if query.id:                            
            return  query.id 
        return  False

    @classmethod
    def update_data(cls, _id, dataJson):
        try:
            db.session.rollback()
            query = cls.query.filter_by(id=_id).first()
            if query:
                if 'concepto' in dataJson:
                    query.concepto = dataJson['concepto']
                if 'id_tipo_movimiento' in dataJson:
                    query.id_tipo_movimiento = dataJson['id_tipo_movimiento']
                if 'monto' in dataJson:
                    query.monto = dataJson['monto']
                if 'id_centro_costo' in dataJson:
                    query.id_centro_costo = dataJson['id_centro_costo']
                if 'fecha' in dataJson:
                    query.fecha = dataJson['fecha']
                               
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
    def get_data_fecha(cls, fecha_ini, fecha_fin = None, tipo_movimiento = None):
        filtro = ' '
        if fecha_fin is None:
            filtro += "AND m.fecha = '" + str(fecha_ini) + "' "
        else:
            filtro += "AND m.fecha >= '" + str(fecha_ini) + "' AND m.fecha <= '" + str(fecha_fin) +"' " 

        if tipo_movimiento is not None:
            filtro += "AND m.id_tipo_movimiento = " +str(tipo_movimiento)

        sql = "SELECT \
                    m.fecha, \
                    if(tm.id = 1, m.monto, m.monto*-1 ) as monto_bruto, \
                    (m.monto * cc.comision) as comision, \
                    m.concepto, \
                    cc.descripcion \
                FROM movimiento m \
                JOIN tipo_movimiento tm ON tm.id = m.id_tipo_movimiento \
                JOIN centro_costo cc ON cc.id = m.id_centro_costo \
                WHERE 1 = 1 " + str(filtro)
        
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(sql)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        query = db.session.execute(sql)
        result = []
        if query:
            for x in query:
                temp = {
                   "fecha": str(x.fecha),
                   "monto_bruto": x.monto_bruto,
                   "comision": str(x.comision),
                   "concepto": x.concepto,
                   "descripcion": x.descripcion
                }
                result.append(temp)
        
        return  result
