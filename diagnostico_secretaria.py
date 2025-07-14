#!/usr/bin/env python3
"""
Script de diagnóstico para verificar el acceso al panel de secretaria
"""

import requests
import json

# Configuración
base_url = "http://localhost:5000"

def test_login_secretaria():
    """Probar login de secretaria"""
    print("🔐 Probando login de secretaria...")
    
    session = requests.Session()
    
    # Credenciales de secretaria
    credentials = {
        "usuario": "secretaria",
        "contrasena": "secretaria123"
    }
    
    try:
        response = session.post(f"{base_url}/login", data=credentials)
        
        if response.status_code == 200:
            print("✅ Login de secretaria exitoso")
            return session
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_access_secretaria_panel(session):
    """Probar acceso al panel de secretaria"""
    print("\n🏥 Probando acceso al panel de secretaria...")
    
    try:
        response = session.get(f"{base_url}/secretaria")
        
        if response.status_code == 200:
            print("✅ Acceso al panel de secretaria exitoso")
            
            # Verificar elementos importantes en el HTML
            html_content = response.text
            
            elementos_requeridos = [
                "Panel de Secretaría",
                "Gestión de Pagos",
                "pacientes-cobrar",
                "sala-espera"
            ]
            
            elementos_faltantes = []
            for elemento in elementos_requeridos:
                if elemento not in html_content:
                    elementos_faltantes.append(elemento)
            
            if elementos_faltantes:
                print(f"⚠️  Elementos faltantes: {elementos_faltantes}")
            else:
                print("✅ Todos los elementos principales están presentes")
            
            return True
        else:
            print(f"❌ Error accediendo al panel: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_api_endpoints(session):
    """Probar endpoints de API importantes para secretaria"""
    print("\n🔌 Probando endpoints de API...")
    
    endpoints = [
        ("/api/pacientes/recepcionados", "Pacientes Recepcionados"),
        ("/api/pacientes/sala-espera", "Pacientes en Sala de Espera"),
        ("/api/pagos", "Pagos"),
        ("/api/pagos/estadisticas", "Estadísticas de Pagos")
    ]
    
    resultados = []
    
    for endpoint, nombre in endpoints:
        try:
            response = session.get(f"{base_url}{endpoint}")
            
            if response.status_code == 200:
                print(f"✅ {nombre}: OK")
                resultados.append(True)
            else:
                print(f"❌ {nombre}: Error {response.status_code}")
                resultados.append(False)
        except Exception as e:
            print(f"❌ {nombre}: Error de conexión - {e}")
            resultados.append(False)
    
    return all(resultados)

def test_session_info(session):
    """Probar información de sesión"""
    print("\n👤 Probando información de sesión...")
    
    try:
        response = session.get(f"{base_url}/api/session-info")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Usuario: {data.get('usuario', 'N/A')}")
            print(f"✅ Rol: {data.get('rol', 'N/A')}")
            return True
        else:
            print(f"❌ Error obteniendo información de sesión: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🔍 DIAGNÓSTICO DEL PANEL DE SECRETARIA")
    print("=" * 60)
    
    # Probar login
    session = test_login_secretaria()
    
    if not session:
        print("\n❌ No se pudo hacer login. Verificar:")
        print("   1. Que la aplicación esté corriendo")
        print("   2. Que las credenciales sean correctas")
        print("   3. Que no haya errores en el servidor")
        return
    
    # Probar acceso al panel
    panel_ok = test_access_secretaria_panel(session)
    
    # Probar información de sesión
    session_ok = test_session_info(session)
    
    # Probar APIs
    apis_ok = test_api_endpoints(session)
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL DIAGNÓSTICO:")
    print(f"   ✅ Login: {'OK' if session else 'FALLO'}")
    print(f"   ✅ Panel: {'OK' if panel_ok else 'FALLO'}")
    print(f"   ✅ Sesión: {'OK' if session_ok else 'FALLO'}")
    print(f"   ✅ APIs: {'OK' if apis_ok else 'FALLO'}")
    
    if session and panel_ok and session_ok and apis_ok:
        print("\n🎉 El panel de secretaria está funcionando correctamente")
        print("   Si no puedes acceder, verificar:")
        print("   1. Que estés usando las credenciales correctas")
        print("   2. Que no haya problemas de red")
        print("   3. Que el navegador no tenga caché")
    else:
        print("\n❌ Hay problemas que necesitan ser corregidos")
        print("   Revisar los errores específicos arriba")

if __name__ == "__main__":
    main()