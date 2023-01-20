from pandas import Series
from entity.urban.Lot import Lot
from entity.urban.Block import Block
from entity.urban.Lot import Lot
import geopandas

class LotSourceRepository:

    def find_by_block(self, block:Block) -> any:
        pass

    def get_geometry_attribute_name(self) -> str:
        pass

    def find_by_blocks(self, blocks:list[Block]) -> any:
        pass
