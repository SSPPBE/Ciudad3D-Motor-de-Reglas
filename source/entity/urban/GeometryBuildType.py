from numpy import number
from entity.geo.Geometry import Geometry

class GeometryBuildType(Geometry):
    
    def __init__(self) -> None:
        super().__init__()
        from entity.urban.BuildType import BuildType
        self.__build_type:BuildType = None

    def get_build_type(self): 
        return self.__build_type

    def set_build_type(self, value):
        self.__build_type = value