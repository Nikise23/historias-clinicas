from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

AGENDA_FILE = "agenda.json"
HORARIOS_VALIDOS = [f"{h:02d}:{m:02d}" for h in range(9, 19+1) for m in (0, 30)]
DIAS_VALIDOS = ["lunes", "martes", "miércoles", "jueves", "viernes"]

def cargar_agenda():
    if os.path.exists(AGENDA_FILE):
        with open(AGENDA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def guardar_agenda(agenda):
    with open(AGENDA_FILE, "w", encoding="utf-8") as file:
        json.dump(agenda, file, indent=2, ensure_ascii=False)

@app.route("/agenda", methods=["GET"])
def ver_agenda_completa():
    return jsonify(cargar_agenda())

@app.route("/agenda/<medico>", methods=["GET"])
def ver_agenda_medico(medico):
    agenda = cargar_agenda()
    if medico not in agenda:
        return jsonify({"error": "Médico no encontrado"}), 404
    return jsonify(agenda[medico])

@app.route("/agenda/<medico>/<dia>", methods=["PUT"])
def actualizar_dia_agenda(medico, dia):
    datos = request.json  # Se espera una lista de horarios: ["09:00", "10:30", ...]
    if dia not in DIAS_VALIDOS:
        return jsonify({"error": "Día inválido. Solo de lunes a viernes"}), 400
    if not isinstance(datos, list) or not all(isinstance(h, str) for h in datos):
        return jsonify({"error": "Formato inválido. Enviar lista de strings (horarios)"}), 400
    if not all(hora in HORARIOS_VALIDOS for hora in datos):
        return jsonify({"error": "Uno o más horarios no están permitidos (09:00 a 19:00 cada 30 minutos)"}), 400

    agenda = cargar_agenda()
    if medico not in agenda:
        return jsonify({"error": "Médico no encontrado"}), 404

    agenda[medico][dia] = datos
    guardar_agenda(agenda)
    return jsonify({"mensaje": f"Agenda actualizada para {medico} el día {dia}"}), 200

