#!/usr/bin/env python3
"""
Script para crear turnos de prueba para hoy
"""

import json
from datetime import date

def cargar_json(archivo):
    """Cargar archivo JSON"""
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def guardar_json(archivo, datos):
    """Guardar archivo JSON"""
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def crear_turnos_hoy():
    """Crear turnos de prueba para hoy"""
    print("📅 Creando turnos de prueba para hoy...")
    
    # Cargar datos existentes
    turnos = cargar_json('turnos.json')
    pacientes = cargar_json('pacientes.json')
    
    fecha_hoy = date.today().isoformat()
    print(f"Fecha de hoy: {fecha_hoy}")
    
    # Verificar si ya hay turnos para hoy
    turnos_hoy = [t for t in turnos if t.get('fecha') == fecha_hoy]
    if turnos_hoy:
        print(f"⚠️ Ya existen {len(turnos_hoy)} turnos para hoy")
        return
    
    # Obtener algunos pacientes para crear turnos
    if not pacientes:
        print("❌ No hay pacientes registrados")
        return
    
    # Crear turnos de prueba
    nuevos_turnos = [
        {
            "medico": "Marianela Bobbiesi",
            "hora": "09:00",
            "fecha": fecha_hoy,
            "dni_paciente": pacientes[0]['dni'],
            "estado": "sin atender"
        },
        {
            "medico": "Marianela Bobbiesi", 
            "hora": "09:30",
            "fecha": fecha_hoy,
            "dni_paciente": pacientes[1]['dni'] if len(pacientes) > 1 else pacientes[0]['dni'],
            "estado": "recepcionado",
            "hora_recepcion": "09:15"
        },
        {
            "medico": "Francisco Colom",
            "hora": "10:00", 
            "fecha": fecha_hoy,
            "dni_paciente": pacientes[2]['dni'] if len(pacientes) > 2 else pacientes[0]['dni'],
            "estado": "sin atender"
        },
        {
            "medico": "Francisco Colom",
            "hora": "10:30",
            "fecha": fecha_hoy, 
            "dni_paciente": pacientes[3]['dni'] if len(pacientes) > 3 else pacientes[0]['dni'],
            "estado": "recepcionado",
            "hora_recepcion": "10:20"
        },
        {
            "medico": "Julieta Colom",
            "hora": "11:00",
            "fecha": fecha_hoy,
            "dni_paciente": pacientes[4]['dni'] if len(pacientes) > 4 else pacientes[0]['dni'],
            "estado": "sin atender"
        }
    ]
    
    # Agregar los nuevos turnos
    turnos.extend(nuevos_turnos)
    
    # Guardar
    guardar_json('turnos.json', turnos)
    
    print(f"✅ Creados {len(nuevos_turnos)} turnos para hoy:")
    for turno in nuevos_turnos:
        paciente = next((p for p in pacientes if p['dni'] == turno['dni_paciente']), {})
        nombre = f"{paciente.get('apellido', '')} {paciente.get('nombre', '')}".strip()
        print(f"   - {turno['hora']} | {nombre} | Estado: {turno['estado']} | Médico: {turno['medico']}")
    
    print("\n💡 Ahora puedes:")
    print("1. Ir a 'Gestión de Turnos' para ver los turnos")
    print("2. Marcar algunos como 'recepcionado'")
    print("3. Ir a 'Gestión de Pagos' para ver pacientes pendientes de cobro")

if __name__ == "__main__":
    crear_turnos_hoy()