from pandas import Series
from entity.urban.ArchaeologicalRisk import ArchaeologicalRisk
from entity.urban.Block import Block
from entity.urban.ArchaeologicalRisk import ArchaeologicalRisk
import geopandas

from adapter.urban.ArchaeologicalRiskSourceRepository import ArchaeologicalRiskSourceRepository

class ArchaeologicalRiskFileRepository(ArchaeologicalRiskSourceRepository):

    def __init__(self, prop) -> None:
        self.__prop = prop
    
    def find_all(self) -> any:
        return geopandas.read_file(self.__resolve_path(), layer=self.__prop['layer'])

    def get_geometry_attribute_name(self) -> str:
        return "geometry"

    def __resolve_path(self) -> str: 
        return self.__threadService.get('path')

