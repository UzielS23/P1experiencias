from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Función para conectar a la base de datos con manejo de errores
def get_db_connection():
    try:
        con = mysql.connector.connect(
            host="185.232.14.52",
            database="u760464709_tst_sep",
            user="u760464709_tst_sep_usr",
            password="dJ0CIAFF="
        )
        return con
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Ruta para mostrar todas las experiencias
@app.route('/')
def index():
    con = get_db_connection()
    if con is None:
        flash("Error al conectar a la base de datos. Inténtalo más tarde.")
        return render_template('index.html', experiencias=[])

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tst0_experiencias")
        experiencias = cursor.fetchall()
    except Error as e:
        print(f"Error al obtener experiencias: {e}")
        experiencias = []
        flash("Error al cargar las experiencias.")
    finally:
        if con:
            con.close()
    return render_template('index.html', experiencias=experiencias)

# Ruta para añadir una nueva experiencia
@app.route('/add', methods=['POST', 'GET'])
def add_experiencia():
    if request.method == 'POST':
        nombre = request.form['Nombre_Apellido']
        comentario = request.form['Comentario']
        calificacion = request.form['Calificacion']

        con = get_db_connection()
        if con is None:
            flash("Error al conectar a la base de datos. Inténtalo más tarde.")
            return redirect(url_for('index'))

        try:
            cursor = con.cursor()
            cursor.execute("INSERT INTO tst0_experiencias (Nombre_Apellido, Comentario, Calificacion) VALUES (%s, %s, %s)", 
                           (nombre, comentario, calificacion))
            con.commit()
            flash('Experiencia añadida correctamente')
        except Error as e:
            print(f"Error al añadir experiencia: {e}")
            flash("Error al añadir la experiencia. Inténtalo más tarde.")
        finally:
            if con:
                con.close()

        return redirect(url_for('index'))

    return render_template('add.html')

# Ruta para actualizar una experiencia
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update_experiencia(id):
    con = get_db_connection()
    if con is None:
        flash("Error al conectar a la base de datos. Inténtalo más tarde.")
        return redirect(url_for('index'))

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tst0_experiencias WHERE Id_Experiencia=%s", (id,))
        experiencia = cursor.fetchone()

        if request.method == 'POST':
            nombre = request.form['Nombre_Apellido']
            comentario = request.form['Comentario']
            calificacion = request.form['Calificacion']

            cursor = con.cursor()
            cursor.execute("""
                UPDATE tst0_experiencias
                SET Nombre_Apellido=%s, Comentario=%s, Calificacion=%s
                WHERE Id_Experiencia=%s
            """, (nombre, comentario, calificacion, id))
            con.commit()
            flash('Experiencia actualizada correctamente')
            return redirect(url_for('index'))
    except Error as e:
        print(f"Error al actualizar experiencia: {e}")
        flash("Error al actualizar la experiencia. Inténtalo más tarde.")
        return redirect(url_for('index'))
    finally:
        if con:
            con.close()

    return render_template('update.html', experiencia=experiencia)

# Ruta para eliminar una experiencia
@app.route('/delete/<int:id>', methods=['POST'])
def delete_experiencia(id):
    con = get_db_connection()
    if con is None:
        flash("Error al conectar a la base de datos. Inténtalo más tarde.")
        return redirect(url_for('index'))

    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM tst0_experiencias WHERE Id_Experiencia=%s", (id,))
        con.commit()
        flash('Experiencia eliminada correctamente')
    except Error as e:
        print(f"Error al eliminar experiencia: {e}")
        flash("Error al eliminar la experiencia. Inténtalo más tarde.")
    finally:
        if con:
            con.close()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
