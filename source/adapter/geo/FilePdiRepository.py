from usecase.core.ConfigurationService import ConfigurationService
from adapter.geo.PdiRepository import PdiRepository
import geopandas as gpd

class FilePdiRepository(PdiRepository):

    def __init__(self, configurationService:ConfigurationService, file_path):
        self.configurationService = configurationService
        self.__prop = configurationService.get_prop()
        self.__conf = configurationService.get_conf()
        self.__file_path = file_path

    def get_block_geometry_name(self) -> str:
        return "geometry"

    def get_restriction_frame(self) -> any:
        return gpd.read_file(self.__file_path, layer=self.__prop['geometry.restriction.layer'])

    def get_lot_frame(self) -> any:
        return gpd.read_file(self.__file_path, layer=self.__prop['geometry.lot.layer'])

    def get_block_frame(self) -> any:
        return gpd.read_file(self.__file_path, layer=self.__prop['geometry.block.layer'], )

    def get_real_frame(self) -> any:
        return gpd.read_file(self.__file_path, layer=self.__prop['geometry.real.layer'])

    def get_crs(self, crs) -> any:
        return crs

