import shutil
import subprocess
from collections import defaultdict

from numpy import insert
from adapter.core.DbConnector import DbConnector
from entity.urban.Block import Block
from entity.geo.Geometry import Geometry
from adapter.geo.GisLibrary import GisLibrary
from usecase.output.FileService import FileService
import paramiko
import os

class Ciudad3dService:

    def __init__(self, 
                gis_library:GisLibrary,
                file_service:FileService,
                db_connector:DbConnector,
                prop:dict
                ) -> None:
        self.__gis_library = gis_library
        self.__file_service = file_service
        self.__prop = prop
        self.__db_connector = db_connector

    def save(self, files:dict) -> dict:

        # files = self.__file_service.save(export, self.__prop['save']['geojson'], "GeoJSON")    
        # sftp, transport = self.__start_sftp()

        default_param = self.__prop['tippecanoe']['default']

        for file in files:
            simple_name = file['simple_name'] + "." + "mbtiles"
            path = file['folder'] + "/" + simple_name
            layer_param = self.__prop['tippecanoe'][file['simple_name']]
            param = ["tippecanoe", "-o", path]
            if (default_param):
                param.extend(default_param)
            if (layer_param):
                param.extend(layer_param)
            param.extend([file['path']])
            subprocess.run(param)
            file['path'] = path

        return files
            # self.__copy(sftp, path, simple_name)

        # self.__stop_sftp(sftp, transport)

    def save_cd3_tiles_nfs(self, files:dict) -> dict:

        root = os.getenv(self.__prop['nfs']['root']) 
        relative = os.getenv(self.__prop['nfs']['relative']) 
        for file in files:
            path = root + "/" + relative + "/"+ file["simple_name"] + "." + "mbtiles"
            origin = os.path.abspath(file['path'])
            shutil.copyfile(origin, path)
            
        return files

           

    def save_data(self, exports:dict) -> dict:

        for key, values in exports.items():
            self.__db_connector.clear_all(key)
            self.__db_connector.insert(key, values)
        
        self.__db_connector.execute("select algoritmo.actualizarciudad3d_2()")
        # self.__db_connector.execute(func.algoritmo.actualizarciudad3d_2())
        
    def __start_sftp(self):
        host = os.getenv(self.__prop['copy']['host']) 
        port = int(os.getenv(self.__prop['copy']['port'])) 
        password = os.getenv(self.__prop['copy']['pass']) 
        username = os.getenv(self.__prop['copy']['user']) 
        transport = paramiko.Transport((host, port))
        transport.connect(username = username, password = password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp, transport

    def __stop_sftp(self, sftp, transport):
        sftp.close()
        transport.close()

    def __copy(self, sftp, local_path, name):
        remote_path =  os.getenv(self.__prop['copy']['remote']) + "/" + name #"user"
        print(remote_path)
        sftp.put(local_path, remote_path)


        
