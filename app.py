from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import sqlite3

def get_db_connection():
    conn = sqlite3.connect("alumnos.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to the API"})

@app.route("/base", methods=["GET"])
def base():
    return render_template('base.html')

@app.route("/home", methods=["GET"])
def home():
    return render_template('home.html')

@app.route("/about", methods=["GET"])
def about():
    return render_template('about.html')

@app.route("/alumno", methods=["GET"])
def get_all_alumnos():
    conn = get_db_connection()
    alumnos = conn.execute('SELECT * FROM alumnos').fetchall()
    conn.close()
    alumnos_lists = [dict(post) for post in alumnos]
    return jsonify(alumnos_lists)

@app.route("/alumno/<int:post_id>", methods=["GET"])
def get_one_post(post_id: int):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM alumnos WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404, description="Post not found")
    return jsonify(dict(post))


@app.route("/alumno/create", methods=["POST"])
def create_one_post():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    
    conn = get_db_connection()
    conn.execute('INSERT INTO alumnos (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    conn.close()
    return jsonify({"message": "Alumno created"})


@app.route("/alumno/edit/<int:post_id>", methods=["PUT"])
def edit_one_post(post_id):
    data = request.json
    title = data.get('title')
    content = data.get('content')

    conn = get_db_connection()
    conn.execute('UPDATE alumnos SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Alumno updated"})


@app.route("/alumno/delete/<int:post_id>", methods=["POST"])
def delete_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM alumnos WHERE id = ?', (post_id,)).fetchone()
    
    if post is None:
        abort(404)

    conn.execute('DELETE FROM alumnos WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_all_alumnos'))


# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, port=5000)
