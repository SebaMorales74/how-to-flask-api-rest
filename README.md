# Flask y MySQL para el desarrollo de una API RESTful

Este repositorio contiene una implementación básica de una API RESTful utilizando Flask y MySQL. A continuación se detallan los conceptos fundamentales y la estructura del proyecto.

## Conceptos Básicos

<div align="center">

### Conectores de Base de Datos

<img src="https://xperti.io/wp-content/uploads/2024/03/best-databases-for-python-projects.webp" alt="Conectores de Base de Datos" width="400"/>
</div>
<br/>

Un conector de base de datos es una biblioteca de software que permite a una aplicación comunicarse con un sistema de gestión de bases de datos. En Python, existen varios conectores para diferentes tipos de bases de datos. En este proyecto, utilizamos `mysql-connector-python` para conectarnos a **MySQL**.

#### Cómo funcionan los conectores de bases de datos

Los conectores de bases de datos actúan como un puente entre tu aplicación y el servidor de base de datos:

1. **Establecen conexión**: Crean y mantienen una conexión con el servidor de la base de datos
2. **Envían consultas**: Transmiten las consultas SQL al servidor
3. **Procesan resultados**: Reciben y convierten los resultados en un formato utilizable por la aplicación
4. **Manejan transacciones**: Gestionan el inicio, confirmación o reversión de transacciones
5. **Cierran conexiones**: Liberan recursos cuando ya no son necesarios

#### Flujo de trabajo con el conector en este proyecto

En este proyecto, hemos encapsulado toda la lógica de conexión en la clase `Database` dentro del archivo db.py. El flujo general es:

1. **Inicialización**: Al crear una instancia de la clase `Database`, se cargan las credenciales desde variables de entorno
2. **Integración con Flask**: Al pasar la app Flask, se registra automáticamente el cierre de conexiones
3. **Obtención de conexión**: El método `get_db()` proporciona una conexión activa al contexto actual
4. **Uso en rutas**: Las rutas de la API utilizan la conexión para realizar operaciones CRUD
5. **Cierre automático**: La conexión se cierra automáticamente al finalizar cada solicitud


<br>
<div align="center">

### Variables de Entorno

<div style="display: flex; justify-content: center; gap: 20px;">
<img src="https://cdn-icons-png.flaticon.com/512/8631/8631491.png" alt="Variables de Entorno" width="200"/>

<img src="https://images.seeklogo.com/logo-png/33/2/python-logo-png_seeklogo-332789.png" alt="Variables de Entorno" width="200"/>
</div>

</div>

En este proyecto utilizamos la biblioteca `python-dotenv` para gestionar variables de entorno que contienen información sensible como credenciales de base de datos.

#### Por qué usar variables de entorno

Las variables de entorno son fundamentales en el desarrollo de aplicaciones modernas por varias razones:

