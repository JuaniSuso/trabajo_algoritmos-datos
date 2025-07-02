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
                         # Redirigir según el rol
                        if rol == "empleado":
                            return redirect(url_for("main.admin_panel"))
                        else:
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

        try:
            with open("usuarios.txt", "r") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(";")
                    if datos[0] == usuario:
                        flash("El nombre de usuario ya existe.")
                        return redirect(url_for("main.register"))
        except FileNotFoundError:
            pass  

        with open("usuarios.txt", "a") as archivo:
            archivo.write(f"{usuario};{contraseña};cliente;{nombre};{email};{telefono}\n")

        flash("Usuario registrado exitosamente. Iniciá sesión.")
        return redirect(url_for("main.login"))

    return render_template("register.html")



from datetime import datetime

@main.route("/perfil")
def perfil():
    if "usuario" not in session:
        flash("Tenés que iniciar sesión.")
        return redirect(url_for("main.login"))

    datos = {
        "usuario": session.get("usuario"),
        "nombre": session.get("nombre"),
        "email": session.get("email"),
        "telefono": session.get("telefono"),
    }
    reservas_usuario = []

    try:
        with open("data/reservas.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos_reserva = linea.strip().split(" - ")
                if len(datos_reserva) != 3:  # Validar que la línea tenga exactamente 3 valores
                    continue
                usuario, cancha, fecha_hora = datos_reserva
                if usuario == datos["usuario"]:
                    # Verificar si la reserva aún puede cancelarse
                    fecha_hora_obj = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M")
                    puede_cancelar = fecha_hora_obj > datetime.now()
                    reservas_usuario.append({
                        "cancha": cancha,
                        "fecha_hora": fecha_hora,
                        "puede_cancelar": puede_cancelar
                    })
    except FileNotFoundError:
        pass  # Si no existe el archivo, no pasa nada

    return render_template("perfil.html", datos=datos, reservas=reservas_usuario)

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


@main.route("/confirmar_reserva", methods=["POST"])
def confirmar_reserva():
    if "usuario" not in session:
        flash("Tenés que iniciar sesión para reservar.")
        return redirect(url_for("main.login"))

    cancha = request.form["cancha"]
    fecha_hora = request.form["fecha_hora"]
    usuario = session["usuario"]
    nueva_reserva = f"{usuario} - {cancha} - {fecha_hora}"

    canchas = [
        {"nombre": "Cancha 1", "ubicacion": "Av. Siempre Viva 123", "tipo": "Sintético", "precio": 5000},
        {"nombre": "Cancha 2", "ubicacion": "Calle Fútbol 456", "tipo": "Pasto natural", "precio": 6000},
    ]

    try:
        with open("data/reservas.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split(" - ")
                if len(datos) != 3:
                    continue
                _, c, fh = datos
                if c == cancha and fh == fecha_hora:
                    flash(f"La cancha '{cancha}' ya está reservada para el horario {fecha_hora}. Por favor, seleccioná otro horario.", "error")
                    return render_template("reserva.html", canchas=canchas)
    except FileNotFoundError:
        pass

    with open("data/reservas.txt", "a", encoding="utf-8") as archivo:
        archivo.write(nueva_reserva + "\n")
    flash(f"Reserva confirmada para {cancha} el {fecha_hora}.", "success")
    return render_template("reserva.html", canchas=canchas)


@main.route("/cancelar_reserva", methods=["POST"])
def cancelar_reserva():
    if "usuario" not in session:
        flash("Tenés que iniciar sesión.")
        return redirect(url_for("main.login"))

    reserva_a_cancelar = request.form["reserva"]
    nuevas_reservas = []

    try:
        with open("data/reservas.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.strip() != reserva_a_cancelar.strip():
                    nuevas_reservas.append(linea)
    except FileNotFoundError:
        flash("No se encontró el archivo de reservas.")
        return redirect(url_for("main.perfil"))

    # Sobrescribir el archivo con las reservas restantes
    with open("data/reservas.txt", "w", encoding="utf-8") as archivo:
        archivo.writelines(nuevas_reservas)

    flash("Reserva cancelada correctamente.")
    return redirect(url_for("main.perfil"))


@main.route('/gestion')
def gestion():
    if 'usuario' in session and session['rol'] == 'empleado':
        return render_template('gestion.html')
    return redirect(url_for('main.login'))


@main.route("/admin")
def admin_panel():
    if "usuario" not in session or session.get("rol") != "empleado":
        return redirect(url_for("main.login"))

    canchas = []
    try:
        with open("data/canchas.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                canchas.append(linea.strip().split(" - "))
    except FileNotFoundError:
        pass

    return render_template("admin.html", usuario=session["usuario"], canchas=canchas)

@main.route("/admin/agregar_cancha", methods=["GET", "POST"])
def agregar_cancha():
    if "usuario" not in session or session.get("rol") != "empleado":
        return redirect(url_for("main.login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        ubicacion = request.form["ubicacion"]
        cesped = request.form["cesped"]

        with open("data/canchas.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"{nombre} - {ubicacion} - {cesped}\n")

        flash("Cancha agregada correctamente.")
        return redirect(url_for("main.admin_panel"))

    return render_template("agregar_cancha.html")

@main.route("/ver_disponibilidad")
def ver_disponibilidad():
    # 3 canchas (índices: 0, 1, 2)
    # Matriz de 3 filas x 24 columnas 
    matriz = [[1 for _ in range(24)] for _ in range(3)]

    # Asociar nombres de cancha con índices de fila
    nombre_a_indice = {
        "Cancha 1": 0,
        "Cancha 2": 1,
        "Cancha 3": 2,
    }

    try:
        with open("data/reservas.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split(" - ")
                if len(datos) != 3:
                    continue
                _, cancha_nombre, fecha_hora = datos

                if cancha_nombre not in nombre_a_indice:
                    continue  # Si la cancha no está en nuestro mapeo

                cancha_idx = nombre_a_indice[cancha_nombre]

                # Obtener hora 
                from datetime import datetime
                try:
                    fecha_hora_obj = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M")
                    hora = fecha_hora_obj.hour
                except ValueError:
                    continue

                # Marcar como ocupada
                matriz[cancha_idx][hora] = 0
    except FileNotFoundError:
        pass  # Sin reservas aún

    # Cálculo de estadísticas
    por_cancha = [sum(fila) for fila in matriz]
    por_horario = [sum(col) for col in zip(*matriz)]

    return render_template(
        "disponibilidad.html",
        matriz=matriz,
        por_cancha=por_cancha,
        por_horario=por_horario
    )

@main.route("/admin/editar_cancha/<int:cancha_id>", methods=["GET", "POST"])
def editar_cancha(cancha_id):
    if "usuario" not in session or session.get("rol") != "empleado":
        return redirect(url_for("main.login"))
    canchas = []
    with open("data/canchas.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            canchas.append(linea.strip().split(" - "))
    if cancha_id < 0 or cancha_id >= len(canchas):
        flash("Cancha no encontrada.")
        return redirect(url_for("main.admin_panel"))
    if request.method == "POST":
        nombre = request.form["nombre"]
        ubicacion = request.form["ubicacion"]
        cesped = request.form["cesped"]
        canchas[cancha_id] = [nombre, ubicacion, cesped]
        with open("data/canchas.txt", "w", encoding="utf-8") as archivo:
            for c in canchas:
                archivo.write(" - ".join(c) + "\n")
        flash("Cancha editada correctamente.")
        return redirect(url_for("main.admin_panel"))
    cancha = canchas[cancha_id]
    return render_template("editar_cancha.html", cancha=cancha, cancha_id=cancha_id)

@main.route("/admin/eliminar_cancha/<int:cancha_id>", methods=["POST"])
def eliminar_cancha(cancha_id):
    if "usuario" not in session or session.get("rol") != "empleado":
        return redirect(url_for("main.login"))
    canchas = []
    with open("data/canchas.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            canchas.append(linea)
    if cancha_id < 0 or cancha_id >= len(canchas):
        flash("Cancha no encontrada.")
        return redirect(url_for("main.admin_panel"))
    canchas.pop(cancha_id)
    with open("data/canchas.txt", "w", encoding="utf-8") as archivo:
        archivo.writelines(canchas)
    flash("Cancha eliminada correctamente.")
    return redirect(url_for("main.admin_panel"))
