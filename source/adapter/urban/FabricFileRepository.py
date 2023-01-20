from pandas import Series
from entity.urban.Fabric import Fabric
from entity.urban.Block import Block
from entity.urban.Lot import Lot
import geopandas

from adapter.urban.FabricSourceRepository import FabricSourceRepository

class FabricFileRepository(FabricSourceRepository):

    def __init__(self, prop) -> None:
        self.__prop = prop
    
    def find_by_block(self, block:Block) -> any:
        return geopandas.read_file(self.__resolve_path(), layer=self.__prop['layer'])

    def get_geometry_attribute_name(self) -> str:
        return "geometry"

    def __resolve_path(self) -> str: 
        return self.__threadService.get('path')

