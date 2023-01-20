from pyproj import CRS
from shapely.geometry import Polygon
import geopandas as gpd
import matplotlib.pyplot as plt

def test_crs():

    lat_point_list = [50.854457, 52.518172, 50.072651, 48.853033, 50.854457]
    lon_point_list = [4.377184, 13.407759, 14.435935, 2.349553, 4.377184]

    polygon_geom = Polygon(zip(lon_point_list, lat_point_list))

    crs = CRS.from_user_input("+proj=tmerc +lat_0=-34.629269 +lon_0=-58.4633 +k=0.9999980000000001 +x_0=100000 +y_0=100000 +ellps=intl +units=m +no_defs")
 #   crs = CRS.from_user_input('epsg:4326')

    p1 = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])     
    p1.inte
    print(p1.geometry)
    print(p1.head())
    p1.plot(figsize=(6, 6))
    p1
#    plt.show()

#    polygon.to_file(filename='temp/test_crs/polygon.geojson', driver='GeoJSON')
    p1.to_file(filename='./polygon.shp', driver="ESRI Shapefile")

    
#crs_utm = CRS.from_user_input(26915)
if __name__ == "__main__":
    test_crs()
    print("Everything passed")