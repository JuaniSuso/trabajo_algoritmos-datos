import pytest
from flask import Flask
from app.routes import main

@pytest.fixture
def app():
    import os
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, 'app', 'templates')
    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = 'test_secret_key'
    app.register_blueprint(main)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Bienvenido' in response.data or b'bienvenido' in response.data

def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Inicio de sesi' in response.data or b'inicio de sesi' in response.data
