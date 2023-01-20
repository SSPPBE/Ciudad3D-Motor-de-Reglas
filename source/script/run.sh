# Archivo Run de referencia

# Para entorno de desarrollo descomentar, usar runserver y comentar lo demás
# cd /opt/asi-0280-algoritmo-ciudad3d-backend/source/app
# python3.9 -W ignore manage.py runserver 0.0.0.0:8080 --noreload

# Para entorno de QA descomentar y comentar lo demás
# sudo su -
# cd /opt/asi-0280-algoritmo-ciudad3d-backend/source/app
# gunicorn -c gunicorn_config.py --access-logfile=/var/log/gunicorn-access.log --error-logfile=/var/log/gunicorn-error.log --log-level 'debug'


# Para entorno de Producción descomentar y comentar lo demás
sudo su -
cd /opt/asi-0280-algoritmo-ciudad3d-backend/source/app
gunicorn -c gunicorn_config.py
