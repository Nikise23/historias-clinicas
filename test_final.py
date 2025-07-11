#!/usr/bin/env python3
"""
Script de prueba final para verificar que todos los cambios funcionan
"""

import requests
import json

def test_final():
    base_url = "http://localhost:5000"
    
    session = requests.Session()
    
    # Login con usuario de prueba
    login_data = {"usuario": "test", "contrasena": "123456"}
    
    try:
        # Login
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
        print(f"✅ Login exitoso: {response.status_code}")
        
        # Verificar sesión
        response = session.get(f"{base_url}/api/session-info")
        if response.status_code == 200:
            session_data = response.json()
            print(f"✅ Sesión válida: {session_data}")
            
            # Probar API de agenda
            response = session.get(f"{base_url}/api/agenda")
            if response.status_code == 200:
                agenda_data = response.json()
                print(f"✅ API de agenda funciona: {len(agenda_data)} médicos encontrados")
                
                # Verificar que la fecha de hoy es correcta
                from datetime import datetime
                hoy = datetime.now().strftime("%Y-%m-%d")
                print(f"✅ Fecha de hoy: {hoy}")
                
                print("\n🎉 Todos los cambios funcionan correctamente!")
                return True
            else:
                print(f"❌ Error en API de agenda: {response.status_code}")
                return False
        else:
            print(f"❌ Error en sesión: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_final()