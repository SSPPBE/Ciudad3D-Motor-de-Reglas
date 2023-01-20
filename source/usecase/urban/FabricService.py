from usecase.core.DictUtil import DictUtil
from entity.urban.Block import Block
from adapter.urban.FabricRepository import FabricRepository
from entity.urban.Fabric import Fabric
from entity.geo.Geometry import Geometry
from adapter.geo.GisLibrary import GisLibrary
from entity.urban.Lot import Lot
from entity.urban.Consolidation import Consolidation

class FabricService:

    def __init__(self, 
                fabric_repository:FabricRepository,
                gis_library:GisLibrary,
                dict_util:DictUtil,
                prop:dict
                ) -> None:
        self.__fabric_repository = fabric_repository
        self.__gis_library = gis_library
        self.__dict_util = dict_util
        self.__prop = prop

    def find_by_block(self, block:Block) -> list[Fabric]:
        return self.__fabric_repository.find_by_block(block)

    def build_consolidated(self, block:Block):
        
        buffer = self.__prop['buffer']
        lo_with_buffer = self.__gis_library.buffer(block.get_geometry('official_line'), buffer)
        if (lo_with_buffer):
            for lot in block.get_lots():

                if (len(lot.get_heights()) > 0 and len(lot.get_fabrics()) > 0):

                    dissolve = self.__find_fabric(lot)
                    max_height = 0
                    max_height_in_lo = 0

                    for fabric in lot.get_fabrics():
                        if (fabric.get_height() >= max_height_in_lo):
                            max_height = fabric.get_height()
                            intersects = self.__gis_library.intersects(lo_with_buffer, fabric)
                            if (intersects and fabric.get_height() > max_height_in_lo):
                                max_height_in_lo = fabric.get_height()
                    if (lot.get_heights()[0] is not None):
                        type_consolidated, consolidated, percentage = self.__find_type(max_height_in_lo, lot.get_heights()[0])
                        if (dissolve is not None):
                            consolidate = Consolidation()
                            consolidate.add_value(dissolve.get_value())
                            consolidate.set_consolidated(consolidated)
                            consolidate.set_percentage(percentage)
                            consolidate.set_type_consolidated(type_consolidated)
                            consolidate.set_max_height(max_height_in_lo)
                            lot.set_consolidation(consolidate)

    def __find_type(self, fabric_height, lot_height):
        percentage = fabric_height / lot_height * 100
        it = self.__dict_util.find_in_range(self.__prop['ranges'], percentage)
        if (it):
            return (it['type'], 'consolidated' in it and it['consolidated'], percentage)
        return None

    def __find_fabric(self, lot:Lot):

        ls = [Fabric]
        filter = lot.get_build_types()[0].get_consolidate_filter()
        if (filter is not None):
            for fabric in lot.get_fabrics():
                if (fabric.get_height() > filter):
                    ls.append(fabric)
        else:
            ls = lot.get_fabrics()

        return self.__gis_library.dissolve(ls)

