from flask import Flask

def crear_app():
    app = Flask(__name__)
    app.secret_key = 'clave_secreta_facundo'  # para sesiones y seguridad

    from .routes import main
    app.register_blueprint(main)

    return app
