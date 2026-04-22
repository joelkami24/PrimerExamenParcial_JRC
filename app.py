from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Creamos una funcion para la BASE DE DATOS
def init_database():
    # Creamos o nos conectamos a la base de datos
    conn = sqlite3.connect("citas.db")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pacientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mascota TEXT NOT NULL,
            propietario TEXT NOT NULL,
            especie TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
init_database()
# Hasta aqui nos conectamos a la Base de Datos y creamos la tabla


@app.route("/")
def index():
    # Conexion a la base de datos
    conn = sqlite3.connect("citas.db")
    # Permite manejar registros en forma de diccionario
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()

    return render_template('index.html', pacientes=pacientes)

# Aqui creamos para que funcione: create.html
@app.route("/create")
def create():
    return render_template('create.html')
# Hasta aqui

# Añadimos la ruta para hacer el guardado
@app.route("/save", methods=['POST'])
def save():
    # Debemos recoger los datos que nos envia desde el formulario
    mascota = request.form['mascota']
    propietario = request.form['propietario']
    especie = request.form['especie']
    fecha = request.form['fecha']

    conn = sqlite3.connect("citas.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO pacientes (mascota, propietario, especie, fecha)
        VALUES (?,?,?,?)
        """,
        (mascota, propietario, especie, fecha)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route("/edit/<int:id>")
def paciente_edit(id):
    # Conexion a la base de datos
    conn = sqlite3.connect("citas.db")
    # Permite manejar registros en forma de diccionario
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes WHERE id = ?", (id,))
    paciente = cursor.fetchone()
    conn.close()
    return render_template("edit.html", paciente=paciente)

@app.route("/update", methods=['POST'])
def paciente_update():
    id = request.form['id']
    mascota = request.form['mascota']
    propietario = request.form['propietario']
    especie = request.form['especie']
    fecha = request.form['fecha']

    conn = sqlite3.connect("citas.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE pacientes SET mascota=?, propietario=?, especie=?, fecha=? WHERE id=?",
        (mascota, propietario, especie, fecha, id)
    )

    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/delete/<int:id>")
def paciente_delete(id):
    conn = sqlite3.connect("citas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)