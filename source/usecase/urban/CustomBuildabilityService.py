from adapter.urban.CustomBuildabilityRepository import CustomBuildabilityRepository
from entity.urban.Block import Block
from entity.geo.Geometry import Geometry
from usecase.core.LogService import LogService
from entity.urban.CustomBuildability import CustomBuildability
from adapter.geo.GisLibrary import GisLibrary

class CustomBuildabilityService:

    def __init__(self,
                 custom_buildability_repository:CustomBuildabilityRepository) -> None:
        self.__custom_buildability_repository = custom_buildability_repository

    def find_by_block(self, block:Block)->list[CustomBuildability]:
        return self.__custom_buildability_repository.find_by_block(block)