import traceback
from numpy import number
from pyproj import CRS
import pyproj
from usecase.core.LogService import LogService
from entity.geo.Geometry import Geometry
import numpy
import shapely as shp
import pandas
import shapely.ops as ops
from geopandas.geodataframe import GeoDataFrame
from geopandas.geoseries import GeoSeries
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.multipoint import MultiPoint
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import Polygon, orient
from shapely.validation import make_valid
from shapely.ops import linemerge, unary_union, polygonize, cascaded_union, transform
from shapely.ops import snap
import matplotlib.pyplot as plt
import math
from decimal import *

class GisLibrary:

    def __init__(self,
                 log_service:LogService) -> None:

        self.__projection:dict = {}
        self.__transformation:dict = {}
        self.__log_service = log_service

    def reduce_precision(self, geos:any, precision:number) -> Geometry:
        shps = self.__to_shape_list(geos)
        new_shps = []
        for sh in shps:
            new_sh = shp.wkt.dumps(sh, rounding_precision=precision)
            new_shps.append(new_sh)
        return self.__to_geo(new_shps) 

    def dissolve_union(self, geos:any, round=False) -> Geometry:

        geos = self.dissolve(geos, round)
        if (geos):
            shps = self.__to_shape_list(geos)
            shps_geos = list(shps)
            
            new_shps = []
            for shp in shps_geos:
                if (shp.geom_type == "Polygon"):
                    new_shps.append(Polygon(shp.exterior.coords))
                else:
                    print('stop')
                
            return self.__to_geo(new_shps)

        return None            

    def dissolve_union_list(self, geos:any, round=False) -> list[Geometry]:

        geos = self.dissolve(geos, round)
        if (geos):
            shps = self.__to_shape_list(geos)
            shps_geos = list(shps)
            
            new_shps = []

            for shp in shps_geos:

                if (shp.geom_type == "MultiPolygon"):
                    for shp_child in list(shp):
                        new_shps.append(Polygon(shp_child.exterior.coords))

                elif (shp.geom_type == "Polygon"):
                    new_shps.append(Polygon(shp.exterior.coords))
                
            return self.__to_geo_list(new_shps)

        return None    

    def dissolve(self, geos:any, round=False) -> Geometry:
        
        shps = self.__to_shape_list(geos)
        if (shps):
            new_shps = []
            for shp in shps:
                if (not round):
                    new_shps.append(shp)
                else:
                    new_shps.append(shp.buffer(0.0000000001))

            shp_merge = self.__merge(new_shps)
            self.__merge(new_shps)
            geo_merge = self.__to_geo(shp_merge)
            gf = self.__to_frame(geo_merge)
            dissolve = gf.dissolve()
            if (not dissolve.empty): 
                serie = dissolve.geometry
                if (serie.__len__() > 0):
                    return self.__to_geo(serie[0]) 

        return None

    def spatial_join(self, origin:list[Geometry], destiny:list[Geometry],  origin_attributes:list = [], destiny_attributes:list = []) -> list[Geometry]:

        origin = self.__to_frame_relation(origin)
        destiny = self.__to_frame_relation(destiny)

        out = destiny['df'].sjoin(origin['df'], how="inner", op='intersects');   

        result = []
        for idx, it in out.iterrows():
            left = it['relation_left']
            right = it['relation_right']
            result.append((origin['relation'][right],destiny['relation'][left], it['geometry'].wkt))

        return result

    def add_projection(self, name:str, definition:str):
        crs = CRS.from_user_input(definition)
        self.__projection[str(name)] = crs

    def add_transformation(self, name:str, from_projection:str, to_projection:str):
        from_crs = self.__projection[from_projection]
        to_crs = self.__projection[to_projection]
        transformation = pyproj.Transformer.from_crs(from_crs, to_crs, always_xy=True).transform
        self.__transformation[name] = transformation

    def project(self, geo:Geometry, transformation_name):

        if (geo is not None):
            geo_result = geo
            if (transformation_name != None):
                shp_list = self.__to_shape_list(geo) 
                new_shp_list = []
                for item in shp_list:
                    new_shp_list.append(transform(self.__transformation[transformation_name], item))
                geo_result = self.__to_geo(new_shp_list)
                if (geo_result is None):
                    return None
            return geo_result.get_value()
            
        return None

    def is_gis_type(self, geo:Geometry, type:str) -> bool:
        serie = GeoSeries.from_wkt(geo.get_values())
        return (serie[0].geom_type == type)

    def scale(self, geo:Geometry, scale_x, scale_y, origin="center") -> Geometry:
        try:
            series = self.__scale(geo, scale_x, scale_y, origin=origin)
        except Exception as e:
            print("ERROR EXCEPTION:", e)
        return self.__to_geo(series)

    def __scale(self, obj:any, scale_x:number, scale_y:number, origin="center") -> GeoSeries:
        series = self.__to_serie(obj)
        if (not series is None):
            result = series.scale(scale_x, scale_y, origin=origin)
            if (not result.empty):
                return result
            return None

    def snap(self, geos:any) -> list[Geometry]:

        shps = self.__to_shape_list(geos)
        size = len(shps)
        
        for x in range(size):
            for y in range(size):
                if (x != y):
                    res = snap(shps[x], shps[y], 0.0000001)
                    shps[x] = res

        return self.__to_geo(shps)
            
   
    def interpolate(self, line:Geometry, distance:number) -> Geometry:
        shptmp:LineString = self.__to_shape(line)  
        point:Point = shptmp.interpolate(distance)
        return self.__to_geo(point)

    def find_vertice_and_adjacent(self, geo:Geometry) -> list[tuple[Geometry, list[Geometry]]]:

        lines = self.__disaggregate(geo)
        response = []
        if (lines is not None):
            size = len(lines)
            for idx, line in enumerate(lines):
                ida = idx - 1 if idx > 0 else size - 1
                idb = idx + 1 if idx < size -1 else 0
                if (idx < size):
                    p = self.__to_geo(Point(lines[idx].coords[0]))
                    p1 = self.__to_geo(Point(lines[ida].coords[0]))
                    p2 = self.__to_geo(Point(lines[idb].coords[0]))
                    it = (p, [p1, p2])
                    response.append(it)
                        
        return response

    def find_side_rectangle(self, points:list[Geometry], distance:number) -> number: 
        line = self.__merge(points)
        distance_2:number = line.length

        result = numpy.sqrt(distance_2**2 - distance**2)
        return result

    def angle(self, vertice:Geometry, points:list[Geometry]) -> number: 

        b = self.__to_shape(vertice) 
        a = self.__to_shape(points[0]) 
        c = self.__to_shape(points[1]) 

        ang = math.degrees(math.atan2(c.y-b.y, c.x-b.x) - math.atan2(a.y-b.y, a.x-b.x))
        return ang + 360 if ang < 0 else ang

    def split(self, origin:Geometry, splitter:Geometry) -> list[Geometry]:

        shp_origin = self.__cast(origin, 'LineString')
        shp_splitter = self.__cast(splitter, 'LineString')

        merged = linemerge([shp_origin, shp_splitter])
        borders = unary_union(merged)
        polygons = polygonize(borders)

        response = []
        for shp in polygons:
            response.append(self.__to_geo(shp))
        return response

    def get_area(self, geo:any) -> number:
        shps = self.__to_shape_list(geo)
        shp = self.__merge(shps)
        return shp.area if shp is not None else 0

    def length(self, geo:Geometry) -> number:
        shp = self.__to_shape(geo)
        return shp.length

    def disaggregate(self, geo:Geometry, destiny:str = 'LineString') -> Geometry:
        shp = self.__disaggregate(geo, destiny)
        return self.__to_geo(shp)

    def disaggregate_list(self, geos:any, destiny:str = 'LineString') -> list[Geometry]:
        shps = self.__disaggregate(geos, destiny)
        return self.__to_geo_list(shps)

    def __disaggregate(self, obj:any, destiny:str = 'LineString') -> list[BaseGeometry]:
        shps = self.__to_shape_list(obj)

        cast_shps = []
        for shp in shps:
            cast_shps.append(self.__cast_gis(shp, destiny))

        response = []
        if (cast_shps):
            for shp in cast_shps:
                try:
                    geos = shp.coords if destiny == 'LineString' else shp.geoms
                    size = len(geos)
                    if (destiny == 'LineString'):
                        for idx, it in enumerate(geos):
                            if (idx < size - 1):
                                shp_tmp = LineString([geos[idx], geos[idx + 1]])
                                response.append(shp_tmp)
                    elif (destiny == 'MultiPoint'):
                        for idx, it in enumerate(geos):
                            shp_tmp = Point(it.x, it.y)
                            response.append(shp_tmp)
                    elif (destiny == "Polygon"):
                        for idx, it in enumerate(geos):
                            shp_tmp = Polygon(it)
                            response.append(shp_tmp)
                except Exception:
                    response.append(shp)

        return response

    def find_point_center(self, geo:Geometry) -> Geometry:
        shp = self.__to_shape(geo)
        result = shp.centroid
        return self.__to_geo(result)

    def export(self, layer_name:str, geos:list[Geometry], path):

        gdf = self.__to_frame(geos)
        gdf.set_geometry(col='geometry', inplace=True)
        gdf.to_file(path, layer=layer_name, driver="GPKG")
        # crs = self.__pdiRepository.get_crs(crs)
        # gdf.set_crs(crs)

    def export_infos(self, infos:list,path:str, type:str, geo_attribute:str, projection:str, layer_name:str = None):
        gdf = self.__to_frame_dict(infos, geo_attribute)
        gdf.set_geometry(col=geo_attribute, inplace=True)
        gdf.to_file(path, crs=self.__projection[projection], layer=(layer_name if layer_name is not None else None), driver=type)

    def export_geos(self, infos:list,path:str, type:str, geo_attribute:str, projection:str, layer_name:str = None):
        gdf = self.__to_frame_geo(infos, geo_attribute)
        gdf.to_file(path, crs=self.__projection[projection], layer=(layer_name if layer_name is not None else None), driver=type)

    def merge(self, geos:list[Geometry]) -> Geometry:
        return self.__to_geo(self.__merge(geos))

    def parallel_offset(self, geo:Geometry, distance:number, side:str = 'right') -> Geometry:        
        shp = self.__to_shape(geo)
        result = shp.parallel_offset(distance, side)
        return self.__to_geo(result)

    def find_closest_parallel(self, geo:Geometry, comparison:Geometry, parallel_distance, perpendicular_scalar) -> Geometry:       

        shps = self.__to_shape_list(geo)
        min_line = None
        if (shps.__len__() == 1):
            shp = shps[0]
            parallel = shp.parallel_offset(parallel_distance, 'right')
            p1 = shp.centroid
            p2 = parallel.centroid
            perpendicular = self.__merge([p1, p2])
            scaled_perpendicular = self.__scale(perpendicular, perpendicular_scalar, perpendicular_scalar)

            comparison_lines = self.__disaggregate(comparison)
            min_length = None
            for comparison_line in comparison_lines:
                intersection = self.__intersection(scaled_perpendicular, comparison_line)
                if (intersection):
                    resulted_line = self.__merge([p1, intersection])
                    if (min_length is None or min_length > resulted_line.length):
                        min_length = resulted_line.length
                        min_line = comparison_line

        return self.__to_geo(min_line)

    def difference(self, geo:Geometry, subtrahends:list[Geometry]) -> Geometry:

        shps = self.__to_shape_list(geo)
        result = None
        if (shps.__len__() == 1):
            result = shps[0]
            subs = self.__to_shape_list(subtrahends)
            for sub in subs:
                result = result.difference(sub)
        
        if (result is None or result.is_empty):
            result = None
        return self.__to_geo(result)

    def intersects(self, origin:any, destiny:any) -> bool:        
        shp_ori = self.__merge(origin)
        shp_des = self.__merge(destiny)
        result = shp_ori.intersects(shp_des)
        return result

    def intersection(self, origin:any, destiny:any) -> Geometry:       
        return self.__to_geo(self.__intersection(origin, destiny))

    def __intersection(self, origin:any, destiny:any) -> list[BaseGeometry]:
        origin_shp = self.__merge(origin)
        destiny_shp = self.__merge(destiny)
        result = origin_shp.intersection(destiny_shp) 
        if (not result.is_empty):
            return result
        return None

    def buffer(self, geo:Geometry, buffer, single_side=False, sign = 1, cap_style = 2, join_style = 2) -> Geometry:
        shp:BaseGeometry = self.__to_shape(geo)
        if (shp):
            result = shp.buffer((sign)*buffer, single_sided=single_side, cap_style=cap_style, join_style=join_style)
            return self.__to_geo(result)
        else:
            return None

    def plot(self, geos:any):
        data = self.__to_data_list(geos)
        gdf = self.__to_frame_gis(data)        
        gdf.plot(figsize=(6, 6))
        plt.show()

    def cast(self, geo:Geometry, cast:str) -> Geometry:
        if geo is not None:
            try:
                return self.__to_geo(self.__cast(geo, cast))
            except Exception:
                self.__log_service.add({'message':'GIS ERROR > CASTING ', 'error':traceback.format_exc()})
        return None

    def __cast(self, geo:Geometry, cast:str) -> Geometry:

        shp = self.__to_shape(geo)
        return self.__cast_gis(shp, cast)

    def convert(self, geos, to:str) -> list[Geometry]:
        shps = self.__to_shape_list(geos)
        shps = self.__convert(shps, to)
        return self.__to_geo_list(shps)

    def convert_one(self, geos, to:str) -> Geometry:
        geos = self.convert(geos, to)
        return self.__to_geo(geos)

    def get_value(self, geo:Geometry) -> str:
        if (geo is None):
            return ""
        return geo.get_value()

    def __convert(self, shps:list[BaseGeometry], to:str) -> list[BaseGeometry]:

        hierarchy = ['MultiPolygon', 'Polygon', 'MultiLineString', 'LineString', 'MultiPoint', 'Point']
        result:list[BaseGeometry] = []    

        for shp in shps:

            from_idx = hierarchy.index(shp.geom_type)
            to_idx = hierarchy.index(to)
            if from_idx == to_idx:
                return shps

            descending = from_idx < to_idx 
            ascending = not descending
            values:list[BaseGeometry] = [shp]

            for i in range(from_idx + (1 if descending else -1), to_idx + (1 if descending else -1), -1 if ascending else 1):
                type_geom = hierarchy[i]
                temp = []
                if (type_geom == "MultiPolygon" and ascending):
                    values = [MultiPolygon(values)]
                if (type_geom == "Polygon" and ascending):
                    # Polygon <- MultLineString
                    for shp in values:
                        temp.append(Polygon(shp.coords))
                    values = temp
                if (type_geom in "Polygon" and descending):
                    # MultiPolygon -> Polygon
                    for it in shp.geoms:    
                        temp.append(it)
                    values = temp
                if (type_geom == "MultiLineString" and descending):
                    # Polygon -> MultiLineString
                    for shp in values:
                        if shp.boundary.type == "LineString":
                            temp.append(MultiLineString([shp.boundary]))
                        elif shp.boundary.type == "MultiLineString":
                            temp.append(shp.boundary)
                    values = temp
                if (type_geom == "MultiLineString" and ascending):
                    values = [MultiLineString(values)]
                if (type_geom == "LineString" and descending):
                    # MultiLineString -> LineString
                    for shp in values:
                        for it in shp.geoms:
                            temp.append(it)
                    values = temp
                if (type_geom == "MultiPoint" and descending):
                    # LineString -> MultiPoint
                    for shp in values:
                        if shp.boundary.type == "MultiPoint":
                            temp.append(shp.boundary)
                    values = temp        
                if (type_geom == "Point" and descending):
                    # MultiPoint -> Point
                    for it in shp.coords:    
                        temp.append(Point(it[0], it[1]))
                    values = temp

            result.extend(values)

        return result

    def __cast_gis(self, shp, cast:str) -> BaseGeometry:

        new_shp:any = None
        origin = shp.geom_type

        if (origin == cast):
            return shp

        elif (origin == "Polygon"):
            if (cast == "MultiPolygon"):
                new_shp = MultiPolygon([shp])
            elif (cast == "LineString"):
                new_shp = linemerge([shp.boundary])

        elif (origin == "MultiPolygon"):                
            if (cast == "MultiLineString"):
                new_shp = shp.boundary
            elif (cast == "LineString"):
                new_shp = linemerge(shp.boundary)
            elif (cast == "Polygon"):
                new_shp = self.__to_poligonize(shp)

        elif (origin == "MultiLineString"):
            if (cast == "LineString"):
                new_shp = linemerge(shp.geoms)
            elif (cast == "Polygon"):
                new_shp = self.__to_poligonize(shp)
            elif (cast == "Point"):
                new_shp = linemerge(shp.geoms)
                new_shp = self.__cast_gis(new_shp, "MultiPoint")

        elif (origin == "MultiPoint"):                
            if (cast == "LineString"):
                new_shp = LineString(shp)

        elif (origin == "LineString"):                
            if (cast == "MultiPoint"):
                shps = self.__to_list(shp)
                list = []
                for shp in shps:
                    list.extend(shp.boundary)
                new_shp = MultiPoint(list)
            elif (cast == "Polygon"):
                new_shp = self.__to_poligonize(shp)

        return new_shp

    def poligonize(self, geos:any) -> Geometry:
        shps = self.__to_shape_list(geos)
        result = []
        if shps:
            for shp in shps:
                result.append(self.__to_poligonize(shp))
        return self.__to_geo(result)

    def __to_poligonize(self, shp:any) -> BaseGeometry:
        result:BaseGeometry = None
        list_obj = []
        objs = polygonize(shp)
        for obj in objs:
            list_obj.append(obj)

        if (list_obj.__len__() == 1):
            result = obj
        elif (list_obj.__len__() > 1):
            result = MultiPolygon(list_obj)
        return result


    def __merge(self, geos:list[Geometry]) -> BaseGeometry:

        shps = self.__to_shape_list(geos)
        if (shps.__len__() == 1):
            return shps[0]

        result:BaseGeometry = None
        if (shps):
            origin = shps[0].geom_type
            if (origin == "Point"):
                result = LineString(shps)
            elif (origin == "LineString"):
                result = MultiLineString(shps)
            elif (origin == "Polygon"):
                result = MultiPolygon(shps)
            elif (origin == "MultiPoint"):
                result = LineString(shps)
            elif (origin == "MultiPolygon"):
                result = unary_union(shps)
                if (result.geom_type == "Polygon"):
                    result = MultiPolygon([result])
            elif (origin == "MultiLineString"):
                result = unary_union(shps)
                if (result.geom_type == "LineString"):
                    result = MultiLineString([result])

        return result

    def __to_frame_relation(self, geos:list[Geometry]) -> dict:

        list = []
        list_rel = []
        rel = {}
        for idx, geo in enumerate(geos):
            for value in geo.get_values():
                list.append(value)
                rel[idx] = geo
                list_rel.append(idx)
                
        data = {'geometry':list, 'relation':list_rel}
        df = pandas.DataFrame(data)
        df["geometry"] = GeoSeries.from_wkt(df["geometry"])
        result = {'df':GeoDataFrame(df,geometry=df["geometry"]), 'relation':rel}
        return result

    def __to_frame_dict(self, infos:list[dict], geo_attribute:str) -> GeoDataFrame:
        data = {}
        if (len(infos) > 0):
            for k in infos[0]:
                data[k] = []

            for info in infos:
                for k, value in info.items():
                    data[k].append(value)
        df = pandas.DataFrame(data)
        df[geo_attribute] = GeoSeries.from_wkt(df[geo_attribute])
        return GeoDataFrame(df,geometry=geo_attribute)        

    def __to_frame_geo(self, infos:list[dict], geo_attribute:str) -> GeoSeries:
        data = {}
        if (len(infos) > 0):
            for k in infos[0]:
                data[k] = []

            for info in infos:
                for k, value in info.items():
                    data[k].append(value)
        df = pandas.DataFrame(data)
        return GeoSeries.from_wkt(df[geo_attribute])

    def __to_frame(self, geos:list[Geometry], attribute:list = []) -> GeoDataFrame:
        list = []
        geos = self.__to_list(geos)
        for geo in geos:
            for value in geo.get_values():
                list.append(value)
        return self.__to_frame_gis(list, attribute)

    def __to_frame_gis(self, list:list[any], attribute:list = []) -> GeoDataFrame:

        data = {'geometry':list}
        df = pandas.DataFrame(data)
        df["geometry"] = GeoSeries.from_wkt(df["geometry"])
        return GeoDataFrame(df,geometry=df["geometry"])

    def __to_serie(self, obj:any) -> GeoSeries:
        geos = self.__to_data_list(obj)
        serie = GeoSeries.from_wkt(geos)
        if not serie.empty:
            return serie
        return None

    def __to_geo(self, shape) -> Geometry:
        geos = self.__to_data_list(shape)
        if (geos):
            geo = Geometry()
            geo.set_values(geos)
            return geo
        return None

    def __to_geo_list(self, shape) -> Geometry:
        shps = self.__to_data_list(shape)
        result = []
        if (shps):
            for shp in shps:
                result.append(self.__to_geo(shp))
        return result

    def __to_shape(self, geo:Geometry) -> any:

        value:str = None
        if (isinstance(geo, str)):
            value = geo
        elif (geo and not geo.is_multiple()):
            value = geo.get_value()
        if (value):
            return shp.wkt.loads(value)

        return None

    def __to_shape_list(self, obj) -> list[BaseGeometry]:

        result = []
        if (isinstance(obj, list)):
            for o in obj:
                result.extend(self.__to_shape_list(o))
        if (isinstance(obj, Geometry)):
            result.extend(self.__to_shape_list(obj.get_values()))
        if (isinstance(obj, BaseGeometry)):
            result.append(obj)
        elif (isinstance(obj, str)):
            result.append(shp.wkt.loads(obj))
        elif (isinstance(obj, GeoSeries)):
            for o in obj:
                result.extend(self.__to_shape_list(o))
            
        return result

    def __to_data_list(self, obj)-> list[any]:

        result = []
        if (isinstance(obj, list)):
            for o in obj:
                result.extend(self.__to_data_list(o))
        if (isinstance(obj, Geometry)):
            result.extend(self.__to_data_list(obj.get_values()))
        if (isinstance(obj, BaseGeometry)):
            result.append(obj.wkt)
        elif (isinstance(obj, str)):
            result.append(obj)
        elif (isinstance(obj, GeoSeries)):
            for o in obj:
                result.extend(self.__to_data_list(o))
            
        return result

    def __to_list(self, obj:any) -> list:
        if (not isinstance(obj, list)):
            return [obj]
        else:
            return obj
