import json
from app import app, db
from models import Usuario, Paciente, Turno, Pago, Agenda, HistoriaClinica

# Archivos JSON
USUARIOS_FILE = "usuarios.json"
PACIENTES_FILE = "pacientes.json"
TURNOS_FILE = "turnos.json"
PAGOS_FILE = "pagos.json"
AGENDA_FILE = "agenda.json"
DATA_FILE = "historias_clinicas.json"

def cargar_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def migrar_usuarios():
    print("Migrando usuarios...")
    for u in cargar_json(USUARIOS_FILE):
        if not Usuario.query.filter_by(usuario=u["usuario"]).first():
            db.session.add(Usuario(
                usuario=u["usuario"],
                contrasena=u["contrasena"],
                rol=u.get("rol", "secretaria")
            ))
    db.session.commit()

def migrar_pacientes():
    print("Migrando pacientes...")
    for p in cargar_json(PACIENTES_FILE):
        if not Paciente.query.filter_by(dni=p["dni"]).first():
            db.session.add(Paciente(
                nombre=p["nombre"],
                apellido=p["apellido"],
                dni=p["dni"],
                obra_social=p.get("obra_social", ""),
                numero_obra_social=p.get("numero_obra_social", ""),
                celular=p.get("celular", ""),
                fecha_nacimiento=p.get("fecha_nacimiento", ""),
                edad=p.get("edad")
            ))
    db.session.commit()

def migrar_turnos():
    print("Migrando turnos...")
    for t in cargar_json(TURNOS_FILE):
        db.session.add(Turno(
            medico=t["medico"],
            hora=t["hora"],
            fecha=t["fecha"],
            dni_paciente=t["dni_paciente"],
            estado=t.get("estado", "sin atender"),
            hora_recepcion=t.get("hora_recepcion"),
            hora_sala_espera=t.get("hora_sala_espera"),
            pago_registrado=t.get("pago_registrado", False),
            monto_pagado=t.get("monto_pagado", 0)
        ))
    db.session.commit()

def migrar_pagos():
    print("Migrando pagos...")
    for p in cargar_json(PAGOS_FILE):
        db.session.add(Pago(
            dni_paciente=p["dni_paciente"],
            nombre_paciente=p.get("nombre_paciente", ""),
            monto=p["monto"],
            fecha=p["fecha"],
            hora=p.get("hora"),
            fecha_registro=p.get("fecha_registro"),
            observaciones=p.get("observaciones", ""),
            obra_social=p.get("obra_social", ""),
            tipo_pago=p.get("tipo_pago", "efectivo")
        ))
    db.session.commit()

def migrar_agenda():
    print("Migrando agenda...")
    for medico, dias in cargar_json(AGENDA_FILE).items():
        for dia, horarios in dias.items():
            db.session.add(Agenda(
                medico=medico,
                dia=dia,
                horarios=json.dumps(horarios)
            ))
    db.session.commit()

def migrar_historias():
    print("Migrando historias clínicas...")
    for h in cargar_json(DATA_FILE):
        db.session.add(HistoriaClinica(
            dni=h["dni"],
            consulta_medica=h.get("consulta_medica", ""),
            medico=h.get("medico", ""),
            fecha_consulta=h.get("fecha_consulta", ""),
            fecha_creacion=h.get("fecha_creacion", "")
        ))
    db.session.commit()

def main():
    with app.app_context():
        db.create_all()
        migrar_usuarios()
        migrar_pacientes()
        migrar_turnos()
        migrar_pagos()
        migrar_agenda()
        migrar_historias()
        print("¡Migración completa!")

if __name__ == "__main__":
    main()