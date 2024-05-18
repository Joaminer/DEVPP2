from flask_sqlalchemy import SQLAlchemy

local_db = SQLAlchemy()

class Material(local_db.Model):
    id = local_db.Column(local_db.Integer, primary_key=True)
    codigo_barras = local_db.Column(local_db.String(50), unique=True, nullable=False)
    nombre = local_db.Column(local_db.String(100), nullable=False)
    estado = local_db.Column(local_db.String(50), nullable=False)
    tipo = local_db.Column(local_db.String(50), nullable=False)
    ubicacion = local_db.Column(local_db.String(100), nullable=False)
