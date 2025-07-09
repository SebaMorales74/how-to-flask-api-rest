from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.db import Database
import os
from dotenv import load_dotenv
import logging

# Cargar variables de entorno
load_dotenv()

# Inicializa la aplicación Flask
app = Flask(__name__)

# Configurar CORS para permitir solicitudes desde cualquier origen
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuración de la aplicación
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Configuración de logging para producción
if not app.debug:
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask desplegada en modo producción')

# Inicializa la configuración de la base de datos
# Carga la configuración de la base de datos desde el archivo .env
# Establece la conexión a la base de datos
db: Database = Database(app)
db.init_db()


@app.route('/api/books', methods=['GET'])
def get_books():
    """
    ## Obtiene todos los libros de la base de datos.

    * URI: http://localhost:5000/api/books
    * Metodo: GET

    :return: Lista de libros en formato JSON.
    :rtype: JSON
    """
    # Obtener la conexión a la base de datos
    connection = db.get_db()
    # Crear un cursor para ejecutar consultas
    cursor = connection.cursor(dictionary=True)

    # Escribir la consulta SQL para obtener todos los libros
    query = "SELECT * FROM books"
    # Ejecutar la consulta
    cursor.execute(query)
    # Almacenar los resultados en una variable
    books = cursor.fetchall()

    # Cerrar el cursor y la conexión
    cursor.close()
    # Devolver los resultados en formato JSON
    return jsonify(books)


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id: int):
    """
    ## Obtiene un libro específico de la base de datos.

    * URI: http://localhost:5000/api/books/book_id
    * Metodo: GET

    :param book_id: ID del libro a obtener.
    :type book_id: int
    :return: Detalles del libro en formato JSON.
    :rtype: JSON
    :raises 404: Si el libro no se encuentra en la base de datos.
    """
    # Obtiene un libro específico de la base de datos.
    connection = db.get_db()
    # Crear un cursor para ejecutar consultas
    cursor = connection.cursor(dictionary=True)

    # Escribir la consulta SQL para obtener un libro específico
    query = 'SELECT * FROM books WHERE id = %s'
    # Ejecutar la consulta
    cursor.execute(query, (book_id,))
    # Almacenar el resultado en una variable
    row = cursor.fetchone()

    # Cerrar el cursor y la conexión
    cursor.close()
    # Devolver el resultado en formato JSON
    # Si se encuentra el libro, devolverlo; de lo contrario, devolver un error 404
    if row:
        return jsonify(row)
    else:
        return jsonify({"error": "Libro no encontrado"}), 404


@app.route('/api/books', methods=['POST'])
def create_book():
    """
    ## Crea un nuevo libro en la base de datos.

    * URI: http://localhost:5000/api/books
    * Metodo: POST

    :return: Detalles del libro creado en formato JSON.
    :rtype: JSON
    :raises 400: Si los datos de entrada son incompletos.
    """
    # Evalúa si la solicitud contiene datos JSON y si los campos 'title' y 'author' están presentes
    # Si no están presentes, devuelve un error 400
    if not request.json or 'title' not in request.json or 'author' not in request.json:
        return jsonify({"error": "Datos incompletos"}), 400
    # Si los datos son válidos, crea un nuevo libro en la base de datos
    connection = db.get_db()
    # Crear un cursor para ejecutar consultas
    cursor = connection.cursor()

    # Escribir la consulta SQL para insertar un nuevo libro
    query = 'INSERT INTO books (title, author) VALUES (%s, %s)'
    # Ejecutar la consulta con los datos del libro
    cursor.execute(query, (request.json['title'], request.json['author']))
    # Confirmar los cambios en la base de datos
    connection.commit()
    # Almacenar los resultados en una variable
    new_id = cursor.lastrowid

    # Cerrar el cursor y la conexión
    cursor.close()
    # Devolver los detalles del libro creado en formato JSON
    return jsonify({"id": new_id, "title": request.json['title'], "author": request.json['author']}), 201


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id: int):
    """
    ## Actualiza un libro existente en la base de datos.
    
    * URI: http://localhost:5000/api/books/book_id
    * Metodo: PUT

    :param book_id: ID del libro a actualizar.
    :type book_id: int
    :return: Detalles del libro actualizado en formato JSON.
    :rtype: JSON
    :raises 404: Si el libro no se encuentra en la base de datos.
    """
    connection = db.get_db()
    cursor = connection.cursor(dictionary=True)

    query = 'SELECT * FROM books WHERE id = %s'
    cursor.execute(query, (book_id,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        return jsonify({"error": "Libro no encontrado"}), 404
    else:
        title = request.json.get('title', row['title'])
        author = request.json.get('author', row['author'])
        resultado = connection.cursor()
        resultado.execute(
            'UPDATE books SET title = %s, author = %s WHERE id = %s',
            (title, author, book_id)
        )
        connection.commit()

    cursor.close()
    resultado.close()
    return jsonify({"id": book_id, "title": title, "author": author})


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id: int):
    """
    ## Elimina un libro de la base de datos.

    * URI: http://localhost:5000/api/books/book_id
    * Metodo: DELETE

    :param book_id: ID del libro a eliminar.
    :type book_id: int
    :return: Mensaje de confirmación en formato JSON.
    :rtype: JSON
    :raises 404: Si el libro no se encuentra en la base de datos.
    """
    # Elimina un libro de la base de datos.
    connection = db.get_db()
    # Crear un cursor para ejecutar consultas
    cursor = connection.cursor()

    # Verificar si el libro existe
    query = 'SELECT * FROM books WHERE id = %s'
    cursor.execute(query, (book_id,))
    row = cursor.fetchone()
    # Si el libro no existe, devolver un error 404
    if not row:
        cursor.close()
        return jsonify({"error": "Libro no encontrado"}), 404

    # Escribir la consulta SQL para eliminar un libro específico
    query = 'DELETE FROM books WHERE id = %s'
    # Ejecutar la consulta
    cursor.execute(query, (book_id,))
    # Confirmar los cambios en la base de datos
    connection.commit()

    # Cerrar el cursor
    cursor.close()
    # Mostrar un mensaje de confirmación
    return jsonify({"message": "Libro eliminado"}), 200

if __name__ == '__main__':
    # Ejecutar la aplicación Flask
    app.run(host='127.0.0.1', port=5000, debug=app.config['DEBUG'])