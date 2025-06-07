from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = "Nadielosabe2233"  # Cambiar en producción por una clave segura

DATA_FILE = "historias_clinicas.json"
USUARIOS_FILE = "usuarios.json"

# ===================== Funciones auxiliares ======================

def cargar_historias():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def guardar_historias(historias):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(historias, file, indent=4)

def cargar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ========================== RUTAS ============================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contrasena = request.form.get("contrasena")
        usuarios = cargar_usuarios()

        for u in usuarios:
            if u["usuario"] == usuario and u["contrasena"] == contrasena:
                session["usuario"] = usuario
                return redirect(url_for("inicio"))
        return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

@app.route("/")
@login_requerido
def inicio():
    return render_template("index.html")

@app.route("/historias", methods=["GET"])
@login_requerido
def listar_historias():
    historias = cargar_historias()
    return jsonify(historias)

@app.route("/historias", methods=["POST"])
@login_requerido
def crear_historia():
    historias = cargar_historias()
    nueva = request.json
    if not nueva.get("dni"):
        return jsonify({"error": "DNI requerido"}), 400

    if any(h["dni"] == nueva["dni"] for h in historias):
        return jsonify({"error": "Ya existe una historia con ese DNI"}), 400

    historias.append(nueva)
    guardar_historias(historias)
    return jsonify({"mensaje": "Historia creada"}), 201

@app.route("/historias/<dni>", methods=["GET", "PUT", "DELETE"])
@login_requerido
def manejar_historia(dni):
    historias = cargar_historias()

    if request.method == "GET":
        for h in historias:
            if h["dni"] == dni:
                return jsonify(h)
        return jsonify({"error": "Historia no encontrada"}), 404

    if request.method == "PUT":
        datos = request.json
        for h in historias:
            if h["dni"] == dni:
                h.update(datos)
                guardar_historias(historias)
                return jsonify({"mensaje": "Historia modificada"})
        return jsonify({"error": "Historia no encontrada"}), 404

    if request.method == "DELETE":
        nuevas = [h for h in historias if h["dni"] != dni]
        if len(nuevas) == len(historias):
            return jsonify({"error": "Historia no encontrada"}), 404
        guardar_historias(nuevas)
        return jsonify({"mensaje": "Historia eliminada"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)




