#!/usr/bin/env python3
"""
Script para verificar el contenido del archivo directamente
"""

def check_file_content():
    """Verificar el contenido del archivo"""
    print("🔍 Verificando contenido del archivo templates/secretaria.html...")
    
    try:
        with open('templates/secretaria.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
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
        
        print("\n📋 Verificando elementos en el archivo:")
        for elemento in elementos:
            if elemento in content:
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
        
        print("\n📋 Verificando secciones en el archivo:")
        for seccion in secciones:
            if seccion in content:
                print(f"✅ '{seccion}' - ENCONTRADO")
            else:
                print(f"❌ '{seccion}' - NO ENCONTRADO")
        
        # Verificar que no hay errores de JavaScript
        if "body is not defined" in content:
            print("\n❌ ERROR: Se encontró 'body is not defined' en el archivo")
        else:
            print("\n✅ No se encontraron errores de JavaScript en el archivo")
        
        # Mostrar líneas donde aparecen los elementos
        print("\n📍 Ubicación de elementos clave:")
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'total-efectivo-resumen' in line:
                print(f"   Línea {i}: {line.strip()}")
            if 'Pagos Registrados Hoy' in line:
                print(f"   Línea {i}: {line.strip()}")
        
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")

if __name__ == "__main__":
    check_file_content()