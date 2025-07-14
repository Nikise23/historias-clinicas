#!/usr/bin/env python3
"""
Script de prueba para verificar la nueva funcionalidad de pacientes en sala de espera
"""

import requests
import time

# Configuración
base_url = "http://localhost:5000"
admin_credentials = {
    "usuario": "admin",
    "contrasena": "admin123"
}

def test_sala_espera_api():
    """Probar la nueva API de pacientes en sala de espera"""
    print("🧪 Probando API de pacientes en sala de espera...")
    
    session = requests.Session()
    
    # Login
    response = session.post(f"{base_url}/login", data=admin_credentials)
    
    if response.status_code != 200:
        print("❌ Error en login")
        return False
    
    # Probar obtener pacientes en sala de espera
    response = session.get(f"{base_url}/api/pacientes/sala-espera")
    
    if response.status_code == 200:
        try:
            pacientes = response.json()
            print(f"✅ API de sala de espera funciona - {len(pacientes)} pacientes encontrados")
            
            # Mostrar detalles de los pacientes
            for paciente in pacientes:
                print(f"   📋 {paciente.get('apellido', '')} {paciente.get('nombre', '')} - ${paciente.get('monto_pagado', 0)} ({paciente.get('tipo_pago', 'obra_social')})")
            
            return True
        except Exception as e:
            print(f"❌ Error parseando respuesta JSON: {e}")
            return False
    else:
        print(f"❌ Error en API de sala de espera: {response.status_code}")
        return False

def test_recepcionados_api():
    """Probar la API de pacientes recepcionados"""
    print("\n🧪 Probando API de pacientes recepcionados...")
    
    session = requests.Session()
    
    # Login
    response = session.post(f"{base_url}/login", data=admin_credentials)
    
    if response.status_code != 200:
        print("❌ Error en login")
        return False
    
    # Probar obtener pacientes recepcionados
    response = session.get(f"{base_url}/api/pacientes/recepcionados")
    
    if response.status_code == 200:
        try:
            pacientes = response.json()
            print(f"✅ API de recepcionados funciona - {len(pacientes)} pacientes encontrados")
            
            # Mostrar detalles de los pacientes
            for paciente in pacientes:
                print(f"   📋 {paciente.get('apellido', '')} {paciente.get('nombre', '')} - Pendiente de cobro")
            
            return True
        except Exception as e:
            print(f"❌ Error parseando respuesta JSON: {e}")
            return False
    else:
        print(f"❌ Error en API de recepcionados: {response.status_code}")
        return False

def test_view_elements():
    """Probar que los elementos de la vista están presentes"""
    print("\n🧪 Probando elementos de la vista...")
    
    session = requests.Session()
    
    # Login
    response = session.post(f"{base_url}/login", data=admin_credentials)
    
    if response.status_code != 200:
        print("❌ Error en login")
        return False
    
    # Obtener la vista de secretaria
    response = session.get(f"{base_url}/secretaria")
    
    if response.status_code == 200:
        html_content = response.text
        
        # Verificar elementos de sala de espera
        elementos_sala_espera = [
            'Pacientes en Sala de Espera',
            'tabla-pacientes-sala-espera',
            'cargarPacientesSalaEspera'
        ]
        
        elementos_faltantes = []
        for elemento in elementos_sala_espera:
            if elemento not in html_content:
                elementos_faltantes.append(elemento)
        
        if elementos_faltantes:
            print(f"❌ Elementos faltantes: {elementos_faltantes}")
            return False
        else:
            print("✅ Todos los elementos de sala de espera están presentes")
            return True
    else:
        print(f"❌ Error obteniendo vista: {response.status_code}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBAS DE PACIENTES EN SALA DE ESPERA")
    print("=" * 60)
    
    # Esperar a que la aplicación esté lista
    time.sleep(3)
    
    # Probar APIs
    sala_espera_ok = test_sala_espera_api()
    recepcionados_ok = test_recepcionados_api()
    view_ok = test_view_elements()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   ✅ API Sala de Espera: {'OK' if sala_espera_ok else 'FALLO'}")
    print(f"   ✅ API Recepcionados: {'OK' if recepcionados_ok else 'FALLO'}")
    print(f"   ✅ Elementos de Vista: {'OK' if view_ok else 'FALLO'}")
    
    if sala_espera_ok and recepcionados_ok and view_ok:
        print("\n🎉 ¡La nueva funcionalidad está funcionando correctamente!")
        print("   ✅ Se agregó la API de pacientes en sala de espera")
        print("   ✅ Se agregó la sección de pacientes en sala de espera en la vista")
        print("   ✅ Ahora puedes ver tanto pacientes pendientes como ya cobrados")
    else:
        print("\n❌ Hay problemas que necesitan ser corregidos.")

if __name__ == "__main__":
    main()