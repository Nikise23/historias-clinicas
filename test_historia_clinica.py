#!/usr/bin/env python3
"""
Script para probar la nueva funcionalidad de historia clínica
"""

import requests
import json

def test_historia_clinica():
    base_url = "http://localhost:5000"
    
    session = requests.Session()
    
    # Login con usuario médico
    login_data = {"usuario": "Marianela Bobbiesi", "contrasena": "123456"}
    
    try:
        # Login
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=True)
        print(f"✅ Login exitoso: {response.status_code}")
        print(f"URL final: {response.url}")
        print(f"Cookies: {dict(session.cookies)}")
        
        # Verificar sesión
        response = session.get(f"{base_url}/api/session-info")
        print(f"Session info status: {response.status_code}")
        print(f"Session info response: {response.text}")
        
        if response.status_code == 200:
            try:
                session_data = response.json()
                print(f"✅ Sesión válida: {session_data}")
                
                # Probar crear una consulta médica
                consulta_data = {
                    "dni": "37863139",
                    "consulta_medica": "Paciente consulta por dolor de cabeza. Se realiza examen físico normal. Se indica paracetamol 500mg cada 8 horas por 3 días.",
                    "fecha_consulta": "2025-07-11",
                    "medico": "Marianela Bobbiesi"
                }
                
                response = session.post(f"{base_url}/historias", json=consulta_data)
                print(f"Crear consulta status: {response.status_code}")
                print(f"Crear consulta response: {response.text}")
                
                if response.status_code == 201:
                    resultado = response.json()
                    print(f"✅ Consulta creada exitosamente: {resultado}")
                    
                    # Verificar que se guardó correctamente
                    response = session.get(f"{base_url}/api/historias")
                    if response.status_code == 200:
                        historias = response.json()
                        consulta_creada = next((h for h in historias if h.get("dni") == "37863139" and h.get("consulta_medica")), None)
                        if consulta_creada:
                            print(f"✅ Consulta encontrada en el historial: {consulta_creada.get('consulta_medica')[:50]}...")
                        else:
                            print("❌ Consulta no encontrada en el historial")
                    else:
                        print(f"❌ Error al obtener historias: {response.status_code}")
                else:
                    resultado = response.json()
                    print(f"❌ Error al crear consulta: {resultado}")
                
                return True
            except json.JSONDecodeError as e:
                print(f"❌ Error al decodificar JSON: {e}")
                print(f"Response text: {response.text}")
                return False
        else:
            print(f"❌ Error en sesión: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_historia_clinica()