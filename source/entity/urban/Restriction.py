from entity.geo.Geometry import Geometry

class Restriction(Geometry):
    def __init__(self) -> None:
        super().__init__()
        from entity.urban.Block import Block
        self.set_descriptor("restriction")
        self.__block: Block

    def get_block(self):  
        return self.__block 

    def set_block(self, value):
        self.__block = value

    def get_type_restriction(self) -> str:
        return self.__type_restriction

    def set_type_restriction(self, value:str):
        self.__type_restriction = value

    def get_order(self) -> str:
        return self.__order

    def set_order(self, value:str):
        self.__order = value

    def get_observation(self) -> str:
        return self.__observation

    def set_observation(self, value:str):
        self.__observation = value
