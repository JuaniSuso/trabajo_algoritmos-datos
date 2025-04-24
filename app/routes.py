from flask import Blueprint, render_template, request, redirect, url_for, flash, session

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario_ingresado = request.form["usuario"]
        contraseña_ingresada = request.form["contraseña"]

        try:
            with open("usuarios.txt", "r") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(";")
                    if len(datos) != 6:  # Validar que la línea tenga exactamente 6 valores
                        continue
                    usuario, contraseña, rol, nombre, email, telefono = datos
                    if usuario == usuario_ingresado and contraseña == contraseña_ingresada:
                        session["usuario"] = usuario
                        session["rol"] = rol
                        session["nombre"] = nombre
                        session["email"] = email
                        session["telefono"] = telefono
                        flash(f"Bienvenido, {usuario}!")
                        return redirect(url_for("main.perfil"))
                flash("Usuario o contraseña incorrectos.")
        except FileNotFoundError:
            flash("No hay usuarios registrados aún.")
        
        return redirect(url_for("main.login"))

    return render_template("login.html")

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["telefono"]

        # Validar si el usuario ya existe
        try:
            with open("usuarios.txt", "r") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(";")
                    if datos[0] == usuario:
                        flash("El nombre de usuario ya existe.")
                        return redirect(url_for("main.register"))
        except FileNotFoundError:
            pass  # El archivo se crea si no existe

        # Guardar nuevo usuario
        with open("usuarios.txt", "a") as archivo:
            archivo.write(f"{usuario};{contraseña};cliente;{nombre};{email};{telefono}\n")

        flash("Usuario registrado exitosamente. Iniciá sesión.")
        return redirect(url_for("main.login"))

    return render_template("register.html")



@main.route("/perfil")
def perfil():
    if "usuario" not in session:
        flash("Debés iniciar sesión para ver tu perfil.")
        return redirect(url_for("main.login"))
    
    datos_usuario = {
        "usuario": session["usuario"],
        "nombre": session["nombre"],
        "email": session["email"],
        "telefono": session["telefono"]
    }
    return render_template("perfil.html", datos=datos_usuario)

@main.route("/reservar")
def reservar():
    if "usuario" not in session:
        flash("Tenés que iniciar sesión para reservar.")
        return redirect(url_for("main.login"))

    # Por ahora, usamos una lista fija de canchas de ejemplo
    canchas = [
        {"nombre": "Cancha 1", "ubicacion": "Av. Siempre Viva 123", "tipo": "Sintético", "precio": 5000},
        {"nombre": "Cancha 2", "ubicacion": "Calle Fútbol 456", "tipo": "Pasto natural", "precio": 6000},
    ]
    return render_template("reserva.html", canchas=canchas)


@main.route('/gestion')
def gestion():
    if 'usuario' in session and session['rol'] == 'empleado':
        return render_template('gestion.html')
    return redirect(url_for('main.login'))