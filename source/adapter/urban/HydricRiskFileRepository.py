from pandas import Series
from entity.urban.HydricRisk import HydricRisk
from entity.urban.Block import Block
from entity.urban.HydricRisk import HydricRisk
import geopandas

from adapter.urban.HydricRiskSourceRepository import HydricRiskSourceRepository

class HydricRiskFileRepository(HydricRiskSourceRepository):

    def __init__(self, prop) -> None:
        self.__prop = prop
    
    def find_all(self) -> any:
        return geopandas.read_file(self.__resolve_path(), layer=self.__prop['layer'])

    def get_geometry_attribute_name(self) -> str:
        return "geometry"

    def __resolve_path(self) -> str: 
        return self.__threadService.get('path')

