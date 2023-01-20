from entity.geo.Geometry import Geometry

class ArchaeologicalRisk(Geometry):
    def __init__(self) -> None:
        super().__init__()
        self.set_descriptor("archaeological_risk")

    def get_description(self) -> str:
        return self.__description

    def set_description(self, value:str):
        self.__description = value
