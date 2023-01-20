from collections import defaultdict
from adapter.urban.CustomLineRepository import CustomLineRepository
from entity.urban.Block import Block
from entity.geo.Geometry import Geometry
from usecase.core.LogService import LogService
from entity.urban.CustomLine import CustomLine
from adapter.geo.GisLibrary import GisLibrary

class CustomLineService:

    def __init__(self,
                 custom_line_repository:CustomLineRepository,
                 gis_library:GisLibrary) -> None:
        self.__custom_line_repository = custom_line_repository
        self.__gis_library = gis_library

    def find_by_block(self, block:Block)->list[CustomLine]:
        result = []
        list_it = self.__custom_line_repository.find_by_block(block)
        line = defaultdict(list)
        for it in list_it:
            line[it.get_type_custom_line()].append(it)

        for code, list_line in line.items():
            it = CustomLine()
            it.set_type_custom_line(code)
            merge = self.__gis_library.merge(list_line)
            if (merge):
                it.set_values(merge.get_values())
                result.append(it)

        return result