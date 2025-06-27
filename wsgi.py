"""
WSGI Entry Point para Gunicorn
"""
from main import app

if __name__ == "__main__":
    app.run()
