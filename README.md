# Sistema de Gestión de Reservas de Canchas

Este proyecto es una aplicación web desarrollada en Flask para gestionar reservas de canchas, usuarios y administración.

## Requisitos
- Python 3.10 o superior
- pip

## Instalación de dependencias
Instalá las dependencias necesarias ejecutando:

```
pip install -r requirements.txt
```

## Uso
1. Ejecutá el servidor Flask:
   ```
   python run.py
   ```
2. Accedé a la aplicación en tu navegador en: http://127.0.0.1:5000/

## Funcionalidades principales
- Registro e inicio de sesión de usuarios y administradores.
- Reserva y cancelación de canchas.
- Panel de administración para gestionar canchas y reservas.
- Descarga de comprobantes e informes en JSON.
- Cancelación de reservas de cualquier usuario por parte del admin.

## Estructura de carpetas
- `app/` : Código fuente y templates.
- `data/` : Archivos de datos (usuarios, canchas, reservas).
- `app/static/` : Archivos estáticos (CSS, imágenes).

## Dependencias principales
- Flask
- pytest (para testing)

## Notas
- Asegurate de tener los archivos de datos (`usuarios.txt`, `data/canchas.txt`, `data/reservas.txt`) creados.
- Para testing, ejecutá:
  ```
  pytest
  ```

---

Cualquier duda, consultá el código o pedí ayuda.
