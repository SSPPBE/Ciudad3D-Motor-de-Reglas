from numpy import number
from entity.geo.Geometry import Geometry

class CustomLine(Geometry):
    
    def __init__(self) -> None:
        super().__init__()
        from entity.urban.Block import Block
        self.set_descriptor("custom_line")
        self.__block:Block

    def get_block(self): 
        return self.__block

    def set_block(self, value):
        self.__block = value

    def get_type_custom_line(self) -> str: 
        return self.__type_custom_line

    def set_type_custom_line(self, value: str):
        self.__type_custom_line = value
