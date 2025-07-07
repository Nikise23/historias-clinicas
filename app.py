from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import os
from functools import wraps
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave_insegura_dev")


DATA_FILE = "historias_clinicas.json"
USUARIOS_FILE = "usuarios.json"
PACIENTES_FILE = "pacientes.json"
TURNOS_FILE = "turnos.json"
AGENDA_FILE = "agenda.json"


# ===================== Funciones auxiliares ======================


def cargar_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def guardar_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def validar_historia(data):
    campos_obligatorios = ["nombre", "dni", "diagnostico", "medico"]
    for campo in campos_obligatorios:
        if not data.get(campo) or not str(data[campo]).strip():
            return False, f"El campo '{campo}' es obligatorio."


    if not data["dni"].isdigit() or len(data["dni"]) not in [7, 8]:
        return False, "DNI inválido."


    for campo in ["fecha_nacimiento", "fecha_consulta"]:
        fecha = data.get(campo)
        if fecha:
            try:
                f = datetime.strptime(fecha, "%Y-%m-%d")
                if f > datetime.now():
                    return False, f"La fecha '{campo}' no puede ser futura."
            except ValueError:
                return False, f"Formato de fecha inválido en '{campo}'."


    return True, ""


def login_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def rol_requerido(rol_permitido):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get("rol") != rol_permitido:
                return redirect(url_for("inicio"))
            return f(*args, **kwargs)
        return decorated
    return wrapper


def rol_permitido(varios_roles):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get("rol") not in varios_roles:
                return redirect(url_for("inicio"))
            return f(*args, **kwargs)
        return decorated
    return wrapper


# ========================== RUTAS GENERALES ============================


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contrasena = request.form.get("contrasena")
        usuarios = cargar_json(USUARIOS_FILE)


        for u in usuarios:
            if u["usuario"] == usuario and check_password_hash(u["contrasena"], contrasena):
                session["usuario"] = usuario
                session["rol"] = u.get("rol", "")
                return redirect(url_for("inicio"))
        return render_template("login.html", error="Usuario o contraseña incorrectos")


    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("rol", None)
    return redirect(url_for("login"))


@app.route("/")
@login_requerido
def inicio():
    return render_template("index.html")


@app.route("/api/session-info")
@login_requerido
def session_info():
    return jsonify({
        "usuario": session.get("usuario"),
        "rol": session.get("rol")
    })


# ========================== MÉDICO ============================


@app.route("/historias", methods=["GET"])
@login_requerido
@rol_requerido("medico")
def ver_historia_clinica():
    dni = request.args.get("dni", "").strip()
    if not dni:
        return "DNI no especificado", 400
    return render_template("historia_clinica.html", dni=dni)


@app.route("/api/historias", methods=["GET"])
@login_requerido
@rol_requerido("medico")
def obtener_todas_las_historias():
    historias = cargar_json(DATA_FILE)
    return jsonify(historias)


@app.route("/historias", methods=["POST"])
@login_requerido
@rol_requerido("medico")
def crear_historia():
    historias = cargar_json(DATA_FILE)
    nueva = request.json


    valido, mensaje = validar_historia(nueva)
    if not valido:
        return jsonify({"error": mensaje}), 400


    if any(h["dni"] == nueva["dni"] for h in historias):
        return jsonify({"error": "Ya existe una historia con ese DNI"}), 400


    historias.append(nueva)
    guardar_json(DATA_FILE, historias)
    return jsonify({"mensaje": "Historia creada"}), 201


