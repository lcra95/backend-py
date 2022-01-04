# coding: utf-8

import sys, os, re
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Table, Text, Time
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from aplicacion.helpers.utilidades import Utilidades
from aplicacion.modelos.OrdenDetalle import OrdenDetalle
from aplicacion.modelos.OrdenPago import OrdenPago
from aplicacion.modelos.TipoPago import TipoPago

# db = SQLAlchemy()

from aplicacion.db import db


class Orden(db.Model):
    __tablename__ = 'orden'


    id = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.String(128), nullable=False)
    kilometros = db.Column(db.String(128), nullable=True)
    id_tipo_entrega = db.Column(db.Integer, nullable=False)
    id_sucursal = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Integer, nullable=False)
    id_creador = db.Column(db.Integer, nullable=False)
    hora_recepcion = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    hora_salida = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    id_direccion = db.Column(db.Integer, nullable=True)
    delivery = db.Column(db.Integer, nullable=True)
    informada= db.Column(db.Integer, nullable=True)
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
            estado = 1,
            delivery =dataJson['delivery'],
            kilometros =dataJson['kilometros'],
            informada =0
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
                if 'estado' in dataJson:
                    query.estado = dataJson['estado']         
                if 'delivery' in dataJson:
                    query.delivery = dataJson['delivery']         
                if 'informada' in dataJson:
                    query.informada = dataJson['informada']         
               
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
                	o.kilometros,o.delivery, p.nombre, p.apellido_paterno, t.numero as telefono,c.nombre as comuna, d.direccion_escrita, td.nombre as tipo, d.numero, d.departamento \
                FROM orden o \
                JOIN persona p ON p.id = o.id_persona \
                JOIN telefono t ON t.id_persona = p.id \
                LEFT JOIN direccion d ON d.id = o.id_direccion \
                LEFT JOIN comuna c ON c.id = d.id_comuna \
                LEFT JOIN tipo_direccion td ON td.id = d.id_tipo_direccion where o.id = '+ str(_id) +' '
       
        query = db.session.execute(sql)
        res = []
        if query:
            apellido = ''
            depto = ''
            direccion = ''
            for x in query:
                if x.departamento is not None:
                    depto = x.departamento 
                if x.direccion_escrita  is not None:
                    direccion = str(x.direccion_escrita + ", " + x.tipo + " " + depto ).upper()
                pago = OrdenPago.get_data_orden(_id)
                idtp =pago[0]["id_tipo_pago"]
                tipo_pago = TipoPago.get_data(idtp)
                pago[0]["tipo_pago"] = tipo_pago[0]["nombre"]
                if x.apellido_paterno is not None:
                    apellido = x.apellido_paterno
                temp = {
                    "nombre": x.nombre + " " + str(apellido),
                    "telefono": x.telefono,
                    "direccion" : direccion,
                    "delivery" : x.delivery,
                    "kilometros" : x.kilometros,
                    "detalle": OrdenDetalle.DetalleByOrden(_id),
                    "pago": pago
                }
                res.append(temp)
        return  res
    @classmethod
    def ordenFullInfoData(cls, _sucursal, _fecha, estado):
        sql =   "SELECT \
                    CASE WHEN o.estado = 1 then 'Pendiente' WHEN o.estado = 2 then 'En Curso' WHEN o.estado = 3 then 'Despachada' WHEN o.estado = 4 then 'Entregada' END as estado, \
                	date_format(o.created_at, '%d-%m-%Y') as fecha, \
                    date_format(o.created_at, '%H:%I:%S') as hora, o.id, \
                    concat(p.nombre,' ', p.apellido_paterno) as nombre, te.nombre as tipo_entrega, \
                    concat(d.direccion_escrita, ' ', d.numero, ' ',d.departamento ) as direccion, \
                    t.numero, c.direccion as correo, op.id_tipo_pago, op.estado as pagado \
                FROM orden o \
                JOIN persona p on p.id = o.id_persona \
                LEFT JOIN direccion d ON d.id = o.id_direccion \
                JOIN tipo_entrega te ON te.id = o.id_tipo_entrega \
                JOIN telefono t ON t.id_persona = o.id_persona \
                JOIN correo c ON c.id_persona = o.id_persona \
                JOIN orden_pago op ON op.id_orden = o.id \
                WHERE o.id_sucursal = " + str(_sucursal) + " and o.estado = " + str(estado) + " and date_format(o.created_at, '%d-%m-%Y') = '"+ str(_fecha) +"'  \
                ORDER BY o.id ASC"
       
        query = db.session.execute(sql)
        res = []
        if query:
            for x in query:
                temp = {
                    "id": x.id,
                    "estado" : x.estado,
                    "fecha": x.fecha,
                    "hora": x.hora,
                    "nombre": x.nombre,
                    "direccion" : x.direccion,
                    "tipo_entrega" : x.tipo_entrega,
                    "numero": x.numero,
                    "correo":  x.correo,
                    "tipo_pago" : x.id_tipo_pago,
                    "pagado" : x.pagado,
                    "detalle": OrdenDetalle.DetalleByOrden(x.id)
                }
                res.append(temp)
        return  res
    
    @classmethod
    def ordenToNotify(cls):
        sql =   "SELECT * FROM orden WHERE informada = 0";
       
        query = db.session.execute(sql)
        res = []
        if query:
            for x in query:
                temp = {
                    "id": x.id,
                }
                res.append(temp)
        return  res