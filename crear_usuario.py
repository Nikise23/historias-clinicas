import json
import os
from werkzeug.security import generate_password_hash

USUARIOS_FILE = "usuarios.json"


# ---------- utilidades de archivo ----------
def cargar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


# ---------- validaciones ----------
def input_no_vacio(mensaje):
    """
    Pide input hasta que el usuario escriba algo no vacío.
    Evita que con solo ENTER se continúe.
    """
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("❌ El campo no puede quedar vacío.")


# ---------- operaciones ----------
def crear_usuario():
    print("\n--- Crear nuevo usuario ---")
    usuario = input_no_vacio("Nombre de usuario: ")

    # contraseña y confirmación
    while True:
        contrasena = input_no_vacio("Contraseña: ")
        confirmar = input_no_vacio("Confirmar contraseña: ")
        if contrasena == confirmar:
            break
        print("❌ Las contraseñas no coinciden. Intentá de nuevo.")

    # rol
    while True:
        rol = input_no_vacio("Rol (medico / secretaria): ").lower()
        if rol in ("medico", "secretaria"):
            break
        print("❌ Rol inválido. Debe ser 'medico' o 'secretaria'.")

    usuarios = cargar_usuarios()
    if any(u["usuario"] == usuario for u in usuarios):
        print("❌ Ese usuario ya existe.")
        return

    usuarios.append(
        {
            "usuario": usuario,
            "contrasena": generate_password_hash(contrasena),
            "rol": rol,
        }
    )
    guardar_usuarios(usuarios)
    print(f"✅ Usuario '{usuario}' creado con rol '{rol}'.")


def eliminar_usuario():
    print("\n--- Eliminar usuario ---")
    usuarios = cargar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    print("Usuarios:")
    for u in usuarios:
        print(f" • {u['usuario']} ({u['rol']})")

    a_eliminar = input_no_vacio("Usuario a eliminar: ")
    nuevos = [u for u in usuarios if u["usuario"] != a_eliminar]

    if len(nuevos) == len(usuarios):
        print("❌ Usuario no encontrado.")
    else:
        guardar_usuarios(nuevos)
        print(f"✅ Usuario '{a_eliminar}' eliminado.")


def reiniciar_archivo():
    print("\n--- Reiniciar archivo de usuarios ---")
    confirmar = input(
        "Escribí 'SI' para confirmar que querés borrar TODOS los usuarios: "
    )
    if confirmar.upper() == "SI":
        guardar_usuarios([])
        print("✅ Archivo de usuarios reiniciado (lista vacía).")
    else:
        print("Operación cancelada.")


# ---------- menú principal ----------
def menu():
    while True:
        print("\n=== Gestión de Usuarios ===")
        print("1. Crear nuevo usuario")
        print("2. Eliminar usuario")
        print("3. Reiniciar archivo usuarios.json")
        print("4. Salir")

        opcion = input("Elegí una opción: ").strip()
        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            eliminar_usuario()
        elif opcion == "3":
            reiniciar_archivo()
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    menu()
