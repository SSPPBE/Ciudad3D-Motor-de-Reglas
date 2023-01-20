from entity.geo.Geometry import Geometry

class HydricRisk(Geometry):
    def __init__(self) -> None:
        super().__init__()
        self.set_descriptor("hydric_risk")