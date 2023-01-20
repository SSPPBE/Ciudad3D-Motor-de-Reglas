from collections import defaultdict
import traceback
from typing import Dict
from xmlrpc.client import Boolean, boolean
from shapely.geometry.geo import mapping
from adapter.geo.DbPdiRepository import DbPdiRepository
from adapter.geo.PdiRepository import PdiRepository
from adapter.geo.GisLibrary import GisLibrary
from usecase.core.LogService import LogService
from usecase.output.Ciudad3dService import Ciudad3dService
from usecase.output.FileService import FileService
from entity.urban.ArchaeologicalRisk import ArchaeologicalRisk
from entity.urban.HydricRisk import HydricRisk
from entity.urban.Restriction import Restriction
from usecase.urban.HydricRiskService import HydricRiskService
from usecase.urban.ArchaeologicalRiskService import ArchaeologicalRiskService
from usecase.urban.RestrictionService import RestrictionService
from usecase.urban.BlockService import BlockService
from usecase.core.ThreadService import ThreadService
from usecase.core.ConfigurationService import ConfigurationService
from adapter.geo.FilePdiRepository import FilePdiRepository
import ezdxf
from ezdxf.addons import Importer
import os
from ezdxf import colors, bbox

class ProcessService():

    def __init__(self, 
                 configurationService:ConfigurationService, 
                 restriction_service:RestrictionService,
                 thread_service:ThreadService,
                 log_service:LogService,
                 block_service:BlockService,
                 gis_library:GisLibrary,
                 ciudad3d_service:Ciudad3dService,
                 file_service:FileService,                 
                 archaelogical_risk_service:ArchaeologicalRiskService,
                 hydric_risk_service:HydricRiskService,
                 prop:dict):
        self.__prop = prop
        self.__restriction_service = restriction_service
        self.__thread_service = thread_service
        self.__log_service = log_service
        self.__block_service = block_service
        self.__hydric_risk_service = hydric_risk_service
        self.__archaelogical_risk_service = archaelogical_risk_service
        self.__ciudad3d_service = ciudad3d_service
        self.__file_service = file_service   
        self.__gis_library = gis_library
        

    process_result = []

    def execute(self, blocks:list[str], sections:list[str], full:bool = False, output:str = "basic") -> dict:

        result = {}

        self.__thread_service.set("connector", "db")
        self.__thread_service.set("log", [])

        block_items = []
        if (blocks or sections):
            block_items = self.__block_service.find_by_blocks_sections(blocks, sections)
        if (full):
            block_items = self.__block_service.find_all()

        if block_items:

            restrictions = self.__restriction_service.find_all()
            archeological_risks = self.__archaelogical_risk_service.find_all()
            hydric_risks = self.__hydric_risk_service.find_all()        

            self.__block_service.find_restrictions(block_items, restrictions)

            block_items = self.__block_service.run_algorythms(block_items)

            return self.__output(output, block_items, restrictions, archeological_risks, hydric_risks)
                

    def __output(self, output, block_items, restrictions, archeological_risks, hydric_risks) -> Dict:

        result = None
        if not block_items:
            return result

        output = self.__prop['output'][output]
        self.__set_projections()
        info = None

        try:
            for phase in output['phases']:

                transformation = phase['transformation'] if 'transformation' in phase else None
                phase_code = phase['code']

                if phase_code == 'export_basic':
                    info = defaultdict(list)
                    info = self.__block_service.export(info, block_items, transformation)
                    info = self.__export(info, transformation, archeological_risks, hydric_risks, restrictions)

                if phase_code == 'export_cd3_info':
                    info = defaultdict(list)
                    info = self.__block_service.export_data(info, block_items, transformation)

                elif phase_code == "export_cad":
                    info = defaultdict(list)
                    info = self.__block_service.export_cad(info, block_items, transformation)

                elif phase_code == "save_basic":

                    result = self.__file_service.save(info, phase)

                elif phase_code == "save_cd3_tiles":

                    result = self.__ciudad3d_service.save(result)

                elif phase_code == "save_cd3_tiles_nfs":

                    result = self.__ciudad3d_service.save_cd3_tiles_nfs(result)

                elif phase_code == "save_cd3_data":

                    self.__ciudad3d_service.save_data(info)

                elif phase_code == "save_dxf":
                    result = self.__save_dxf(result, block_items[0].get_name())

        except Exception:
            self.__log_service.add({'message':'ERROR OUTPUT', 'error':traceback.format_exc()})

        return result

    
    def merge(self, source, target):
        importer = Importer(source, target)
        # import all entities from source modelspace into target modelspace
        importer.import_modelspace()
        # import all required resources and dependencies
        importer.finalize()

    def assign_layer(self, doc, layer_name, layer_color):
        """
        Assign layer inside dxf target based on new layer (layername)
        Set active entity for dxf layer with equivalent layername
        """
        try:
            new_layer = doc.layers.new(layer_name)
        except ezdxf.DXFTableEntryError:
            print(f"layer '{layer_name}' already exist")
            return
        new_layer.dxf.color = layer_color
        for entity in doc.modelspace():
            entity.dxf.layer = layer_name        

    def __save_dxf(self, files, name):

        root = os.getenv(self.__prop['dxf']['root']) 
        relative = os.getenv(self.__prop['dxf']['relative']) 
        dir = root + "/" + relative + "/"
        target = ezdxf.new()

        for file in files:
            source = ezdxf.readfile(file['path'])
            importer = Importer(source, target)
            importer.import_modelspace()
            importer.finalize()
            self.assign_layer(source, file['simple_name'], colors.BLACK)
            self.merge(source, target)

        path = dir + name + '.dxf'
        target.saveas(path)
        result = {
            'folder': dir,
            'simple_name': name + '.dxf',
            'root_name':dir,
            'path':path
        }  
        return result

    def __export(self, layer, transformation, archeological_risks:list[ArchaeologicalRisk], 
                 hydric_risks:list[HydricRisk], restrictions:list[Restriction]):

        items = []

        for archeological_risk in archeological_risks:
            #cur_riesgo_arqueologico
            item = {}
            definition = {'name':'cur_riesgo_arqueologico', 'info':item}
            item['tipo'] = archeological_risk.get_description()
            item['geom'] = self.__gis_library.project(archeological_risk, transformation)
            items.append(definition)            

        for hydric_risk in hydric_risks:
            #cur_riesgo_hidrico
            item = {}
            definition = {'name':'cur_riesgo_hidrico', 'info':item}
            item['geom'] = self.__gis_library.project(hydric_risk, transformation)
            items.append(definition)            

        for restriction in restrictions:
            #cur_restricciones
            item = {}
            definition = {'name':'cur_restricciones', 'info':item}
            item['nro_ord'] = restriction.get_order()
            item['obs'] = restriction.get_observation()
            item['tipo'] = restriction.get_type_restriction()
            item['clase'] = ''
            item['geom'] = self.__gis_library.project(restriction, transformation)
            items.append(definition) 

        for definition in items:
            layer[definition['name']].append(definition['info'])   

        return layer      

    def __set_projections(self):

        for k, v in self.__prop['projection'].items():
            self.__gis_library.add_projection(k, v)       

        for k, v in self.__prop['transformation'].items():
            self.__gis_library.add_transformation(k, v['from'], v['to'])       
