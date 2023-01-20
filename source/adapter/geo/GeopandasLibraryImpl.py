from typing import Dict

from pyproj.crs.crs import CRS
from entity.gcba.ErrorType import ErrorType
from entity.gcba.exception.ErrorException import ErrorException
from entity.gcba.geo.GeoData import GeoData
from entity.gcba.geo.Projection import Projection

class GeopandasLibraryImpl():

    def build(self):
        """
        Build new structure data in library \n
        This structure is use as a param in all gis methods \n
        Structure depends on implementation class
        """
        return GeoData()

    def set_projection(self, data:GeoData, projection:Projection):
        """
        Set Coordinate Reference System (CRS) information to be used in processing
        """
        if (projection.get_data() is None) :
            if (projection.get_value() is None):
                raise ErrorException(ErrorType.INTERNAL, "projection.invalid")
            crs = CRS.from_user_input(projection.get_value())
            projection.set_data(crs)
            data.set_projection(projection)
            
        return self

    
