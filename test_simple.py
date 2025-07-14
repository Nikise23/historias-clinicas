#!/usr/bin/env python3
"""
Script de prueba simple para verificar el HTML directamente
"""

import requests

def test_html_content():
    """Probar el contenido HTML directamente"""
    print("🧪 Probando contenido HTML de la vista de secretaria...")
    
    session = requests.Session()
    
    # Login
    response = session.post("http://localhost:5000/login", data={
        "usuario": "admin",
        "contrasena": "admin123"
    })
    
    if response.status_code != 200:
        print(f"❌ Error en login: {response.status_code}")
        return
    
    # Obtener la vista de secretaria
    response = session.get("http://localhost:5000/secretaria")
    
    if response.status_code != 200:
        print(f"❌ Error obteniendo vista: {response.status_code}")
        return
    
    html_content = response.text
    
    # Buscar elementos específicos
    elementos = [
        'total-efectivo-resumen',
        'total-transferencia-resumen', 
        'total-obra-social-resumen',
        'total-recaudado-resumen',
        'cantidad-efectivo-resumen',
        'cantidad-transferencia-resumen',
        'cantidad-obra-social-resumen'
    ]
    
    print("\n📋 Verificando elementos en el HTML:")
    for elemento in elementos:
        if elemento in html_content:
            print(f"✅ {elemento} - ENCONTRADO")
        else:
            print(f"❌ {elemento} - NO ENCONTRADO")
    
    # Buscar secciones específicas
    secciones = [
        'Pagos Registrados Hoy',
        'Resumen de totales por tipo de pago',
        'Efectivo',
        'Transferencias',
        'Obra Social',
        'Total Recaudado'
    ]
    
    print("\n📋 Verificando secciones en el HTML:")
    for seccion in secciones:
        if seccion in html_content:
            print(f"✅ '{seccion}' - ENCONTRADO")
        else:
            print(f"❌ '{seccion}' - NO ENCONTRADO")
    
    # Verificar que no hay errores de JavaScript
    if "body is not defined" in html_content:
        print("\n❌ ERROR: Se encontró 'body is not defined' en el HTML")
    else:
        print("\n✅ No se encontraron errores de JavaScript")

if __name__ == "__main__":
    test_html_content()