@app.route("/historias/<dni>", methods=["GET", "PUT", "DELETE"])
@login_requerido
@rol_requerido("medico")
def manejar_historia(dni):
    historias = cargar_json(DATA_FILE)


    if request.method == "GET":
        for h in historias:
            if h["dni"] == dni:
                return jsonify(h)
        return jsonify({"error": "Historia no encontrada"}), 404


    if request.method == "PUT":
        datos = request.json
        valido, mensaje = validar_historia(datos)
        if not valido:
            return jsonify({"error": mensaje}), 400


        for h in historias:
            if h["dni"] == dni:
                h.update(datos)
                guardar_json(DATA_FILE, historias)
                return jsonify({"mensaje": "Historia modificada"})
        return jsonify({"error": "Historia no encontrada"}), 404


    if request.method == "DELETE":
        nuevas = [h for h in historias if h["dni"] != dni]
        if len(nuevas) == len(historias):
            return jsonify({"error": "Historia no encontrada"}), 404
        guardar_json(DATA_FILE, nuevas)
        return jsonify({"mensaje": "Historia eliminada"})


# ========================== SECRETARIA ============================


@app.route("/pacientes")
@login_requerido
@rol_requerido("secretaria")
def vista_pacientes():
    return render_template("pacientes.html")


@app.route("/api/pacientes", methods=["GET"])
@login_requerido
@rol_permitido(["secretaria", "medico"])
def obtener_pacientes():
    pacientes = cargar_json(PACIENTES_FILE)
    pacientes.sort(key=lambda p: p.get("apellido", "").lower())
    return jsonify(pacientes)


@app.route("/api/pacientes", methods=["POST"])
@login_requerido
@rol_requerido("secretaria")
def registrar_paciente():
    data = request.json
    campos = ["nombre", "apellido", "dni", "obra_social", "numero_obra_social", "celular", "fecha_nacimiento"]
    for campo in campos:
        if not data.get(campo):
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400


    pacientes = cargar_json(PACIENTES_FILE)
    if any(p["dni"] == data["dni"] for p in pacientes):
        return jsonify({"error": "Ya existe un paciente con ese DNI"}), 400


    pacientes.append(data)
    guardar_json(PACIENTES_FILE, pacientes)
    return jsonify({"mensaje": "Paciente registrado correctamente"})


@app.route("/api/pacientes/<dni>", methods=["PUT"])
@login_requerido
@rol_requerido("secretaria")
def actualizar_paciente(dni):
    data = request.json
    campos = ["nombre", "apellido", "dni", "obra_social", "numero_obra_social", "celular", "fecha_nacimiento"]
    for campo in campos:
        if not data.get(campo):
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    pacientes = cargar_json(PACIENTES_FILE)
    for i, p in enumerate(pacientes):
        if p["dni"] == dni:
            pacientes[i] = data
            guardar_json(PACIENTES_FILE, pacientes)
            return jsonify({"mensaje": "Paciente actualizado correctamente"})
    
    return jsonify({"error": "Paciente no encontrado"}), 404


# --- Rutas para turnos y agenda ---


@app.route("/api/turnos", methods=["GET"])
@login_requerido
@rol_permitido(["secretaria", "medico"])
def obtener_turnos():
    turnos = cargar_json(TURNOS_FILE)
    pacientes = cargar_json(PACIENTES_FILE)


    for t in turnos:
        paciente = next((p for p in pacientes if p["dni"] == t["dni_paciente"]), None)
        t["paciente"] = paciente
        t["estado"] = t.get("estado", "sin atender")
    return jsonify(turnos)


