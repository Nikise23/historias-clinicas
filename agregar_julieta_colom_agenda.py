import json
from datetime import datetime, timedelta

NOMBRE = "Julieta Colom"

# Generar horarios de 14:05 a 19:00 cada 5 minutos
def generar_horarios():
    horarios = []
    hora = datetime.strptime("14:05", "%H:%M")
    fin = datetime.strptime("19:00", "%H:%M")
    while hora <= fin:
        horarios.append(hora.strftime("%H:%M"))
        hora += timedelta(minutes=5)
    return horarios

horarios = generar_horarios()

with open("agenda.json", "r", encoding="utf-8") as f:
    agenda = json.load(f)

if NOMBRE not in agenda:
    agenda[NOMBRE] = {
        "LUNES": [],
        "MARTES": [],
        "MIERCOLES": horarios,
        "JUEVES": [],
        "VIERNES": horarios
    }
    with open("agenda.json", "w", encoding="utf-8") as f:
        json.dump(agenda, f, indent=2, ensure_ascii=False)
    print(f"✅ Médico '{NOMBRE}' agregado a agenda.json")
else:
    print(f"ℹ️ Médico '{NOMBRE}' ya existe en agenda.json")