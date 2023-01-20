- 1.0.0-RC8
    * Se han incluido los siguientes tickets
      * APPC3D-65 Descarga archivo 2d: Consolidar un solo dxf
      * APPC3D-60 Irregulares: Adaptar proceso de irregulares a particularizadas
      * APPC3D-63 Planificacion Ejecucion semanal: Cambiar metodo de planificacion utilizando libreria de python. ASI no acepta planificacion por Sistema Operativo.

    * Se acepta la incorporacion de una variable en el entorno de ambientes: CRON_JOB. Ejemplo: 0 12 * * 0 (Todos los domingos a las 12 hs)

    * Si no existen las carpetas MEDIA y TILES, las crea

    * [NOC #823668](https://noc-mesa.buenosaires.gob.ar/WorkOrder.do?woMode=viewWO&woID=823668) Fix first assessment P0815_VA01:
        * Vulnerabilidad 1. Implementación de Gunicorn:
            * Agregada librería al archivo requirements.txt
            * Actualizado en el upgrade.md los pasos a seguir para levantar el servidor
        * Vulnerabilidad 2. Desactivado modo de depuración.
        * Vulnerabilidad 3. Actualizada la versión de Django a 3.2.16
        * Vulnerabilidad 4. Actualizado el endpoint /health para que al recibir datos por body la aplicación arroje un error 400.

        Nota: La versión de Python es la 3.9

    * Agregado archivo de ejemplo de variables de entorno ._env

    * [APPCASENOC-418](https://asijira.buenosaires.gob.ar/browse/APPCASENOC-418) Corrección de lógica en cálculo de LFI y LIB

- 1.0.0-RC6
    * Se genera la documentacion Postman de las APIs
    * Se agregan las variables de entorno para guardar los Tiles y los archivos Media, con esta estructura
        Ejemplo:
        ROOT_FOLDER= /app/test/...
        MEDIA= tmp
        TILES= tiles

