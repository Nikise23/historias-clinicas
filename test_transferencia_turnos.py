#!/usr/bin/env python3
"""
Script de prueba para verificar la nueva funcionalidad de transferencia en gestión de turnos
"""

import requests
import time
import json

# Configuración
base_url = "http://localhost:5000"
admin_credentials = {
    "usuario": "admin",
    "contrasena": "admin123"
}

def test_api_sala_espera_transferencia():
    """Probar la API de sala de espera con tipo de pago transferencia"""
    print("🧪 Probando API de sala de espera con transferencia...")
    
    session = requests.Session()
    
    # Login
    response = session.post(f"{base_url}/login", data=admin_credentials)
    
    if response.status_code != 200:
        print("❌ Error en login")
        return False
    
    # Buscar un turno recepcionado para probar
    response = session.get(f"{base_url}/api/turnos/dia")
    
    if response.status_code != 200:
        print("❌ Error obteniendo turnos")
        return False
    
    turnos = response.json()
    turnos_recepcionados = [t for t in turnos if t.get('estado') == 'recepcionado']
    
    if not turnos_recepcionados:
        print("❌ No hay turnos recepcionados para probar")
        return False
    
    # Tomar el primer turno recepcionado
    turno = turnos_recepcionados[0]
    print(f"📋 Probando con turno: {turno.get('dni_paciente')} - {turno.get('fecha')} - {turno.get('hora')}")
    
    # Probar con transferencia
    data = {
        "dni_paciente": turno['dni_paciente'],
        "fecha": turno['fecha'],
        "hora": turno['hora'],
        "monto": 5000,
        "tipo_pago": "transferencia",
        "observaciones": "Prueba de transferencia desde gestión de turnos"
    }
    
    response = session.put(f"{base_url}/api/turnos/sala-espera", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ API de sala de espera con transferencia funciona correctamente")
        print(f"   Pago registrado: ${result['pago']['monto']} - Tipo: {result['pago']['tipo_pago']}")
        return True
    else:
        print(f"❌ Error en API: {response.status_code}")
        try:
            error = response.json()
            print(f"   Error: {error.get('error', 'Desconocido')}")
        except:
            print(f"   Respuesta: {response.text[:200]}")
        return False

def test_api_sala_espera_efectivo():
    """Probar la API de sala de espera con tipo de pago efectivo"""
    print("\n🧪 Probando API de sala de espera con efectivo...")
    
    session = requests.Session()
    
    # Login
    response = session.post(f"{base_url}/login", data=admin_credentials)
    
    if response.status_code != 200:
        print("❌ Error en login")
        return False
    
    # Buscar un turno recepcionado para probar
    response = session.get(f"{base_url}/api/turnos/dia")
    
    if response.status_code != 200:
        print("❌ Error obteniendo turnos")
        return False
    
    turnos = response.json()
    turnos_recepcionados = [t for t in turnos if t.get('estado') == 'recepcionado']
    
    if not turnos_recepcionados:
        print("❌ No hay turnos recepcionados para probar")
        return False
    
    # Tomar el segundo turno recepcionado (si existe)
    turno = turnos_recepcionados[0] if len(turnos_recepcionados) > 0 else turnos_recepcionados[0]
    print(f"📋 Probando con turno: {turno.get('dni_paciente')} - {turno.get('fecha')} - {turno.get('hora')}")
    
    # Probar con efectivo
    data = {
        "dni_paciente": turno['dni_paciente'],
        "fecha": turno['fecha'],
        "hora": turno['hora'],
        "monto": 3000,
        "tipo_pago": "efectivo",
        "observaciones": "Prueba de efectivo desde gestión de turnos"
    }
    
    response = session.put(f"{base_url}/api/turnos/sala-espera", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ API de sala de espera con efectivo funciona correctamente")
        print(f"   Pago registrado: ${result['pago']['monto']} - Tipo: {result['pago']['tipo_pago']}")
        return True
    else:
        print(f"❌ Error en API: {response.status_code}")
        try:
            error = response.json()
            print(f"   Error: {error.get('error', 'Desconocido')}")
        except:
            print(f"   Respuesta: {response.text[:200]}")
        return False

def test_api_sala_espera_obra_social():
    """Probar la API de sala de espera con obra social (monto 0)"""
    print("\n🧪 Probando API de sala de espera con obra social...")
    
    session = requests.Session()
    
    # Login
    response = session.post(f"{base_url}/login", data=admin_credentials)
    
    if response.status_code != 200:
        print("❌ Error en login")
        return False
    
    # Buscar un turno recepcionado para probar
    response = session.get(f"{base_url}/api/turnos/dia")
    
    if response.status_code != 200:
        print("❌ Error obteniendo turnos")
        return False
    
    turnos = response.json()
    turnos_recepcionados = [t for t in turnos if t.get('estado') == 'recepcionado']
    
    if not turnos_recepcionados:
        print("❌ No hay turnos recepcionados para probar")
        return False
    
    # Tomar el tercer turno recepcionado (si existe)
    turno = turnos_recepcionados[0] if len(turnos_recepcionados) > 0 else turnos_recepcionados[0]
    print(f"📋 Probando con turno: {turno.get('dni_paciente')} - {turno.get('fecha')} - {turno.get('hora')}")
    
    # Probar con obra social (monto 0)
    data = {
        "dni_paciente": turno['dni_paciente'],
        "fecha": turno['fecha'],
        "hora": turno['hora'],
        "monto": 0,
        "observaciones": "Prueba de obra social desde gestión de turnos"
    }
    
    response = session.put(f"{base_url}/api/turnos/sala-espera", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ API de sala de espera con obra social funciona correctamente")
        print(f"   Pago registrado: ${result['pago']['monto']} - Tipo: {result['pago']['tipo_pago']}")
        return True
    else:
        print(f"❌ Error en API: {response.status_code}")
        try:
            error = response.json()
            print(f"   Error: {error.get('error', 'Desconocido')}")
        except:
            print(f"   Respuesta: {response.text[:200]}")
        return False

def test_view_elements():
    """Probar que los elementos de la vista están presentes"""
    print("\n🧪 Probando elementos de la vista de gestión de turnos...")
    
    session = requests.Session()
    
    # Login
    response = session.post(f"{base_url}/login", data=admin_credentials)
    
    if response.status_code != 200:
        print("❌ Error en login")
        return False
    
    # Obtener la vista de gestión de turnos
    response = session.get(f"{base_url}/turnos/gestion")
    
    if response.status_code == 200:
        html_content = response.text
        
        # Verificar elementos de la nueva funcionalidad
        elementos_requeridos = [
            'moverASalaEspera',
            'mostrarModalCobroSalaEspera',
            'confirmarPagoSalaEspera',
            'procesarPagoSalaEspera',
            'tipo-pago-sala-espera'
        ]
        
        elementos_faltantes = []
        for elemento in elementos_requeridos:
            if elemento not in html_content:
                elementos_faltantes.append(elemento)
        
        if elementos_faltantes:
            print(f"❌ Elementos faltantes: {elementos_faltantes}")
            return False
        else:
            print("✅ Todos los elementos de la nueva funcionalidad están presentes")
            return True
    else:
        print(f"❌ Error obteniendo vista: {response.status_code}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBAS DE TRANSFERENCIA EN GESTIÓN DE TURNOS")
    print("=" * 60)
    
    # Esperar a que la aplicación esté lista
    time.sleep(3)
    
    # Probar APIs
    transferencia_ok = test_api_sala_espera_transferencia()
    efectivo_ok = test_api_sala_espera_efectivo()
    obra_social_ok = test_api_sala_espera_obra_social()
    view_ok = test_view_elements()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   ✅ API Transferencia: {'OK' if transferencia_ok else 'FALLO'}")
    print(f"   ✅ API Efectivo: {'OK' if efectivo_ok else 'FALLO'}")
    print(f"   ✅ API Obra Social: {'OK' if obra_social_ok else 'FALLO'}")
    print(f"   ✅ Elementos de Vista: {'OK' if view_ok else 'FALLO'}")
    
    if transferencia_ok and efectivo_ok and obra_social_ok and view_ok:
        print("\n🎉 ¡La nueva funcionalidad está funcionando correctamente!")
        print("   ✅ Se agregó soporte para transferencia en gestión de turnos")
        print("   ✅ Se agregó modal para seleccionar tipo de pago")
        print("   ✅ Se mantiene compatibilidad con efectivo y obra social")
        print("   ✅ Ahora puedes cobrar con transferencia desde gestión de turnos")
    else:
        print("\n❌ Hay problemas que necesitan ser corregidos.")

if __name__ == "__main__":
    main()