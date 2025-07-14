#!/usr/bin/env python3
"""
Script de prueba para verificar la API del administrador
"""

import requests
import json

def test_admin_api():
    base_url = "http://localhost:5000"
    
    # Datos de login
    login_data = {
        "usuario": "admin",
        "contrasena": "admin123"
    }
    
    # Crear sesión
    session = requests.Session()
    
    try:
        # 1. Hacer login
        print("1. Probando login...")
        response = session.post(f"{base_url}/login", data=login_data)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ Login exitoso")
        else:
            print("❌ Error en login")
            return
        
        # 2. Probar la API de estadísticas del administrador
        print("\n2. Probando API de estadísticas del administrador...")
        response = session.get(f"{base_url}/api/pagos/estadisticas-admin?mes=2025-07")
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API de estadísticas funciona")
            print(f"Datos recibidos: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Error en API de estadísticas: {response.text}")
        
        # 3. Probar la vista del administrador
        print("\n3. Probando vista del administrador...")
        response = session.get(f"{base_url}/administrador")
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Vista del administrador funciona")
        else:
            print(f"❌ Error en vista del administrador: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. Asegúrate de que la aplicación esté ejecutándose.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_admin_api()