from app import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(64), unique=True, nullable=False)
    contrasena = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(32), nullable=False)

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    apellido = db.Column(db.String(64), nullable=False)
    dni = db.Column(db.String(16), unique=True, nullable=False)
    obra_social = db.Column(db.String(64))
    numero_obra_social = db.Column(db.String(64))
    celular = db.Column(db.String(32))
    fecha_nacimiento = db.Column(db.String(16))
    edad = db.Column(db.Integer)

class Turno(db.Model):
    __tablename__ = 'turnos'
    id = db.Column(db.Integer, primary_key=True)
    medico = db.Column(db.String(64), nullable=False)
    hora = db.Column(db.String(8), nullable=False)
    fecha = db.Column(db.String(16), nullable=False)
    dni_paciente = db.Column(db.String(16), db.ForeignKey('pacientes.dni'), nullable=False)
    estado = db.Column(db.String(32), default='sin atender')
    hora_recepcion = db.Column(db.String(8))
    hora_sala_espera = db.Column(db.String(8))
    pago_registrado = db.Column(db.Boolean, default=False)
    monto_pagado = db.Column(db.Float, default=0)

class Pago(db.Model):
    __tablename__ = 'pagos'
    id = db.Column(db.Integer, primary_key=True)
    dni_paciente = db.Column(db.String(16), db.ForeignKey('pacientes.dni'), nullable=False)
    nombre_paciente = db.Column(db.String(128))
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.String(16), nullable=False)
    hora = db.Column(db.String(8))
    fecha_registro = db.Column(db.String(32))
    observaciones = db.Column(db.String(256))
    obra_social = db.Column(db.String(64))
    tipo_pago = db.Column(db.String(32), default='efectivo')

class Agenda(db.Model):
    __tablename__ = 'agenda'
    id = db.Column(db.Integer, primary_key=True)
    medico = db.Column(db.String(64), nullable=False)
    dia = db.Column(db.String(16), nullable=False)
    horarios = db.Column(db.Text)  # JSON string

class HistoriaClinica(db.Model):
    __tablename__ = 'historias_clinicas'
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(16), db.ForeignKey('pacientes.dni'), nullable=False)
    consulta_medica = db.Column(db.Text)
    medico = db.Column(db.String(64))
    fecha_consulta = db.Column(db.String(16))
    fecha_creacion = db.Column(db.String(32))
    # Otros campos según tu modelo actual