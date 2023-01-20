from pandas import Series
from entity.urban.Block import Block
from entity.urban.Block import Block
from entity.urban.Lot import Lot
import geopandas

class BlockSourceRepository:

    def find_by_blocks_sections(self, blocks:list[str], sections:list[str]) -> any:
        pass

    def find_all(self) -> any:
        pass

    def find_ae26(self, block:Block) -> any:
        pass

    def get_geometry_attribute_name(self) -> str:
        pass
