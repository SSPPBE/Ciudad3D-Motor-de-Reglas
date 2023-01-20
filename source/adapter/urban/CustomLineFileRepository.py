from entity.urban.Block import Block
from entity.urban.CustomLine import CustomLine
import geopandas

from adapter.urban.CustomLineSourceRepository import CustomLineSourceRepository

class CustomLineFileRepository(CustomLineSourceRepository):

    def __init__(self, prop) -> None:
        self.__prop = prop
    
    def find_by_block(self, block:Block) -> any:
        return geopandas.read_file(self.__resolve_path(), layer=self.__prop['layer'])

    def get_geometry_attribute_name(self) -> str:
        return "geometry"

    def __resolve_path(self) -> str: 
        return self.__threadService.get('path')

