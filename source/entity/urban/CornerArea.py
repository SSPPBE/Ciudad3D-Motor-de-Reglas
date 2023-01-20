from numpy import number
from entity.geo.Geometry import Geometry
from entity.urban.Extension import Extension

class CornerArea(Geometry):
    def __init__(self) -> None:
        super().__init__()
        from entity.urban.Block import Block
        self.set_descriptor("corner_area")
        self.__block: Block
        self.__extension = None

    def get_block(self) -> any: 
        return self.__block

    def set_block(self, value: any):
        self.__block = value

    def get_extension(self) -> Extension: 
        return self.__extension

    def set_extension(self, value: Extension):
        self.__extension = value