from pandas import Series
from entity.urban.Restriction import Restriction
from entity.urban.Block import Block
from entity.urban.Restriction import Restriction
import geopandas

from adapter.urban.RestrictionSourceRepository import RestrictionSourceRepository

class RestrictionFileRepository(RestrictionSourceRepository):

    def __init__(self, prop) -> None:
        self.__prop = prop
    
    def find_all(self) -> any:
        return geopandas.read_file(self.__resolve_path(), layer=self.__prop['layer'])

    def get_geometry_attribute_name(self) -> str:
        return "geometry"

    def __resolve_path(self) -> str: 
        return self.__threadService.get('path')

