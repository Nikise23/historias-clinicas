#!/usr/bin/env python3
"""
Script para actualizar la contraseña del médico
"""

import json
from werkzeug.security import generate_password_hash

def actualizar_password_medico():
    # Cargar usuarios existentes
    try:
        with open("usuarios.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("No se encontró el archivo usuarios.json")
        return
    
    # Buscar y actualizar el usuario médico
    for usuario in usuarios:
        if usuario["usuario"] == "Marianela Bobbiesi":
            usuario["contrasena"] = generate_password_hash("123456")
            print("✅ Contraseña actualizada para Marianela Bobbiesi")
            break
    else:
        print("❌ Usuario Marianela Bobbiesi no encontrado")
        return
    
    # Guardar
    with open("usuarios.json", "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    
    print("Usuario: Marianela Bobbiesi")
    print("Nueva contraseña: 123456")
    print("Rol: medico")

if __name__ == "__main__":
    actualizar_password_medico()