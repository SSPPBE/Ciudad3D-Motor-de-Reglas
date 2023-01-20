from pandas import Series
from entity.urban.Fabric import Fabric
from entity.urban.Block import Block
from entity.urban.Lot import Lot
import geopandas

class FabricSourceRepository:

    def find_by_block(self, block:Block) -> any:
        pass

    def get_geometry_attribute_name(self) -> str:
        pass
