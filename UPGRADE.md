- Implementación de Gunicorn

1. Seguir el paso 1 después de instalado la primera vez.

1. Gunicorn no puede ejecutarse sin ser usuario root, por lo que se debe ejecutar el siguiente comando:

       $ sudo su -

1. Moverse a:

        $ cd /opt/asi-0280-algoritmo-ciudad3d-backend/source/app

1. Verificamos que estamos en el siguiente path, tal como se indica en el paso previo:

       $ /opt/asi-0280-algoritmo-ciudad3d-backend/source/app

1. Ejecutar el siguiente comando para activar Gunicorn como servidor:

       $ gunicorn -c gunicorn_config.py --access-logfile=/var/log/gunicorn-access.log --error-logfile=/var/log/gunicorn-error.log --log-file=/var/log/gunicorn-output.log --timeout 700000

- Fix first assessment

**Después de instalado la primera vez, solo hace falta**:

1.  Activar el entorno virtual

        $ source /opt/asi-0280-algoritmo-ciudad3d-backend/source/env/bin/activate

1. Moverse a:

        $ cd /opt/asi-0280-algoritmo-ciudad3d-backend/source/app

1.  Ejecutar para entorno de desarrollo:

        $ sudo python3.9 -W ignore manage.py runserver 0.0.0.0:8080 --noreload

**Primera vez**:

1. Ejecutar:

        $ cd opt

1. Ejecutar:

        $ sudo git clone https://repositorio-asi.buenosaires.gob.ar/usuarioqa/asi-0280-algoritmo-ciudad3d-backend.git

1. Copiar el archivo de ejemplo de variables de entorno para crear el .env

        $ sudo cp asi-0280-algoritmo-ciudad3d-backend/source/app/_.env asi-0280-algoritmo-ciudad3d-backend/source/app/.env

1. Actualizar el valor de las variables del archivo .env

        $ sudo nano asi-0280-algoritmo-ciudad3d-backend/source/app/.env

    El valor de API_KEY debe ser el mismo que el usado en EPOK.

    El endpoint "/download" ejecutado mediante el método HTTP POST será invocado por la aplicación EPOK usando un token API_KEY para garantizar que la petición sea ejecutada si y solo si entre estos servicios. A su vez la solicitud de ejecución del servicio EPOK lo hará la aplicación de frontend la cual también será mediante token por lo que se garantiza un marco de seguridad entre: el frontend, EPOK y motor de reglas siendo este último un servicio interno sin exposición directa a los usuarios finales.

    **Nota: en el header esa variable se llama "apikey"**

1. Ejecutar el archivo:

      $ sudo /opt/asi-0280-algoritmo-ciudad3d-backend/source/script/install.sh

1. Crear el entorno virtual

        $ sudo python3 -m venv /opt/asi-0280-algoritmo-ciudad3d-backend/source/env

1. Activar el entorno virtual

        $ source /opt/asi-0280-algoritmo-ciudad3d-backend/source/env/bin/activate

1. Instalar dependencias:

        $ sudo pip3 install -r /opt/asi-0280-algoritmo-ciudad3d-backend/source/requirements.txt

1. Moverse a:

        $ cd /opt/asi-0280-algoritmo-ciudad3d-backend/source/app

1. Ejecutar para entorno de desarrollo:

        $ sudo python3.9 -W ignore manage.py runserver 0.0.0.0:8080 --noreload

- 1.0.0-RC7
Se agregan las variables de entorno "CONFIGURATION_FOLDER" y "API_KEY"

CONFIGURATION_FOLDER= ./app
API_KEY= 88d346b3-00ed-4793-8bb2-179e4ff96b81



- 1.0.0-RC4
Se elimina la dependencia a tkinter

- 1.0.0-RC3
Se agrega el endpoint /health para proveer el HealthCheck que requiere ASI

