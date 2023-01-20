from adapter.urban.ArchaeologicalRiskRepository import ArchaeologicalRiskRepository
from entity.urban.ArchaeologicalRisk import ArchaeologicalRisk

class ArchaeologicalRiskService:

    def __init__(self,
                 archaeological_risk_repository:ArchaeologicalRiskRepository) -> None:
        self.__archaeological_risk_repository = archaeological_risk_repository

    def find_all(self)->list[ArchaeologicalRisk]:
        return self.__archaeological_risk_repository.find_all()