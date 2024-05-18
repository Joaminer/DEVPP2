import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from flask_migrate import Migrate
from models import local_db, Material  # Importa desde models.py

app = Flask(__name__)

# Configuración de la base de datos local (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Irma/Desktop/TEP_V6/PP/DEVPP2/instance/materials.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos local (SQLite) y Flask-Migrate
local_db.init_app(app)
migrate = Migrate(app, local_db)

# Variable para verificar si las tablas ya se han creado
tables_created = False

@app.before_request
def create_local_tables():
    global tables_created
    if not tables_created:
        with app.app_context():
            local_db.create_all()
        tables_created = True

# Función para verificar la conexión a internet
def is_internet_available():
    try:
        requests.get("http://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False

@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':
        codigo_barras = request.form['codigo_barras']
        nombre = request.form['nombre']
        estado = request.form['estado']
        tipo = request.form['tipo']
        ubicacion = request.form['ubicacion']

        # Verificar si ya existe un material con el mismo código de barras
        existing_material = Material.query.filter_by(codigo_barras=codigo_barras).first()
        if existing_material:
            flash('Ya existe un material con el mismo código de barras.', 'error')
            return redirect(url_for('add_material'))

        # Guardar en la base de datos local
        new_material = Material(codigo_barras=codigo_barras, nombre=nombre, estado=estado, tipo=tipo, ubicacion=ubicacion)
        local_db.session.add(new_material)
        local_db.session.commit()
        print(f'Datos guardados en la base de datos local: {codigo_barras}, {nombre}, {estado}, {tipo}, {ubicacion}')

        return redirect(url_for('add_material'))

    return render_template('add_material.html')

@app.route('/view_materials')
def view_materials():
    # Leer desde la base de datos local
    materials = Material.query.all()
    return render_template('view_materials.html', materials=materials)

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Puedes definir más tareas aquí si es necesario
    scheduler.start()

if __name__ == '__main__':
    start_scheduler()
    app.run(debug=True)
