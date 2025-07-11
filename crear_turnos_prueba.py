#!/usr/bin/env python3
"""
Script para crear turnos de prueba para el médico
"""

import json
from datetime import date

def crear_turnos_prueba():
    # Cargar datos existentes
    try:
        with open("turnos.json", "r", encoding="utf-8") as f:
            turnos = json.load(f)
    except FileNotFoundError:
        turnos = []
    
    try:
        with open("pacientes.json", "r", encoding="utf-8") as f:
            pacientes = json.load(f)
    except FileNotFoundError:
        print("No se encontró el archivo pacientes.json")
        return
    
    # Obtener fecha de hoy
    hoy = date.today().isoformat()
    
    # Crear turnos de prueba para diferentes estados
    turnos_prueba = [
        {
            "dni_paciente": "37863139",
            "medico": "Marianela Bobbiesi",
            "fecha": hoy,
            "hora": "14:05",
            "estado": "sala de espera",
            "hora_sala_espera": "14:00"
        },
        {
            "dni_paciente": "40022695",
            "medico": "Marianela Bobbiesi", 
            "fecha": hoy,
            "hora": "14:10",
            "estado": "llamado",
            "hora_sala_espera": "14:02",
            "hora_llamado": "14:08"
        },
        {
            "dni_paciente": "38099876",
            "medico": "Marianela Bobbiesi",
            "fecha": hoy,
            "hora": "14:15",
            "estado": "atendido",
            "hora_sala_espera": "14:05",
            "hora_llamado": "14:12",
            "hora_atendido": "14:15"
        }
    ]
    
    # Verificar que los pacientes existen
    dnis_pacientes = [p["dni"] for p in pacientes]
    turnos_validos = []
    
    for turno in turnos_prueba:
        if turno["dni_paciente"] in dnis_pacientes:
            # Verificar si el turno ya existe
            existe = any(t["dni_paciente"] == turno["dni_paciente"] and 
                        t["fecha"] == turno["fecha"] and 
                        t["hora"] == turno["hora"] for t in turnos)
            
            if not existe:
                turnos_validos.append(turno)
                print(f"✅ Turno creado: {turno['dni_paciente']} - {turno['hora']} - {turno['estado']}")
            else:
                print(f"⚠️ Turno ya existe: {turno['dni_paciente']} - {turno['hora']}")
        else:
            print(f"❌ Paciente no encontrado: {turno['dni_paciente']}")
    
    # Agregar turnos válidos
    turnos.extend(turnos_validos)
    
    # Guardar
    with open("turnos.json", "w", encoding="utf-8") as f:
        json.dump(turnos, f, indent=4, ensure_ascii=False)
    
    print(f"\n🎉 Se crearon {len(turnos_validos)} turnos de prueba")
    print("Los turnos están disponibles para el médico 'Marianela Bobbiesi'")

if __name__ == "__main__":
    crear_turnos_prueba()