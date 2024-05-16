# app.py
# Importar las bibliotecas necesarias
from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db
from models import db as local_db, Material
import os

# Crear la aplicación Flask
app = Flask(__name__)

# Inicializar Firebase Admin SDK
cred = credentials.Certificate("sgdd-ok-firebase-adminsdk-gcox3-fa0fd4b026.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sgdd-ok-default-rtdb.firebaseio.com/'
})

# Configurar la base de datos local (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Irma/Desktop/TEP_V6/PP/DEVPP2/instance/materials.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
local_db.init_app(app)

# Crear las tablas de la base de datos local antes de la primera solicitud
with app.app_context():
    local_db.create_all()

# Definir las rutas de la aplicación Flask
@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':
        codigo_barras = request.form['codigo_barras']
        nombre = request.form['nombre']
        estado = request.form['estado']
        tipo = request.form['tipo']
        ubicacion = request.form['ubicacion']

        # Escribir en Firebase Realtime Database
        db.reference('materials').push({
            'codigo_barras': codigo_barras,
            'nombre': nombre,
            'estado': estado,
            'tipo': tipo,
            'ubicacion': ubicacion
        })

        # Guardar en la base de datos local
        new_material = Material(codigo_barras=codigo_barras, nombre=nombre, estado=estado, tipo=tipo, ubicacion=ubicacion)
        local_db.session.add(new_material)
        local_db.session.commit()

        return redirect(url_for('add_material'))

    return render_template('add_material.html')

@app.route('/view_materials')
def view_materials():
    # Leer desde la base de datos local
    materials = Material.query.all()

    # Leer desde Firebase Realtime Database
    materials_firebase = db.reference('materials').get()

    return render_template('view_materials.html', materials=materials, materials_firebase=materials_firebase)


# Ejecutar la aplicación Flask si se ejecuta como script principal
if __name__ == '__main__':
    app.run(debug=True)
