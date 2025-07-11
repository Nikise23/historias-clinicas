#!/usr/bin/env python3
"""
Script para crear un usuario de prueba con contraseña simple
"""

import json
from werkzeug.security import generate_password_hash

def crear_usuario_test():
    # Cargar usuarios existentes
    try:
        with open("usuarios.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        usuarios = []
    
    # Crear usuario de prueba
    usuario_test = {
        "usuario": "test",
        "contrasena": generate_password_hash("123456"),
        "rol": "secretaria"
    }
    
    # Verificar si ya existe
    for usuario in usuarios:
        if usuario["usuario"] == "test":
            print("Usuario 'test' ya existe")
            return
    
    # Agregar usuario
    usuarios.append(usuario_test)
    
    # Guardar
    with open("usuarios.json", "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    
    print("Usuario 'test' creado exitosamente")
    print("Usuario: test")
    print("Contraseña: 123456")
    print("Rol: secretaria")

if __name__ == "__main__":
    crear_usuario_test()