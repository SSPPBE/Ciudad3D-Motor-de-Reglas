from numpy import number
from entity.geo.Geometry import Geometry

class CustomLotLine(Geometry):
    
    def __init__(self) -> None:
        super().__init__()
        from entity.urban.Lot import Lot
        self.set_descriptor("custom_lot_line")
        self.__lot:Lot = None

    def get_lot(self): 
        return self.__lot

    def set_lot(self, value):
        self.__lot = value

    def get_type_custom_line(self) -> str: 
        return self.__type_custom_line

    def set_type_custom_line(self, value: str):
        self.__type_custom_line = value
