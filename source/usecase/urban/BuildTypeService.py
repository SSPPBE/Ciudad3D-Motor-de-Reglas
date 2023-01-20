import string
from entity.urban.BuildType import BuildType
from entity.urban.BuildInfo import BuildInfo
from entity.urban.Block import Block


class BuildTypeService:

    def __init__(self,
                 prop:dict) -> None:
        self.__prop = prop
        self.__repo = {}

    def __get_in_repo(self, build_type_def, build_info) -> BuildType:
        if (build_type_def['code'] in self.__repo):
            return self.__repo[build_type_def['code']]
            # return copy.deepcopy(self.__repo[build_type_def['code']])

        components = self.__prop['component']
        build_type = BuildType()
        comps = []
        if build_type_def['components'] is not None:
            for component in build_type_def['components']:
                for key, value in component.items():
                    if (value is None):
                        value = {}
                    comps.append({ **components[key], **value})
                    if ('no_corner_area' in components[key]):
                        build_type.set_no_corner_area(True)
                    
        build_type.set_components(comps)
        build_type.set_code(build_type_def['code'])
        build_type.set_build_info(build_info)
        if ('accept_rivolta' in build_type_def):
            build_type.set_accept_rivolta(build_type_def['accept_rivolta'])
        if ('consolidate_filter' in build_type_def):
            build_type.set_consolidate_filter(build_type_def['consolidate_filter'])

        if 'height' in build_type_def:
            build_type.set_height(build_type_def['height'])
        self.__repo[build_type_def['code']] = build_type

        return build_type
        # return copy.deepcopy(build_type)

    def find_by_build_info(self, build_info:BuildInfo)->BuildType:

        build_type_defs = self.__prop['build_type']

        for build_type_def in build_type_defs:
            definition:dict = None
            if (build_info.get_uni_edif() is not None and 'uni_edif' in build_type_def and build_type_def['uni_edif'] == build_info.get_uni_edif()) :
                definition = build_type_def
            elif (build_info.get_dist_esp() is not None and 'dist_esp' in build_type_def and build_type_def['dist_esp'] == build_info.get_dist_esp()) :
                if (build_info.get_zone_1() is None):
                    definition = build_type_def
                elif (build_info.get_zone_1() is not None and 'zona_1' in build_type_def and build_info.get_zone_1() == build_type_def['zona_1']) :
                    definition = build_type_def
            if (definition is not None):
                return self.__get_in_repo(definition, build_info)

        return None

    def find_by_code(self, code):
        build_type_defs = self.__prop['build_type']
        for build_type_def in build_type_defs:
            if ('code2' in build_type_def and build_type_def['code2'] == code):
                info = BuildInfo()
                info.set_uni_edif(build_type_def['uni_edif'])
                return info
        return None


    def has_geometry(self, block:Block, geometry_name:string) -> bool:
        
        for lot in block.get_lots():
            for build in lot.get_build_types():
                for component in build.get_components():
                    if ('substract' in component):
                        for key, value in component['substract'].items():
                            if ('geometry' in value):
                                if (value['geometry'] == geometry_name):
                                    return True
        return False

    def has_build_type(self, block:Block) -> bool:
        
        for lot in block.get_lots():
            if (lot.get_build_types()):
                return True
        return False
