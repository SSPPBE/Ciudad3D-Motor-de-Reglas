class Projection:
    """
    Represent Coordinate Reference System (CRS) information 

    Attributes:
    ----------

        id (str): Projection id
        
        value (str): It's CRS information
            Example: 

                An authority string:
                    'epsg:4326'

                PROJ4 keyword arguments for parameters:
                    +proj=tmerc +lat_0=-34.629269 +lon_0=-58.4633 +k=0.9999980000000001 +x_0=100000 +y_0=100000 
                    +ellps=intl +units=m +no_defs

                CRS WKT String
                    PROJCS["GKBA",GEOGCS["International 1909 (Hayford)",DATUM["CAI",SPHEROID["intl",6378388,297]],
                    PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],
                    PARAMETER["latitude_of_origin",-34.629269],PARAMETER["central_meridian",-58.463300],
                    PARAMETER["scale_factor",0.999998],PARAMETER["false_easting",100000],PARAMETER["false_northing",100000],
                    UNIT["Meter",1]]
    
    """

    
    def __init__(self) -> None:
        self.__data = None
        pass

    def get_id(self) -> str :
        return self.__id

    def set_id(self, id: str):
        self.__id = id

    def get_value(self) -> str: 
        return self.__value

    def set_value(self, value:str):
        self.__value = value

    def get_data(self): 
        return self.__data

    def set_data(self, data):
        self.__data = data
