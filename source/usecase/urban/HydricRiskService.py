from adapter.urban.HydricRiskRepository import HydricRiskRepository
from entity.urban.HydricRisk import HydricRisk

class HydricRiskService:

    def __init__(self,
                 hydric_risk_repository:HydricRiskRepository) -> None:
        self.__hydric_risk_repository = hydric_risk_repository

    def find_all(self)->list[HydricRisk]:
        return self.__hydric_risk_repository.find_all()