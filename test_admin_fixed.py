#!/usr/bin/env python3
"""
Script de prueba para verificar que la nueva plantilla del administrador funciona correctamente
"""

import requests
import time

# Configuración
base_url = "http://localhost:5000"
admin_credentials = {
    "usuario": "admin",
    "password": "admin123"
}

def test_admin_login():
    """Probar login del administrador"""
    print("1. Probando login del administrador...")
    
    session = requests.Session()
    
    # Login
    response = session.post(f"{base_url}/login", data=admin_credentials)
    
    if response.status_code == 200 and "administrador" in response.text:
        print("✅ Login del administrador exitoso")
        return session
    else:
        print(f"❌ Error en login del administrador: {response.status_code}")
        return None

def test_admin_view(session):
    """Probar la vista del administrador con la nueva plantilla"""
    print("\n2. Probando vista del administrador con plantilla corregida...")
    
    response = session.get(f"{base_url}/administrador")
    
    if response.status_code == 200:
        print("✅ Vista del administrador carga correctamente")
        
        # Verificar que los elementos HTML están presentes
        html_content = response.text
        
        # Verificar elementos críticos
        elementos_requeridos = [
            'id="titulo-detalle-dia"',
            'id="tabla-detalle-dia"',
            'id="detalle-dia"',
            'id="tabla-ingresos-diarios"',
            'id="total-mes"',
            'id="total-consultas"',
            'id="pagos-particulares"',
            'id="pagos-obra-social"'
        ]
        
        elementos_faltantes = []
        for elemento in elementos_requeridos:
            if elemento not in html_content:
                elementos_faltantes.append(elemento)
        
        if elementos_faltantes:
            print(f"❌ Elementos faltantes en la plantilla: {elementos_faltantes}")
            return False
        else:
            print("✅ Todos los elementos HTML están presentes")
            return True
    else:
        print(f"❌ Error en vista del administrador: {response.status_code}")
        return False

def test_admin_api(session):
    """Probar la API del administrador"""
    print("\n3. Probando API de estadísticas del administrador...")
    
    # Obtener mes actual
    from datetime import datetime
    mes_actual = datetime.now().strftime("%Y-%m")
    
    response = session.get(f"{base_url}/api/pagos/estadisticas-admin?mes={mes_actual}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ API del administrador funciona correctamente")
        print(f"   - Total del mes: ${data.get('total_mes', 0)}")
        print(f"   - Consultas: {data.get('cantidad_pagos_mes', 0)}")
        print(f"   - Pagos particulares: {data.get('pagos_particulares', 0)}")
        print(f"   - Pagos obra social: {data.get('pagos_obra_social', 0)}")
        return True
    else:
        print(f"❌ Error en API del administrador: {response.status_code}")
        return False

def test_detalle_functionality(session):
    """Probar la funcionalidad de detalle del día"""
    print("\n4. Probando funcionalidad de detalle del día...")
    
    # Obtener mes actual
    from datetime import datetime
    mes_actual = datetime.now().strftime("%Y-%m")
    
    # Obtener estadísticas para ver si hay datos
    response = session.get(f"{base_url}/api/pagos/estadisticas-admin?mes={mes_actual}")
    
    if response.status_code == 200:
        data = response.json()
        detalle_por_dia = data.get('detalle_por_dia', {})
        
        if detalle_por_dia:
            # Tomar la primera fecha disponible
            primera_fecha = list(detalle_por_dia.keys())[0]
            print(f"   - Probando con fecha: {primera_fecha}")
            
            # Verificar que la fecha tiene datos
            datos_dia = detalle_por_dia[primera_fecha]
            if datos_dia.get('pacientes'):
                print(f"   - Pacientes en esta fecha: {len(datos_dia['pacientes'])}")
                print("✅ Datos disponibles para probar detalle del día")
                return True
            else:
                print("⚠️  No hay pacientes registrados para esta fecha")
                return False
        else:
            print("⚠️  No hay datos para el mes actual")
            return False
    else:
        print(f"❌ Error obteniendo datos para probar detalle: {response.status_code}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 Iniciando pruebas del panel de administrador corregido...")
    print("=" * 60)
    
    # Probar login
    session = test_admin_login()
    if not session:
        print("\n❌ No se pudo hacer login. Abortando pruebas.")
        return
    
    # Probar vista
    vista_ok = test_admin_view(session)
    if not vista_ok:
        print("\n❌ La vista del administrador tiene problemas.")
        return
    
    # Probar API
    api_ok = test_admin_api(session)
    if not api_ok:
        print("\n❌ La API del administrador tiene problemas.")
        return
    
    # Probar funcionalidad de detalle
    detalle_ok = test_detalle_functionality(session)
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   ✅ Login del administrador: {'OK' if session else 'FALLO'}")
    print(f"   ✅ Vista del administrador: {'OK' if vista_ok else 'FALLO'}")
    print(f"   ✅ API del administrador: {'OK' if api_ok else 'FALLO'}")
    print(f"   ✅ Datos para detalle: {'OK' if detalle_ok else 'SIN DATOS'}")
    
    if vista_ok and api_ok:
        print("\n🎉 ¡El panel de administrador está funcionando correctamente!")
        print("   Puedes acceder a http://localhost:5000/administrador")
        print("   Usuario: admin, Contraseña: admin123")
    else:
        print("\n❌ Hay problemas que necesitan ser corregidos.")

if __name__ == "__main__":
    main()