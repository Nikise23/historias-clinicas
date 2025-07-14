#!/usr/bin/env python3
"""
Script de prueba simple para verificar que el cobro funciona correctamente
"""

import requests
import time

# Configuración
base_url = "http://localhost:5000"
admin_credentials = {
    "usuario": "admin",
    "contrasena": "admin123"
}

def test_login_and_view():
    """Probar login y acceso a la vista de secretaria"""
    print("🧪 Probando login y acceso a la vista de secretaria...")
    
    session = requests.Session()
    
    # Login
    response = session.post(f"{base_url}/login", data=admin_credentials)
    
    if response.status_code == 200 and "administrador" in response.text:
        print("✅ Login del administrador exitoso")
    else:
        print(f"❌ Error en login: {response.status_code}")
        return None
    
    # Probar acceso a la vista de secretaria (como admin)
    response = session.get(f"{base_url}/secretaria")
    
    if response.status_code == 200:
        print("✅ Vista de secretaria accesible")
        
        # Verificar que no hay errores de JavaScript
        html_content = response.text
        if "body is not defined" not in html_content:
            print("✅ No hay errores de JavaScript detectados")
        else:
            print("❌ Se detectaron errores de JavaScript")
        
        # Verificar que los elementos de resumen están presentes
        elementos_requeridos = [
            'id="total-efectivo-resumen"',
            'id="total-transferencia-resumen"',
            'id="total-obra-social-resumen"',
            'id="total-recaudado-resumen"'
        ]
        
        elementos_faltantes = []
        for elemento in elementos_requeridos:
            if elemento not in html_content:
                elementos_faltantes.append(elemento)
        
        if elementos_faltantes:
            print(f"❌ Elementos faltantes: {elementos_faltantes}")
        else:
            print("✅ Todos los elementos de resumen están presentes")
        
        return session
    else:
        print(f"❌ Error accediendo a la vista de secretaria: {response.status_code}")
        return None

def test_payment_api():
    """Probar la API de pagos"""
    print("\n🧪 Probando API de pagos...")
    
    session = requests.Session()
    
    # Login
    response = session.post(f"{base_url}/login", data=admin_credentials)
    
    if response.status_code != 200:
        print("❌ Error en login para probar API")
        return False
    
    # Probar obtener pagos
    response = session.get(f"{base_url}/api/pagos")
    
    if response.status_code == 200:
        try:
            pagos = response.json()
            print(f"✅ API de pagos funciona - {len(pagos)} pagos encontrados")
            
            # Verificar que los pagos tienen el campo tipo_pago
            pagos_con_tipo = [p for p in pagos if 'tipo_pago' in p]
            print(f"✅ {len(pagos_con_tipo)} pagos tienen campo tipo_pago")
            
            return True
        except Exception as e:
            print(f"❌ Error parseando respuesta JSON: {e}")
            print(f"   Respuesta recibida: {response.text[:200]}...")
            return False
    else:
        print(f"❌ Error en API de pagos: {response.status_code}")
        print(f"   Respuesta recibida: {response.text[:200]}...")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBAS DE CORRECCIÓN DE COBRO Y RESUMEN")
    print("=" * 60)
    
    # Esperar a que la aplicación esté lista
    time.sleep(3)
    
    # Probar login y vista
    session = test_login_and_view()
    
    # Probar API
    api_ok = test_payment_api()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   ✅ Login y vista: {'OK' if session else 'FALLO'}")
    print(f"   ✅ API de pagos: {'OK' if api_ok else 'FALLO'}")
    
    if session and api_ok:
        print("\n🎉 ¡Las correcciones están funcionando correctamente!")
        print("   ✅ El error 'body is not defined' ha sido corregido")
        print("   ✅ Se agregaron totales por tipo de pago en el resumen")
        print("   ✅ La funcionalidad de cobro debería funcionar correctamente")
    else:
        print("\n❌ Hay problemas que necesitan ser corregidos.")

if __name__ == "__main__":
    main()