@app.route("/api/turnos", methods=["POST"])
@login_requerido
@rol_requerido("secretaria")
def asignar_turno():
    data = request.json
    campos = ["medico", "hora", "fecha", "dni_paciente"]
    for campo in campos:
        if not data.get(campo):
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400


    try:
        fecha_dt = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido (usar YYYY-MM-DD)"}), 400


    dia_semana = fecha_dt.strftime("%A").upper()
    if dia_semana not in ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]:
        return jsonify({"error": "Solo se pueden asignar turnos de lunes a viernes"}), 400


    dia_es = {
        "MONDAY": "LUNES", "TUESDAY": "MARTES", "WEDNESDAY": "MIERCOLES",
        "THURSDAY": "JUEVES", "FRIDAY": "VIERNES"
    }[dia_semana]


    agenda = cargar_json(AGENDA_FILE)
    medico = data["medico"]
    if medico not in agenda:
        return jsonify({"error": "Médico no encontrado"}), 404


    horarios_disponibles = agenda[medico].get(dia_es, [])
    if data["hora"] not in horarios_disponibles:
        return jsonify({"error": f"La hora '{data['hora']}' no está disponible para el médico {medico} el día {dia_es}"}), 400


    turnos = cargar_json(TURNOS_FILE)
    if any(t["medico"] == medico and t.get("fecha") == data["fecha"] and t["hora"] == data["hora"] for t in turnos):
        return jsonify({"error": "Ya existe un turno asignado para ese horario y fecha"}), 400


    pacientes = cargar_json(PACIENTES_FILE)
    if not any(p["dni"] == data["dni_paciente"] for p in pacientes):
        return jsonify({"error": "Paciente no encontrado"}), 404


    turno_nuevo = {
        "medico": medico,
        "hora": data["hora"],
        "fecha": data["fecha"],
        "dni_paciente": data["dni_paciente"],
        "estado": "sin atender"
    }


    turnos.append(turno_nuevo)
    guardar_json(TURNOS_FILE, turnos)
    return jsonify({"mensaje": "Turno asignado correctamente"})


@app.route("/api/turnos/estado", methods=["PUT"])
@login_requerido
@rol_permitido(["medico", "secretaria"])
def actualizar_estado_turno():
    data = request.json
    dni_paciente = data.get("dni_paciente")
    fecha = data.get("fecha")
    hora = data.get("hora")
    nuevo_estado = data.get("estado")


    if nuevo_estado not in ["sin atender", "llamado", "atendido", "ausente", "recepcionado"]:
        return jsonify({"error": "Estado inválido"}), 400


    turnos = cargar_json(TURNOS_FILE)
    encontrado = False


    for turno in turnos:
        if turno["dni_paciente"] == dni_paciente and turno["fecha"] == fecha and turno["hora"] == hora:
            turno["estado"] = nuevo_estado
            encontrado = True
            break


    if not encontrado:
        return jsonify({"error": "Turno no encontrado"}), 404


    guardar_json(TURNOS_FILE, turnos)
    return jsonify({"mensaje": "Estado actualizado correctamente"})


@app.route("/api/turnos/editar", methods=["PUT"])
@login_requerido
@rol_permitido(["secretaria"])
def editar_turno():
    data = request.json
    dni_paciente = data.get("dni_paciente")
    fecha_original = data.get("fecha_original")
    hora_original = data.get("hora_original")
    nueva_fecha = data.get("nueva_fecha")
    nueva_hora = data.get("nueva_hora")

    if not all([dni_paciente, hora_original, nueva_fecha, nueva_hora]):
        return jsonify({"error": "Faltan datos requeridos"}), 400

    turnos = cargar_json(TURNOS_FILE)
    
    # Buscar el turno original
    turno_encontrado = None
    for i, turno in enumerate(turnos):
        if (turno["dni_paciente"] == dni_paciente and 
            turno.get("fecha") == fecha_original and 
            turno["hora"] == hora_original):
            turno_encontrado = i
            break

    if turno_encontrado is None:
        return jsonify({"error": "Turno no encontrado"}), 404

    # Verificar que la nueva fecha/hora no esté ocupada
    for turno in turnos:
        if (turno["medico"] == turnos[turno_encontrado]["medico"] and
            turno.get("fecha") == nueva_fecha and
            turno["hora"] == nueva_hora and
            turno["dni_paciente"] != dni_paciente):
            return jsonify({"error": "Ya existe un turno en esa fecha y hora"}), 400

    # Actualizar el turno
    turnos[turno_encontrado]["fecha"] = nueva_fecha
    turnos[turno_encontrado]["hora"] = nueva_hora
    
    guardar_json(TURNOS_FILE, turnos)
    return jsonify({"mensaje": "Turno actualizado correctamente"})


