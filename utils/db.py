import mysql.connector
from flask import Flask, g, current_app
from dotenv import load_dotenv
import os

load_dotenv()


class Database:
    """
    Clase para gestionar la conexión y operaciones básicas con MySQL en una aplicación Flask.

    Debe de ser inicializada con la configuración de la base de datos.
    Se puede registrar la conexión en el contexto de la aplicación Flask.
    Proporciona métodos para obtener la conexión, cerrar la conexión y
    inicializar la base de datos.
    """

    def __init__(self, app: Flask = None):
        """
        Inicializa la configuración de la base de datos.
        Si se pasa una instancia de Flask, registra el cierre automático de la conexión.

        :param app: Instancia de Flask (Útil para registrar el cierre de conexión en el contexto de la app).
        :type app: Flask
        :raises ValueError: Si no se proporciona la configuración de la base de datos.
        :raises TypeError: Si la aplicación no es una instancia de Flask.
        """
        self.config = {
            'host': os.getenv('MYSQL_HOST'),
            'user': os.getenv('MYSQL_USER'),
            'password': os.getenv('MYSQL_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE')
        }

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """
        Registra el método de cierre de conexión en el contexto de la app Flask.
        """
        app.teardown_appcontext(self.close_connection)

    def get_db(self):
        """
        Obtiene la conexión a la base de datos para el contexto actual.
        """
        # Chequea que la configuración de la base de datos esté presente
        if 'db' not in g:
            g.db = mysql.connector.connect(**self.config)
        return g.db

    def close_connection(self, exception):
        """
        Cierra la conexión a la base de datos al finalizar el contexto.
        """
        db = g.pop('db', None)
        if db is not None:
            db.close()

        if exception:
            current_app.logger.error(
                f"Cerrando la conexión con la excepción: {exception}")

    def init_db(self):
        """
        Inicializa la base de datos y crea la tabla 'books' si no existe.
        """
        db = mysql.connector.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password']
        )
        cursor = db.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {self.config['database']}"
        )
        db.database = self.config['database']

        # Crear la tabla 'books' si no existe | ESTO ES EXPLICITAMENTE CÓMO EJEMPLO
        # Puedes cambiar el nombre de la tabla y los campos según tus necesidades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL
            )
        ''')

        # Crear datos de prueba si es necesario
        # Puedes agregar aquí la lógica para insertar datos de prueba en la tabla
        # Por ejemplo, para insertar un libro de prueba:
        cursor.execute('''
            INSERT INTO books (title, author) VALUES ('Libro de Prueba', 'Autor de Prueba')
        ''')

        # Si necesitas crear más tablas, puedes hacerlo aquí
        # Asegúrate de definir las tablas y sus campos según tus necesidades
        # Ejemplo:
        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS users (
        #         id INT AUTO_INCREMENT PRIMARY KEY,
        #         username VARCHAR(255) NOT NULL,
        #         email VARCHAR(255) NOT NULL
        #     )
        # ''')

        db.commit()
        cursor.close()
        db.close()
