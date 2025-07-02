#!/bin/bash

# Script de configuración para AWS Linux 2023
# Este script configura el entorno Flask en un servidor AWS EC2

echo "🚀 Configurando Flask App en AWS Linux 2023..."

# Variables de configuración
APP_USER="ec2-user"
APP_DIR="/home/ec2-user/flask-app"
VENV_DIR="$APP_DIR/venv"
SERVICE_NAME="flask-app"

# Función para imprimir mensajes de estado
print_status() {
    echo "📋 $1"
}

print_status "Actualizando el sistema..."
sudo dnf update -y

print_status "Instalando dependencias del sistema..."
sudo dnf install -y python3 python3-pip nginx git

print_status "Creando directorio de la aplicación..."
sudo mkdir -p $APP_DIR
sudo chown $APP_USER:$APP_USER $APP_DIR

print_status "Configurando entorno virtual Python..."
cd $APP_DIR
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

print_status "Instalando dependencias Python..."
pip install --upgrade pip
pip install -r $APP_DIR/requirements.txt

# Si existe requirements.txt, instalar desde ahí
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

print_status "Configurando permisos..."
sudo chown -R $APP_USER:$APP_USER $APP_DIR
sudo chmod -R 755 $APP_DIR

print_status "Configurando el servicio systemd..."
sudo cp flask-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME

print_status "Configurando Nginx..."
sudo cp nginx.conf /etc/nginx/conf.d/flask-app.conf
sudo cp proxy_params /home/ec2-user/flask-app/
sudo cp nginx.conf /etc/nginx/sites-available/flask-app
sudo ln -sf /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/
sudo cp proxy_params /home/ec2-user/flask-app/

# Remover configuración por defecto de Nginx si existe
sudo rm -f /etc/nginx/sites-enabled/default
sudo rm -f /etc/nginx/conf.d/default.conf

print_status "Verificando configuración de Nginx..."
sudo nginx -t

print_status "Iniciando servicios..."
sudo systemctl start $SERVICE_NAME
sudo systemctl restart nginx
sudo systemctl enable nginx

print_status "Verificando estado de los servicios..."
echo "Estado del servicio Flask:"
sudo systemctl status $SERVICE_NAME --no-pager
echo ""
echo "Estado de Nginx:"
sudo systemctl status nginx --no-pager

print_status "✅ Configuración completada!"
echo ""
echo "Para verificar que todo funciona:"
echo "1. Verifica los logs: sudo journalctl -u $SERVICE_NAME -f"
echo "2. Prueba la aplicación: curl http://localhost/api/books"
echo "3. Verifica el socket: ls -la $APP_DIR/flask-app.sock"
echo ""
echo "Para reiniciar la aplicación después de cambios:"
echo "sudo systemctl restart $SERVICE_NAME"
