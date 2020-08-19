# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Text, Time
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
