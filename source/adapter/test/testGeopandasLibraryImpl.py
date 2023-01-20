import unittest
import json
from adapter.gcba.geo.GeopandasLibraryImpl import GeopandasLibraryImpl
from entity.gcba.geo.Projection import Projection

class TestGeopandasLibraryImpl(unittest.TestCase):

    def test_set_projection_success(self):
        geopandasLibraryImpl = GeopandasLibraryImpl()

        projection = Projection()
        projection.set_id("97433")
        projection.set_value("+proj=tmerc +lat_0=-34.629269 +lon_0=-58.4633 +k=0.9999980000000001 +x_0=100000 +y_0=100000 +ellps=intl +units=m +no_defs")        

        data = geopandasLibraryImpl.build()
        geopandasLibraryImpl.set_projection(data, projection)

    def test_set_projection_fail_format_value(self):
        geopandasLibraryImpl = GeopandasLibraryImpl()

        projection = Projection()
        projection.set_id("97433")
        # Bad format value
        projection.set_value("oj=tmerc +lat_0=-34.629269 +lon_0=-58.4633 +k=0.9999980000000001 +x_0=100000 +y_0=100000 +ellps=intl +units=m +no_defs")        

        data = geopandasLibraryImpl.build()
        try:
            geopandasLibraryImpl.set_projection(data, projection)
        except:
            assert True
        else:
            assert False

    #TODO test_load_data_from_WKS
    #TODO test_load_data_from_SHAPE

if __name__ == '__main__':
    t = unittest.TestLoader().loadTestsFromTestCase(TestGeopandasLibraryImpl)
    unittest.TextTestRunner().run(t)