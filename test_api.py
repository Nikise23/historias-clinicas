#!/usr/bin/env python3
"""
Script de prueba para verificar la API de agenda
"""

import requests
import json

def test_agenda_api():
    base_url = "http://localhost:5000"
    
    # Primero hacer login
    login_data = {
        "usuario": "secretaria",
        "contrasena": "123456"
    }
    
    session = requests.Session()
    
    try:
        # Login
        response = session.post(f"{base_url}/login", data=login_data)
        print(f"Login status: {response.status_code}")
        
        if response.status_code == 200:
            # Probar la API de agenda
            response = session.get(f"{base_url}/api/agenda")
            print(f"API agenda status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type', 'No especificado')}")
            print(f"Respuesta completa: {response.text[:500]}...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("✅ API de agenda funciona correctamente")
                    print(f"Datos recibidos: {json.dumps(data, indent=2, ensure_ascii=False)}")
                    return True
                except json.JSONDecodeError as e:
                    print(f"❌ Error al decodificar JSON: {e}")
                    print(f"Contenido de respuesta: {response.text}")
                    return False
            else:
                print(f"❌ Error en API de agenda: {response.text}")
                return False
        else:
            print(f"❌ Error en login: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. Asegúrate de que la aplicación esté ejecutándose.")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    test_agenda_api()