from entity.urban.Block import Block
from entity.urban.CustomBuildability import CustomBuildability
import geopandas

from adapter.urban.CustomBuildabilitySourceRepository import CustomBuildabilitySourceRepository

class CustomBuildabilityFileRepository(CustomBuildabilitySourceRepository):

    def __init__(self, prop) -> None:
        self.__prop = prop
    
    def find_by_block(self, block:Block) -> any:
        return geopandas.read_file(self.__resolve_path(), layer=self.__prop['layer'])

    def get_geometry_attribute_name(self) -> str:
        return "geometry"

    def __resolve_path(self) -> str: 
        return self.__threadService.get('path')

