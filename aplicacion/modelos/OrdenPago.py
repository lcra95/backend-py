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


class OrdenPago(db.Model):
    __tablename__ = 'orden_pago'


    id = db.Column(db.Integer, primary_key=True)
    id_tipo_pago = db.Column(db.Integer, nullable=False)
    id_orden = db.Column(db.Integer, nullable=False)
    monto = db.Column(db.Integer, nullable=False)
    voucher = db.Column(db.String(128), nullable=False)
    comprobante = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    vuelto = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Integer, nullable=False)
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
        query = OrdenPago( 
            id_tipo_pago = dataJson['id_tipo_pago'],
            id_orden = dataJson['id_orden'],
            monto = dataJson['monto'],
            voucher = dataJson['voucher'],
            comprobante = dataJson['comprobante'],
            created_at = func.NOW(),
            updated_at = func.NOW(),
            vuelto = dataJson['vuelto'],
            estado = dataJson['estado'],
            )
        OrdenPago.guardar(query)
        if query.id:                            
            return  query.id 
        return  False

    @classmethod
    def update_data(cls, _id, dataJson):
        try:
            db.session.rollback()
            query = cls.query.filter_by(id=_id).first()
            if query:
                if 'id_tipo_pago' in dataJson:
                    query.id_tipo_pago = dataJson['id_tipo_pago']
                if 'id_orden' in dataJson:
                    query.id_orden = dataJson['id_orden']
                if 'monto' in dataJson:
                    query.monto = dataJson['monto']
                if 'voucher' in dataJson:
                    query.vouvher = dataJson['voucher']
                if 'comprobante' in dataJson:
                    query.comprobante = dataJson['comprobante']
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
    def RepartidorByOrden(cls, id_orden):
        sql =   "SELECT \
                    or1.*, r.* \
                FROM orden o \
                JOIN orden_repartidor or1 ON or1.id_orden = o.id \
                JOIN repartidor r ON r.id = or1.id_tipo_pago \
                WHERE o.id = " + str(id_orden) + " "
        
        query = db.session.execute(sql)
        result = []
        if query:
            for x in query:
                temp = {
                    "id": x.id,
                    "id_tipo_pago": x.id_tipo_pago,
                    "id_orden": x.id_orden,
                    "data_repartidor": Persona.get_data(x.id_persona)
                }
                result.append(temp)
        
        return  result