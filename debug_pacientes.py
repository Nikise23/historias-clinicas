#!/usr/bin/env python3
"""
Script de diagnóstico para verificar el estado de pacientes y turnos
"""

import json
import requests
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

def diagnosticar_problema():
    """Diagnosticar por qué no aparecen pacientes recepcionados"""
    print("🔍 DIAGNÓSTICO DE PACIENTES RECEPCIONADOS")
    print("=" * 60)
    
    # Cargar datos
    turnos = cargar_json('turnos.json')
    pacientes = cargar_json('pacientes.json')
    pagos = cargar_json('pagos.json')
    
    fecha_hoy = date.today().isoformat()
    print(f"📅 Fecha de análisis: {fecha_hoy}")
    print()
    
    # 1. Verificar turnos de hoy
    turnos_hoy = [t for t in turnos if t.get('fecha') == fecha_hoy]
    print(f"📋 Turnos de hoy: {len(turnos_hoy)}")
    
    if turnos_hoy:
        print("   Detalles de turnos:")
        for turno in turnos_hoy:
            paciente = next((p for p in pacientes if p['dni'] == turno['dni_paciente']), {})
            nombre = f"{paciente.get('apellido', '')} {paciente.get('nombre', '')}".strip()
            print(f"   - {turno['hora']} | {nombre} | Estado: {turno.get('estado', 'N/A')}")
    else:
        print("   ❌ No hay turnos para hoy")
        return
    
    print()
    
    # 2. Verificar turnos recepcionados
    turnos_recepcionados = [t for t in turnos_hoy if t.get('estado') == 'recepcionado']
    print(f"📋 Turnos recepcionados: {len(turnos_recepcionados)}")
    
    if turnos_recepcionados:
        print("   Detalles de recepcionados:")
        for turno in turnos_recepcionados:
            paciente = next((p for p in pacientes if p['dni'] == turno['dni_paciente']), {})
            nombre = f"{paciente.get('apellido', '')} {paciente.get('nombre', '')}".strip()
            print(f"   - {turno['hora']} | {nombre} | DNI: {turno['dni_paciente']}")
    else:
        print("   ❌ No hay pacientes recepcionados")
        print("   💡 Para que aparezcan pacientes aquí, primero debes:")
        print("      1. Tener turnos para hoy")
        print("      2. Marcar algunos como 'recepcionado' desde Gestión de Turnos")
        return
    
    print()
    
    # 3. Verificar pagos de hoy
    pagos_hoy = [p for p in pagos if p.get('fecha') == fecha_hoy]
    print(f"📋 Pagos de hoy: {len(pagos_hoy)}")
    
    if pagos_hoy:
        print("   Detalles de pagos:")
        for pago in pagos_hoy:
            print(f"   - DNI: {pago['dni_paciente']} | Monto: ${pago.get('monto', 0)} | Tipo: {pago.get('tipo_pago', 'N/A')}")
    else:
        print("   ✅ No hay pagos registrados para hoy")
    
    print()
    
    # 4. Verificar pacientes pendientes de cobro
    dnis_con_pago = {p['dni_paciente'] for p in pagos_hoy}
    pacientes_pendientes = []
    
    for turno in turnos_recepcionados:
        if turno['dni_paciente'] not in dnis_con_pago:
            paciente = next((p for p in pacientes if p['dni'] == turno['dni_paciente']), {})
            pacientes_pendientes.append({
                'dni': turno['dni_paciente'],
                'nombre': f"{paciente.get('apellido', '')} {paciente.get('nombre', '')}".strip(),
                'hora': turno['hora'],
                'medico': turno['medico']
            })
    
    print(f"📋 Pacientes pendientes de cobro: {len(pacientes_pendientes)}")
    
    if pacientes_pendientes:
        print("   ✅ Estos pacientes deberían aparecer en 'Pendientes de Cobro':")
        for paciente in pacientes_pendientes:
            print(f"   - {paciente['hora']} | {paciente['nombre']} | DNI: {paciente['dni']} | Médico: {paciente['medico']}")
    else:
        print("   ❌ No hay pacientes pendientes de cobro")
        if turnos_recepcionados:
            print("   💡 Esto significa que todos los pacientes recepcionados ya tienen pago registrado")
    
    print()
    
    # 5. Verificar pacientes en sala de espera
    turnos_sala_espera = [t for t in turnos_hoy if t.get('estado') == 'sala de espera']
    print(f"📋 Pacientes en sala de espera: {len(turnos_sala_espera)}")
    
    if turnos_sala_espera:
        print("   Estos pacientes ya fueron cobrados:")
        for turno in turnos_sala_espera:
            paciente = next((p for p in pacientes if p['dni'] == turno['dni_paciente']), {})
            nombre = f"{paciente.get('apellido', '')} {paciente.get('nombre', '')}".strip()
            pago = next((p for p in pagos_hoy if p['dni_paciente'] == turno['dni_paciente']), {})
            monto = pago.get('monto', 0) if pago else 0
            print(f"   - {turno['hora']} | {nombre} | Monto: ${monto}")
    
    print()
    print("=" * 60)
    print("💡 RECOMENDACIONES:")
    
    if not turnos_hoy:
        print("1. Primero crea algunos turnos para hoy")
    elif not turnos_recepcionados:
        print("1. Ve a 'Gestión de Turnos' y marca algunos pacientes como 'recepcionado'")
    elif not pacientes_pendientes:
        print("1. Los pacientes recepcionados ya fueron cobrados. Revisa la sección 'Pacientes en Sala de Espera'")
    else:
        print("1. Los pacientes pendientes deberían aparecer correctamente")

def test_api_recepcionados():
    """Probar la API de pacientes recepcionados"""
    print("\n🧪 PROBANDO API DE PACIENTES RECEPCIONADOS")
    print("=" * 60)
    
    try:
        # Login
        session = requests.Session()
        response = session.post("http://localhost:5000/login", data={
            "usuario": "admin",
            "contrasena": "admin123"
        })
        
        if response.status_code != 200:
            print("❌ Error en login")
            return
        
        # Probar API
        response = session.get("http://localhost:5000/api/pacientes/recepcionados")
        
        if response.status_code == 200:
            pacientes = response.json()
            print(f"✅ API funciona - {len(pacientes)} pacientes encontrados")
            
            if pacientes:
                print("   Detalles:")
                for paciente in pacientes:
                    print(f"   - {paciente.get('apellido', '')} {paciente.get('nombre', '')} | DNI: {paciente.get('dni', '')}")
            else:
                print("   ⚠️ La API no encuentra pacientes recepcionados")
        else:
            print(f"❌ Error en API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    diagnosticar_problema()
    test_api_recepcionados()