@app.route("/api/turnos/eliminar", methods=["DELETE"])
@login_requerido
@rol_permitido(["secretaria"])
def eliminar_turno():
    data = request.json
    dni_paciente = data.get("dni_paciente")
    fecha = data.get("fecha")
    hora = data.get("hora")
    medico = data.get("medico")

    if not all([dni_paciente, hora, medico]):
        return jsonify({"error": "Faltan datos requeridos"}), 400

    turnos = cargar_json(TURNOS_FILE)
    turnos_nuevos = []
    encontrado = False

    for turno in turnos:
        if (turno["dni_paciente"] == dni_paciente and
            turno.get("fecha") == fecha and
            turno["hora"] == hora and
            turno["medico"] == medico):
            encontrado = True
            continue
        turnos_nuevos.append(turno)

    if not encontrado:
        return jsonify({"error": "Turno no encontrado"}), 404

    guardar_json(TURNOS_FILE, turnos_nuevos)
    return jsonify({"mensaje": "Turno eliminado correctamente"})


@app.route("/turnos")
@login_requerido
@rol_permitido(["secretaria", "medico"])
def ver_turnos():
    return render_template("pacientes_turnos.html")


@app.route("/gestion-turnos")
@login_requerido
@rol_permitido(["secretaria"])
def gestion_turnos():
    return render_template("gestion_turnos.html")


@app.route("/gestion-pagos")
@login_requerido
@rol_permitido(["secretaria"])
def gestion_pagos():
    return render_template("gestion_pagos.html")


@app.route("/api/pacientes-atendidos")
@login_requerido
@rol_permitido(["secretaria"])
def obtener_pacientes_atendidos():
    turnos = cargar_json(TURNOS_FILE)
    pacientes = cargar_json(PACIENTES_FILE)
    
    # Filtrar turnos atendidos
    turnos_atendidos = [t for t in turnos if t.get("estado") == "atendido"]
    
    # Enriquecer con datos del paciente
    for t in turnos_atendidos:
        paciente = next((p for p in pacientes if p["dni"] == t["dni_paciente"]), {})
        t["paciente"] = paciente
    
    return jsonify(turnos_atendidos)


@app.route("/api/turnos/medico", methods=["GET"])
@login_requerido
@rol_requerido("medico")
def obtener_turnos_medico():
    usuario_medico = session.get("usuario")
    turnos = cargar_json(TURNOS_FILE)
    pacientes = cargar_json(PACIENTES_FILE)


    turnos_medico = [t for t in turnos if t.get("medico") == usuario_medico]


    # Enriquecer con datos del paciente
    for t in turnos_medico:
        paciente = next((p for p in pacientes if p["dni"] == t["dni_paciente"]), {})
        t["paciente"] = paciente
        t["estado"] = t.get("estado", "sin atender")


    return jsonify(turnos_medico)


@app.route("/agenda")
@login_requerido
@rol_requerido("secretaria")
def ver_agenda():
    return render_template("agenda.html")


@app.route("/api/agenda", methods=["GET"])
@login_requerido
@rol_requerido("secretaria")
def obtener_agenda():
    return jsonify(cargar_json(AGENDA_FILE))


@app.route("/api/agenda/<medico>/<dia>", methods=["PUT"])
@login_requerido
@rol_requerido("secretaria")
def actualizar_agenda_dia(medico, dia):
    nuevos_horarios = request.json
    if dia.upper() not in ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]:
        return jsonify({"error": "Día inválido"}), 400
    if not isinstance(nuevos_horarios, list):
        return jsonify({"error": "Formato inválido, se espera una lista"}), 400


    agenda = cargar_json(AGENDA_FILE)
    if medico not in agenda:
        agenda[medico] = {}


    agenda[medico][dia.upper()] = nuevos_horarios
    guardar_json(AGENDA_FILE, agenda)
    return jsonify({"mensaje": "Agenda actualizada correctamente"})


# ====================================================


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)