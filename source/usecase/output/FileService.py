from collections import defaultdict
from distutils.log import info
from logging import root
from zipfile import ZipFile
from platformdirs import os
from entity.urban.Block import Block
from entity.geo.Geometry import Geometry

import uuid

from adapter.geo.GisLibrary import GisLibrary

class FileService:

    def __init__(self, 
                gis_library:GisLibrary,
                prop:dict
                ) -> None:
        self.__gis_library = gis_library
        self.__prop = prop


    def save(self, layers:dict, export_info:dict) -> dict:
        #TODO: Change dxf params into export info

        result = []
        group = export_info["group"]
        infopath = self.__get_info_path(export_info)

        if group:
            result.append(infopath)

        zip_file = None

        zip = export_info['zip'] if 'zip' in export_info else False
        only_geom = export_info['only_geom'] if 'only_geom' in export_info else False

        if zip:
            path_zip = './' + infopath['folder'] + "/" + infopath['root_name'] + ".zip"
            zip_file = ZipFile(path_zip, 'w')
            infopath["path"] = path_zip
            result.append(infopath)

        for layer_name, infos in layers.items():
            print(layer_name)
            if not group:
                infopath = self.__get_info_path(export_info, infopath['root_name'], layer_name)
                result.append(infopath)

            if only_geom:
                self.__gis_library.export_geos(infos, infopath['path'], export_info['driver'], export_info["geo_attribute"], export_info["projection"], layer_name if group else None)
            else:
                self.__gis_library.export_infos(infos, infopath['path'], export_info['driver'], export_info["geo_attribute"], export_info["projection"], layer_name if group else None)

            if zip:
                zip_file.write(infopath['path'], infopath["simple_name"] + "." + export_info['extension'])

        if zip:
            zip_file.close()

        return result            

    def __get_info_path(self, export_info:dict, root_name:str = None, name:str = None) -> dict:

        if (root_name == None):
            output_name = self.__prop['output']['name']
            output_random = self.__prop['output']['random']

            root_name = ''
            if (output_name != None):
                root_name = output_name
            else:
                if (output_random):
                    root_name = str(uuid.uuid4())

        folder_path = os.getenv(self.__prop['output']['folder_root']) + "/" + os.getenv(self.__prop['output']['folder_relative'])
        output_name = self.__prop['output']['name']
        output_random = self.__prop['output']['random']
        # output_folder = self.__prop['output']['folder']
        output_folder = os.path.abspath(folder_path)
        output_context = self.__prop['output']['context']

        root_name = root_name
        simple_name = name if name is not None else ""
        full_name = root_name if name is None else simple_name
        last = "/" + full_name + "." + export_info["extension"]
        path = output_folder + last
        url = "/" + output_context + last

        print(os.path.abspath(path))
        if os.path.exists(path):
            os.remove(path)

        result = {
            'folder': folder_path,
            'simple_name': simple_name,
            'root_name':root_name,
            'path':path,
            'url':url
        }       

        return result