1. **Seguridad**: Mantienen información sensible fuera del código fuente
2. **Flexibilidad**: Permiten cambiar la configuración sin modificar el código
3. **Portabilidad**: Facilitan el despliegue en diferentes entornos
4. **Buenas prácticas**: Siguen el principio de los [12 factores](https://12factor.net/) para aplicaciones modernas

#### Importancia de no exponer credenciales en el código

Incluir credenciales directamente en el código fuente es una mala práctica por varias razones críticas:

- **Riesgo de seguridad**: Si el código se comparte o se filtra, las credenciales quedan expuestas
- **Control de versiones**: Las credenciales quedan registradas en el historial de Git u otros sistemas
- **Cambios de entorno**: Requiere modificar el código para diferentes entornos (desarrollo, pruebas, producción)
- **Compartir código**: Dificulta compartir código con otros desarrolladores sin exponer credenciales

#### Cómo implementamos python-dotenv

En nuestro proyecto, `python-dotenv` se utiliza para:

1. **Cargar variables**: Al inicio de la aplicación cargamos las variables desde el archivo .env
2. **Acceder a credenciales**: Usamos `os.getenv()` para obtener las credenciales de forma segura
3. **Configurar la conexión**: Las credenciales se utilizan para configurar el conector de MySQL

Un ejemplo del archivo .env (no incluido en el repositorio):

```
MYSQL_HOST=localhost
MYSQL_USER=usuario
MYSQL_PASSWORD=contraseña_secreta
MYSQL_DATABASE=nombre_db
```

<br>
<div align="center">

### API (Application Programming Interface)

</div>

#### Qué es una API
Una API (Application Programming Interface) es una interfaz de programación de aplicaciones que permite a diferentes software comunicarse entre sí para intercambiar datos, funcionalidades y servicios. En esencia, es un puente que conecta aplicaciones, facilitando la colaboración y el intercambio de información sin necesidad de saber cómo están implementadas internamente.

Su función principal es servir cómo intermediarios, permitiendo que una aplicación solicite y reciba información o servicios de otra aplicación, como si fueran dos sistemas diferentes que se están comunicando.

<img src="https://media.geeksforgeeks.org/wp-content/uploads/20230216170349/What-is-an-API.png" alt="API" width="600"/>

#### Qué es una API RESTful
Una API RESTful (API REST) es una interfaz de programación de aplicaciones que sigue los principios de la Transferencia de Estado Representacional (REST).

Es una forma común de conectar aplicaciones y sistemas, permitiendo que intercambien información a través de la web. Las API RESTful se basan en el protocolo HTTP y utilizan métodos como GET, POST, PUT y DELETE para interactuar con recursos.

<img src="https://i0.wp.com/fragmentosdecodigo.home.blog/wp-content/uploads/2021/01/image.png?resize=816%2C454&ssl=1" alt="API RESTful" width="600"/>

#### Ejemplo de implementación básica

```python
# Obtener todos los recursos (GET)
@app.route('/api/recursos', methods=['GET'])
def get_recursos():
    # Lógica para obtener recursos
    return jsonify(recursos)

# Crear un recurso (POST)
@app.route('/api/recursos', methods=['POST'])
def create_recurso():
    # Lógica para crear un recurso
    return jsonify(nuevo_recurso), 201
```
<br>
<div align="center">

### Flask

<img src="https://flask.palletsprojects.com/en/stable/_images/flask-horizontal.png" alt="Flask Logo" width="200"/>

</div>

[Flask](https://flask.palletsprojects.com/) es un microframework web para Python que permite crear aplicaciones web y APIs de forma rápida y con un mínimo de código. Es flexible, extensible y fácil de aprender.

Te permite construir aplicaciones web de manera sencilla, sin imponer una estructura rígida. Esto lo hace ideal para proyectos pequeños y medianos, así como para prototipos y aplicaciones en producción.

#### Para qué sirve Flask

- **Desarrollo rápido**: Permite crear aplicaciones web con poco código
- **Enrutamiento sencillo**: Facilita la definición de rutas y métodos HTTP
- **Extensible**: Se puede ampliar con extensiones para ORM, autenticación, etc.
- **Ligero**: No impone una estructura rígida, permitiendo libertad de diseño

#### ¿Cómo lo vamos a útilizar?

En este proyecto, Flask se utiliza para:

1. **Crear una API RESTful**: Definimos rutas que responden a diferentes métodos HTTP
2. **Gestionar conexiones a la base de datos**: Integramos la clase `Database` con el contexto de la aplicación
3. **Procesar solicitudes JSON**: Convertimos solicitudes y respuestas entre JSON y objetos Python
4. **Manejar errores HTTP**: Devolvemos códigos de estado apropiados según la situación

## Estructura del Proyecto

### Clase Database (db.py)

La clase `Database` encapsula toda la lógica de conexión a MySQL:

```python
class Database:
    def __init__(self, app: Flask = None):
        # Inicializa la configuración desde variables de entorno
        # Registra el cierre de conexión si se proporciona app
        
    def init_app(self, app: Flask):
        # Registra el método de cierre de conexión en el contexto de la app
        
    def get_db(self):
        # Obtiene o crea una conexión para el contexto actual
        
    def close_connection(self, exception):
        # Cierra la conexión al finalizar el contexto
        
    def init_db(self):
        # Inicializa la base de datos y crea tablas si no existen
```

#### Métodos principales

- **`__init__(app=None)`**: Configura la conexión a la base de datos y opcionalmente registra el cierre automático.
- **`init_app(app)`**: Registra el método de cierre de conexión en el contexto de la aplicación Flask.
- **`get_db()`**: Obtiene una conexión a la base de datos para el contexto actual, creándola si no existe.
- **`close_connection(exception)`**: Cierra la conexión al finalizar una solicitud HTTP.
- **`init_db()`**: Inicializa la base de datos y crea la tabla 'books' si no existe.

### API de Libros (main.py)

El archivo main.py implementa una API RESTful para gestionar libros:

#### Rutas implementadas

1. **GET /api/books/**: Obtiene todos los libros
2. **GET /api/books/book_id**: Obtiene un libro específico
3. **POST /api/books/**: Crea un nuevo libro
4. **PUT /api/books/book_id**: Actualiza un libro existente
5. **DELETE /api/books/book_id**: Elimina un libro

#### Flujo en cada operación

Cada ruta sigue un patrón similar:

1. **Obtener conexión**: `connection = db.get_db()`
2. **Crear cursor**: `cursor = connection.cursor()`
3. **Ejecutar consulta**: `cursor.execute(query, params)`
4. **Procesar resultados**: `result = cursor.fetchall()` o similar
5. **Cerrar cursor**: `cursor.close()`
6. **Devolver respuesta**: `return jsonify(data), status_code`

## Uso del Proyecto

Para utilizar este proyecto:

1. **Configurar variables de entorno**: Crear un archivo .env con las credenciales de MySQL
2. **Ejecutar la aplicación**: `python main.py`
3. **Interactuar con la API**: Usar herramientas como Postman, Insomnia o curl para enviar solicitudes
4. **Probar las rutas**: Realizar pruebas a las rutas definidas para verificar su funcionamiento
5. **Consultar la documentación**: Revisar el código y comentarios para entender la lógica de cada ruta
6. **Modificar y extender**: Puedes añadir nuevas rutas o modificar las existentes según tus necesidades

