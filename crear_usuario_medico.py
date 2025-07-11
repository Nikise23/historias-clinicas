#!/usr/bin/env python3
"""
Script para crear un usuario médico de prueba
"""

import json
from werkzeug.security import generate_password_hash

def crear_usuario_medico():
    # Cargar usuarios existentes
    try:
        with open("usuarios.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        usuarios = []
    
    # Crear usuario médico de prueba
    usuario_medico = {
        "usuario": "Marianela Bobbiesi",
        "contrasena": generate_password_hash("123456"),
        "rol": "medico"
    }
    
    # Verificar si ya existe
    for usuario in usuarios:
        if usuario["usuario"] == "Marianela Bobbiesi":
            print("Usuario médico 'Marianela Bobbiesi' ya existe")
            return
    
    # Agregar usuario
    usuarios.append(usuario_medico)
    
    # Guardar
    with open("usuarios.json", "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    
    print("Usuario médico 'Marianela Bobbiesi' creado exitosamente")
    print("Usuario: Marianela Bobbiesi")
    print("Contraseña: 123456")
    print("Rol: medico")

if __name__ == "__main__":
    crear_usuario_medico()