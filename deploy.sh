echo "Desplegando la aplicación Flask..."

echo "Creando el entorno virtual..."
python3 -m venv venv
echo "Activando el entorno virtual..."
source venv/bin/activate
echo "Instalando las dependencias..."
pip install -r requirements.txt

echo "Configurando el servicio systemd..."
sudo cp flask-app.service /etc/systemd/system/flask-app.service
echo "Habilitando el servicio..."
sudo systemctl enable flask-app.service
echo "Iniciando el servicio..."
sudo systemctl start flask-app.service
echo "Verificando el estado del servicio..."
sudo systemctl status flask-app.service

echo "Configurando NGINX..."
sudo cp flask-app.conf /etc/nginx/conf.d/flask-app.conf
echo "Reiniciando NGINX..."
sudo systemctl restart nginx


echo "Reiniciando los Demonios..."
sudo systemctl daemon-reload
echo "Verificando la configuración de NGINX..."
sudo nginx -t
echo "Verificando el estado de NGINX..."
sudo systemctl status nginx

echo "Despliegue completado. La aplicación Flask está corriendo en el puerto 5000."
echo "Puedes acceder a la aplicación en http://localhost:5000"

echo "Comprueba el despliegue con NGINX en http://localhost:80"
echo "Para ver los logs de la aplicación, usa el comando: journalctl -u flask-app.service -f"

echo "Para detener el servicio, usa el comando: sudo systemctl stop flask-app.service"
echo "Para reiniciar el servicio, usa el comando: sudo systemctl restart flask-app.service"
echo "Para ver el estado del servicio, usa el comando: sudo systemctl status flask-app.service"
echo "Para ver los logs de NGINX, usa el comando: sudo tail -f /var/log/nginx/error.log"
echo "Para ver los logs de la aplicación, usa el comando: journalctl -u flask-app.service -f"