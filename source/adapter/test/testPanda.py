import geopandas as gpd
import requests
from shapely.geometry import Polygon
from shapely.geometry import shape
import matplotlib.pyplot as plt

def test_sum():
    assert sum([1, 2, 3]) == 7, "Should be 6"


def test_feature():

    r = requests.get("https://data.cityofnewyork.us/resource/5rqd-h5ci.json")
    r.raise_for_status()

    data = r.json()
    for d in data:
        d['the_geom'] = shape(d['the_geom'])

    gdf = gpd.GeoDataFrame(data).set_geometry('the_geom')
    gdf.plot(figsize=(6, 6))
    plt.show()
#    print(gdf.head())


if __name__ == "__main__":
    test_feature()
    print("Everything passed")