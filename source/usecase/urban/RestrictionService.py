from adapter.urban.RestrictionRepository import RestrictionRepository
from entity.urban.Block import Block
from entity.geo.Geometry import Geometry
from usecase.core.LogService import LogService
from entity.urban.Restriction import Restriction
from adapter.geo.GisLibrary import GisLibrary

class RestrictionService:

    def __init__(self,
                 restriction_repository:RestrictionRepository,
                 gis_library:GisLibrary, 
                 log_service:LogService, 
                 prop:dict) -> None:
        self.__restriction_repository = restriction_repository
        self.__gis_library = gis_library
        self.__log_service = log_service
        self.__prop = prop

    def find_all(self)->list[Restriction]:
        list = self.__restriction_repository.find_all()
        return self.__validate_by_filter(list)

    def validate(self, blocks:list[Block]) -> list[Restriction]:

        for block in blocks:
            valid = False
            if (block.get_restrictions().__len__() == 1):
                for restriction in block.get_restrictions():
                    if (self.__gis_library.is_gis_type(restriction, self.__prop['valid_gis_type'])):
                        valid = True
                    else:
                        self.__log_service.add({'message':'discard restriction', 'cause':'more than 1 restriction to block', 'block':block.get_name()})
            else:
                if (block.get_restrictions().__len__() > 1):
                    self.__log_service.add({'message':'discard restriction', 'cause':'more than 1 restriction to block', 'block':block.get_name()})

            if (not valid):
                values = [y for x in block.get_restrictions() for y in x.get_values()]
                block.add_geometry(Geometry(values, 'restriction_discard'))
                block.set_restrictions([])

    def __validate_by_filter(self, list:list[Restriction]) -> list[Restriction]:
        result = []

        if (list):

            valid_type = self.__prop['valid_type']
            valid_obs =  self.__prop['valid_obs']

            for it in list:
                if (it.get_type_restriction() in valid_type):
                    if (it.get_observation() in valid_obs):
                        result.append(it)
                    else:
                        self.__log_service.add({'message':'discard restriction', 'cause':'observation not valid', 'observation':it.get_observation(), 'order':it.get_order()})
                else:
                    self.__log_service.add({'message':'discard restriction', 'cause':'type not valid', 'type_restriction':it.get_type_restriction(), 'order':it.get_order()})

        return result

    def build_with_restrictions(self, block:Block, origin:Geometry, geometry_name:str):
        
        found = self.find_with_restrictions(block, origin)
        block.add_geometry(found, geometry_name)        

    def find_with_restrictions(self, block:Block, origin:Geometry):

        scalar_x = self.__prop['scalar-x']
        scalar_y = self.__prop['scalar-y']

        if (origin is None):
            return None
            
        found = Geometry(origin.get_values())
        if (block.get_restrictions()):
            restriction = block.get_restrictions()[0]
            restriction_scaled = self.__gis_library.scale(restriction, scalar_x, scalar_y)
            splits = self.__gis_library.split(origin, restriction_scaled)     
            max_value = 0           
            for split in splits:
                area = self.__gis_library.get_area(split)
                if (area > max_value):
                    found = self.__gis_library.cast(split, 'MultiPolygon')
                    max_value = area

        return found        

    