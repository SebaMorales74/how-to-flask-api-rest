#!/bin/bash

# Configuración del entorno
WORK_DIR="/home/ec2-user/flask-app"
VENV_PATH="$WORK_DIR/venv"
PYTHON_VERSION="python3"

# Crear directorio de trabajo
mkdir -p $WORK_DIR
cd $WORK_DIR

# Crear entorno virtual
$PYTHON_VERSION -m venv $VENV_PATH
source $VENV_PATH/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Configurar permisos
chown -R ec2-user:ec2-user $WORK_DIR
chmod +x $WORK_DIR

echo "Aplicación configurada exitosamente"
