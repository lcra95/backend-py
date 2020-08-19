from aplicacion.app import enviroment
from aplicacion.config import app_config
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

settings = app_config[enviroment]
Session = sessionmaker()
db = SQLAlchemy()