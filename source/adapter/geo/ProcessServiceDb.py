from collections import defaultdict
from datetime import datetime
from itertools import groupby
from operator import itemgetter
import os
import traceback
from typing import Dict
import uuid
from xmlrpc.client import Boolean, boolean
import geopandas as gpd
from geopandas.geodataframe import GeoDataFrame
from geopandas.geoseries import GeoSeries
import pandas
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from pyproj.crs.crs import CRS
from shapely.geometry.geo import mapping
from shapely.geometry.linestring import LineString
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon, orient
import matplotlib.pyplot as plt
import shapely as shp
import shapely.ops as shp_ops
import yaml as yaml
from shapely.geometry.base import GeometrySequence
from entity.urban.Block import Block
from adapter.geo.Geometry import Geometry
from urban.Lot import Lot
from usecase.core.ConfigurationService import ConfigurationService
from shapely.ops import polygonize
from sqlalchemy import create_engine

class ProcessServiceDb():

    def __init__(self, configurationService:ConfigurationService):
        self.configurationService = configurationService
        self.__prop = configurationService.get_prop()
        self.__conf = configurationService.get_conf()

        db_connection_url = "postgresql://postgres:postgres@algoritmo-ciudad3d-db:5432/public"
        self.__con = create_engine(db_connection_url)  

    process_result = []

    def append_result(self, param):
        param_string = ""
        if (param != None):
            for key in param:
                param_string = param_string + (' > ' if param_string.__len__() > 0 else '') + key + " : " + param[key]
        log = (self.get_time() + param_string) 
        self.process_result.append(log)
        print (log)

    def get_time(self):
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + " > " 

    def map_block(self, attribute:dict[str, str], item:Series, geo_block:dict[str, list[Geometry]], block_lots:dict[str, list[Lot]]): 
        
        block = Block()
        block.set_name(item[attribute['sm']])
        block.set_type(item[attribute['mz_tipo']])
        
        geometry = Geometry()
        geometry.set_name('manzanas')
        geometry.set_value(item['the_geom'])
        block.set_geometries([geometry])

        if (block.get_name() in geo_block):
            block.set_geometries(block.get_geometries() + geo_block[block.get_name()])

        if (block.get_name() in block_lots):
            block.set_lots(block_lots.get(block.get_name()))
        return block

    def validate(self, block:Block, layer_name:str):
        result = False
        cause = ''
        key_geometry = {x.get_name(): x for x in block.get_geometries()}
        restriction_block_name = self.__prop['geometry.restriction-block.name']
        restriction_done_name = self.__prop['geometry.restriction-done.name']

        if (block.get_type() in ['TIPICA']):
            for geometry in block.get_geometries():
                if (geometry.get_name() == layer_name):
                    if (geometry.get_value().geom_type == 'MultiPolygon'):
                        for item in geometry.get_value().boundary: 
                            if (item.coords.__len__() == 5):
                                restriction_block = key_geometry.get(restriction_block_name)
                                restriction_done = key_geometry.get(restriction_done_name)
                                if (restriction_block == None or (restriction_block != None and restriction_done != None)):
                                    result = True
                                else:
                                    cause = 'discard > has restriction not valid'
                            else:
                                cause = 'discard > size > 4 '                         
                    else:
                        cause = 'discard > not MultiPolygon'
        else:
            cause =  'discard > not TIPICA '

        if (not result):
            self.append_result({'block':block.get_name(), 'cause':cause }) 

        return result

    def create_geometry_line_block(self, block:Block):

        geometry_name = self.__prop['geometry.block-line.name']
        geometry_origin = self.__prop['geometry.block-line.origin']
        geometry_name_origin = self.__prop['geometry.' + geometry_origin + '.name']

        key_geometry = {x.get_name(): x for x in block.get_geometries()}

        if (geometry_name_origin in key_geometry):
            geometry = key_geometry[geometry_name_origin]
            for item in geometry.get_value().boundary: 
                if (item.coords.__len__() == 5):
                    lines = []
                    for idx, point in enumerate(item.coords):
                        if (idx < 4):
                            lines.append(LineString([item.coords[idx], item.coords[idx + 1]]))
                    if (lines.__len__() > 0):
                        geometry = Geometry()
                        geometry.set_name(geometry_name)
                        geometry.set_value(MultiLineString(lines))
                        block.get_geometries().append(geometry)

        
    def create_geometry_base_line(self, block:Block, key:str):

        geometry_name = self.__prop['geometry.' + key + '.name']
        proportion = self.__prop['geometry.' + key + '.divided-by']
        geometry_line_name = self.__prop['geometry.' + key + '-line.name']
        geometry_origin = self.__prop['geometry.' + key + '.origin']
        geometry_origin_name = self.__prop['geometry.' + geometry_origin + '.name']

        self.append_result({'block':block.get_name(), 'calculate':geometry_name})

        for geometry in block.get_geometries():
            if (geometry.get_name() == geometry_origin_name):    
                group = [[0,2],[1,3]]
                lines = [None] * group.__len__()
                lines_total = []
                result = []
                for k, pair in enumerate(group):
                    lines[k] = []
                    center = []
                    for idx in pair:
                        line = geometry.get_value()[idx]
                        center.append(line.centroid)

                    lineCenter = LineString(center)    
                    distance = lineCenter.length / proportion
                    for idx in pair:
                        line:LineString = geometry.get_value()[idx]
                        serieOffset:GeoSeries = GeoSeries(line.parallel_offset(distance)).scale(2, 2)
                        if (serieOffset.__len__() > 0):
                            lineOffset = serieOffset[0]
                            lines[k].append(lineOffset)
                            lines_total.append(lineOffset)
                
                pc = [[0,1],[1,0]]
                for gpc in pc:
                    l1 = lines[gpc[0]]
                    l2 = lines[gpc[1]]
                    for l in l1:
                        s = GeoSeries(l)
                        s2 = GeoSeries(MultiLineString(l2))
                        result.append(LineString(s.intersection(s2)[0]))    

                geo = MultiLineString(lines_total)
                geometryTemp = Geometry()
                geometryTemp.set_name(geometry_line_name)
                geometryTemp.set_value(geo)
                block.get_geometries().append(geometryTemp)

                geo = MultiLineString(result)
                geometryTemp = Geometry()
                geometryTemp.set_name(geometry_name)
                geometryTemp.set_value(geo)
                block.get_geometries().append(geometryTemp)        

            

    '''
        transferAttributes: 
        Transfer attributes from one frame to other frame, using spatial joins
    '''
    def transfer_attributes(self, from_layer, to_layer):
        return to_layer.sjoin(from_layer, how="inner", op='intersects');   


    def map_restriction_block(self, item:Series, key_block:dict, attributes:dict[str, str]): 
        
        geometry_name = self.__prop['geometry.restriction-block.name']
        block = None

        if (item[attributes['sm']] in key_block):
            block = key_block[item[attributes['sm']]]

        if (block == None):
            block = Block()
            block.set_name(item[attributes['sm']])
            param = {
                'tipo': item[attributes['tipo']],
                'nro_ord': item[attributes['nro_ord']],
                'obs': item[attributes['obs_left']]
            }
            geometry = Geometry()
            geometry.set_name(geometry_name)
            geometry.set_value(item[attributes['the_geom']])
            geometry.set_param(param)
            block.set_geometries([geometry])
        else:
            key_geometry = {x.get_name(): x for x in block.get_geometries()}
            if (geometry_name in key_geometry):
                geo:Geometry = key_geometry[geometry_name]
                lines = geo.get_param().get("lines")
                if (lines == None):
                    lines = 2
                else:
                    lines = lines + 1
                geo.get_param()["lines"] = lines
                
                list = []
                for obj in item['geometry'].geoms:
                    list.append(obj)
                for obj in geo.get_value().geoms:
                    list.append(obj)
                geo.set_value(MultiLineString(list))


        key_block[block.get_name()] = block

    def validate_restriction(self, block:Block):
        result = False
        cause = ''
        validate_type_list = self.__conf['geometry']['restriction-done']['validate-type']
        validate_obs_list =  self.__conf['geometry']['restriction-done']['validate-obs']
        geometry_name = self.__prop['geometry.restriction-block.name']
        key_geometry = {x.get_name(): x for x in block.get_geometries()}

        if (geometry_name in key_geometry):
            geometry = key_geometry[geometry_name]

            if (geometry.get_param()['tipo'] in validate_type_list):
                if (geometry.get_param()['obs'] in validate_obs_list):
                    if (geometry.get_param().get("lines") == None):
                        if (geometry.get_value().geom_type == 'MultiLineString'):
                            if (geometry.get_value().geoms.__len__() == 1):
                                result = True
                            else:
                                cause = 'discard restriction > restriction line quantity > 1'
                        else:
                            cause = 'discard restriction > not MultiLineString'
                    else:
                        cause = 'discard restriction size = ' + str(geometry.get_param().get("lines"))
                else:
                    cause = 'discard restriction > not valid observation '
            else:
                cause = 'discard restriction > not valid type '

        if (not result):
            self.append_result({'block':block.get_name(), 'cause':cause }) 

        return result            

    def create_geometry_restriction_done(self, block:Block):
        
        geo_block_name = self.__prop['geometry.restriction-done.name']
        geo_block_origin = self.__prop['geometry.restriction-done.origin']
        geo_block_origin_name = self.__prop['geometry.' + geo_block_origin + '.name']
        key_geo = {x.get_name(): x for x in block.get_geometries()}

        if (geo_block_origin_name in key_geo):
            geo:Geometry = Geometry()
            geo.set_name(geo_block_name) 
            geo.set_value(key_geo[geo_block_origin_name].get_value())
            block.get_geometries().append(geo)

    def analize_attributes(self, frame) -> dict[str, str]:

        result = dict[str, str]()
        for col in frame.columns:
            result[col.lower()] = col
        return result


    def process_restriction(self, block_frame) -> list[Block]:

        layer_name = self.__prop['geometry.restriction.layer']
        sql = "select * from cur_restricciones"
        restriction_frame = gpd.read_postgis(sql, self.__con, 'the_geom')
        restriction_frame_with_block = self.transfer_attributes(block_frame, restriction_frame)
        attributes = self.analize_attributes(restriction_frame_with_block)

        key_block = {}
        for idx, item in restriction_frame_with_block.iterrows():
            self.map_restriction_block(item, key_block, attributes)

        for key in key_block:
            validatedBlock = self.validate_restriction(key_block[key])
            if (validatedBlock):
                self.create_geometry_restriction_done(key_block[key])

        listBlock = key_block.values()
        return list(listBlock)

    def process_before_each_block(self, block_layer) -> dict[str, list[Geometry]]:
        
        blocks = self.process_restriction(block_layer)
        key_geo = {x.get_name(): x.get_geometries() for x in blocks}
        return key_geo

    def calculate_with_restrictions(self, block:Block):
        geo_block_name = self.__prop['geometry.block.name']
        geo_block_restriction_name = self.__prop['geometry.block-restriction.name']
        geo_restriction_name = self.__prop['geometry.restriction-done.name']
        restriction_scalarX = self.__prop['geometry.restriction-done.scalar-x']
        restriction_scalarY = self.__prop['geometry.restriction-done.scalar-y']
        key_geo = {x.get_name(): x for x in block.get_geometries()}

        geoResult = key_geo[geo_block_name].get_value()
        cause = ''

        if (geo_restriction_name in key_geo):
            geoResult = None
            restriction_geo:MultiLineString = key_geo[geo_restriction_name].get_value()
            block_geo = key_geo[geo_block_name].get_value()
            serieOffset:GeoSeries = GeoSeries(restriction_geo).scale(restriction_scalarX, restriction_scalarY)
            if (serieOffset.__len__() > 0):
                lineScaled = serieOffset[0]
            geos = shp_ops.split(block_geo, lineScaled.geoms[0])
            max_value = 0
            for g in geos.geoms:
                area = g.area
                if (area > max_value):
                    geoResult = MultiPolygon([g])
                    max_value = area
                
        if (geoResult != None):
            geo:Geometry = Geometry()
            geo.set_name(geo_block_restriction_name) 
            geo.set_value(geoResult)
            block.get_geometries().append(geo)

    def calculate_with_restrictions_method_buffer(self, block:Block):
        geo_block_name = self.__prop['geometry.block.name']
        geo_block_restriction_name = self.__prop['geometry.block-restriction.name']
        geo_restriction_name = self.__prop['geometry.restriction-done.name']
        restriction_scalarX = self.__prop['geometry.restriction-done.scalar-x']
        restriction_scalarY = self.__prop['geometry.restriction-done.scalar-y']
        restriction_buffer = self.__prop['geometry.restriction-done.buffer']

        key_geo = {x.get_name(): x for x in block.get_geometries()}

        geoResult = key_geo[geo_block_name].get_value()

        if (geo_restriction_name in key_geo):
            restriction_geo:MultiLineString = key_geo[geo_restriction_name].get_value()
            block_geo = key_geo[geo_block_name].get_value()

            serieOffset:GeoSeries = GeoSeries(restriction_geo).scale(restriction_scalarX, restriction_scalarY)
            max_value = 0
            geoResult = None
            cause = ''
            if (serieOffset.__len__() > 0):
                lineScaled = serieOffset[0]
                for sign in [-1, 1]:
                    buffer_geo = lineScaled.buffer((sign)*restriction_buffer, single_sided=True)
                    dfa = pandas.DataFrame({'geometry':MultiPolygon([buffer_geo])})
                    dfb = pandas.DataFrame({'geometry':block_geo})
                    gp1 = GeoDataFrame(dfa,geometry=dfa["geometry"])
                    gp2 = GeoDataFrame(dfb,geometry=dfb["geometry"])
                    intersection = gpd.overlay(gp1, gp2, how='intersection' )
                    if intersection.shape[0] == 1:
                        area = intersection.area[0]
                        if (area > max_value):
                            geoResult = MultiPolygon([intersection.iloc[0]['geometry']])
                            max_value = area
                    else:
                        cause =  'discard calculate block with restriction > intersection result <> 1 in sign (' + sign + ')'                       

            else:
                cause =  'discard calculate block with restriction > scalar restriction > 1 '
            if (cause != ''):
                geoResult = None
                self.append_result({'block':block.get_name(), 'cause':cause }) 

        if (geoResult != None):
            geo:Geometry = Geometry()
            geo.set_name(geo_block_restriction_name) 
            geo.set_value(geoResult)
            block.get_geometries().append(geo)

    def export(self, blocks:list, crs, plot = False) -> dict:

        self.append_result({'export-format': 'gpkg', 'start':''})
        output_name = self.__prop.get('output.name')
        output_random = self.__prop.get('output.random')
        output_folder = self.__prop.get('output.folder')
        output_context = self.__prop.get('output.context')

        result = {}

        name = ''
        if (output_name != None):
            name = output_name
        else:
            if (output_random):
                name = str(uuid.uuid4())

        if (name != None):
            output_root = "./" + output_folder + "/" + name 
            output_file_path = "./" + output_folder + "/" + name + ".gpkg"

            if os.path.exists(output_file_path):
                os.remove(output_file_path)

            layers = {}
            for block in blocks:
                for geometry in block.get_geometries():
                    key = geometry.get_name()
                    if ( key not in layers.keys()):
                        layers[key] = []
                    element = {}
                    element['geometry'] = geometry
                    element['entity'] = block
                    for k, v in geometry.get_param().items():
                        element[k] = v
                    layers[key].append(element)
                for lot in block.get_lots():
                    for geometry2 in lot.get_geometries():
                        key = geometry2.get_name()
                        if ( key not in layers.keys()):
                            layers[key] = []
                        element = {}
                        element['geometry'] = geometry2
                        element['entity'] = lot
                        for k, v in geometry2.get_param().items():
                            element[k] = v
                        layers[key].append(element)


            for key in layers:
                layer = layers[key]
                all_keys = set().union(*(d.keys() for d in layer))
                all_keys.add('id')
                all_keys.add('geometry')
                all_keys.remove('entity')
                data = {}
                for k in all_keys:
                    data[k] = []
                for element in layer:
                    for k in all_keys:
                        if (k == 'id'):
                            value = element['entity'].get_name()
                            data['id'].append(value)
                        elif (k == 'geometry'):
                            data['geometry'].append(element['geometry'].get_value())
                        else:
                            if (k in element):
                                data[k].append(element[k])
                            else:
                                data[k].append(None)
                gdf = gpd.GeoDataFrame(data, crs=crs, geometry="geometry" )
                crs = CRS.from_user_input("+proj=tmerc +lat_0=-34.629269 +lon_0=-58.4633 +k=0.9999980000000001 +x_0=100000 +y_0=100000 +ellps=intl +units=m +no_defs")
                gdf.set_crs(crs)

                if (plot):
                    gdf.plot(figsize=(6, 6))
                    plt.show()

                gdf.set_geometry(col='geometry', inplace=True)
                gdf.to_file(output_file_path, layer=key, driver="GPKG")

            self.append_result({'export-format': 'gpkg', 'end':''})   

            result = {
                'name':name,
                'output_root':output_root,
                'context': output_context, 
                'url':"/" + output_context + "/" + name + ".gpkg" 
            }

        return result

    def export_log(self, process:dict) :

        output_file_path = process['output_root'] + ".log"
        process['log'] = "/" + process['context'] + "/" + process['name'] + ".log"
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        text_file = open(output_file_path, "w")
        text_file.write('\n'.join(self.process_result))
        text_file.close()

        return output_file_path

    def map_lot(self, item:Series): 
        
        geometry_name = self.__prop['geometry.lot.name']
        lot = Lot()
        block = Block()
        block.set_name(item["seccion"] + '-' + item["manzana"])
        lot.set_block(block)
        lot.set_name(item["smp"])
        lot.get_heights().append(item["uni_edif_1"])
        lot.get_zones().append(item["zona_1"])
        lot.get_special_areas().append(item["dist_1_esp"])            
        lot.set_protection(item["proteccion"])
        geometry = Geometry()
        geometry.set_name(geometry_name)
        geometry.set_value(item['the_geom'])
        lot.set_geometries([geometry])
        return lot


    def process_lot(self, block_name) -> dict[str, list[Lot]]:

        sql = """
              select a.*, b.proteccion from cur_parcelas a 
              left join aph_ssregic b on a.smp = b.smp
              """
        sql = sql + "where (a.seccion || '-' || a.manzana)  = '" + block_name + "'"

        lot_frame = gpd.read_postgis(sql, self.__con, 'the_geom')

        lots = list[Lot]()
        for idx, item in lot_frame.iterrows():
            lot = self.map_lot(item)
            if (lot != None):
                lots.append(lot)

        groups = defaultdict(list)
        for lot in lots:
            groups[lot.get_block().get_name()].append(lot)

        return groups

    def validate_buildability(self, block:Block, lot:Lot) -> bool:
        cause=''
        if (9 in lot.get_heights() or 11.6 in lot.get_heights()):
            if (not (lot.get_protection() in self.__conf['geometry']['lot']['validate_protection'])):
                cause=''
            else:
                cause='protection validation > ' + lot.get_protection()
        else:
            cause='discard buildability lot > height not valid '

        if (cause != ''):
            self.append_result({'lot':lot.get_name(), 'cause':'discard buildability > ' + cause }) 
        
        return (cause == '')

    def calculate_buildability_1(self, block:Block, lot:Lot):

        if (len(lot.get_heights()) == 1):
            buildability = 'buildability_1'
            type = lot.get_heights()[0]
            height_name = 'height.' + str(type) + '.' + buildability
            if (height_name in self.__prop):
                height = self.__prop[height_name]

                self.append_result({'lot':lot.get_name(), 'calculate':buildability})

                block_geo = {x.get_name(): x for x in block.get_geometries()}
                inside_line_name = self.__prop['geometry.lbi.name']
                lo_line_origin = self.__prop['geometry.' + buildability + '.lo']
                lo_line_name = self.__prop['geometry.' + lo_line_origin + '.name']

                if (inside_line_name in block_geo and lo_line_name in block_geo):
                    inside = GeoSeries(polygonize(block_geo[inside_line_name].get_value()))[0]
                    lo = GeoSeries(polygonize(block_geo[lo_line_name].get_value()))[0]
                    difference = lo.difference(inside)
                    result = difference.intersection(lot.get_geometries()[0].get_value())

                    name = self.__prop['geometry.' + buildability + '.name']
                    param = dict()
                    param["z"] = height

                    geo:Geometry = Geometry()
                    geo.set_name(name) 
                    geo.set_value(result)
                    geo.set_param(param)
                    lot.get_geometries().append(geo)

    def calculate_buildability_2(self, block:Block, lot:Lot):

        if (len(lot.get_heights()) == 1):
            buildability = 'buildability_2'
            retire = 'retire_2'
            type = lot.get_heights()[0]
            height_name = 'height.' + str(type) + '.' + buildability
            retire_name = 'height.' + str(type) + '.' + retire
            if (height_name in self.__prop and retire_name in self.__prop):
                height = self.__prop[height_name]
                retire = self.__prop[retire_name]
                self.append_result({'lot':lot.get_name(), 'calculate':buildability})

                block_geo = {x.get_name(): x for x in block.get_geometries()}
                lot_geo = {x.get_name(): x for x in lot.get_geometries()}
                geo_base = self.__prop['geometry.buildability_1.name']
                lo_line_origin = self.__prop['geometry.' + buildability + '.lo']
                lo_line_name = self.__prop['geometry.' + lo_line_origin + '.name']
                buildability_sign = self.__prop['geometry.' + buildability + '.sign']

                if (geo_base in lot_geo and lo_line_name in block_geo):
                    base = lot_geo[geo_base].get_value()
                    lo = block_geo[lo_line_name].get_value()
                    intersection = lo
                    buffer_intersection = intersection.buffer((buildability_sign)*retire, single_sided=True)
                    result = base.difference(buffer_intersection)

                    name = self.__prop['geometry.' + buildability + '.name']
                    param = dict()
                    param["z-init"] = lot_geo[geo_base].get_param()['z']
                    param["z"] = param["z-init"] + height

                    geo:Geometry = Geometry()
                    geo.set_name(name) 
                    geo.set_value(result)
                    geo.set_param(param)
                    lot.get_geometries().append(geo)

    def calculate_official_line(self, block:Block):
        
        list = []
        for lot in block.get_lots():
            for geo in lot.get_geometries():
                list.append(geo.get_value())
        df = pandas.DataFrame({'geometry':list})
        gp = GeoDataFrame(df,geometry=df["geometry"])
        dissolve_serie = gp.dissolve().geometry
        if (dissolve_serie.__len__() > 0):
            dissolve = dissolve_serie[0]      

            name = self.__prop['geometry.official_line.name']
        
            geo:Geometry = Geometry()
            geo.set_name(name) 
            geo.set_value(dissolve)
            block.get_geometries().append(geo)

    def calculate_minimal_band(self, block:Block):

        name = self.__prop['geometry.minimal_band.name']
        
        geo:Geometry = Geometry()
        geo.set_name(name) 
        geo.set_value(None)
        block.get_geometries().append(geo)


    def execute(self, block_name:str) -> dict:
        sql = "select * from mo_manzanasmap where sm = '" + block_name + "'"
        block_frame = gpd.read_postgis(sql, self.__con, 'the_geom')

        self.process_result = []
        blocks_with_geometries = self.process_before_each_block(block_frame)
        block_lots = self.process_lot(block_name)
        attribute = self.analize_attributes(block_frame)

        blocks = []
        for idx, item in block_frame.iterrows():
            try:
                block:Block = self.map_block(attribute, item, blocks_with_geometries, block_lots)
                blocks.append(block)

                validated_block = self.validate(block, self.__prop['geometry.block.name'])
                if (validated_block):
                    self.calculate_with_restrictions(block)
                    #This validation has to change to validate to create base line only
                    validated_block = self.validate(block, self.__prop['geometry.block-restriction.name'])
                    if (validated_block):
                        self.create_geometry_line_block(block)
                        self.create_geometry_base_line(block, 'lbi')
                        self.create_geometry_base_line(block, 'lfi')

                self.calculate_official_line(block)
                #self.calculate_minimal_band(block)

                for lot in block.get_lots():
                    validated_lot = self.validate_buildability(block, lot)
                    if (validated_lot):
                        self.calculate_buildability_1(block, lot)
                        self.calculate_buildability_2(block, lot)

            except Exception as e:
                print(traceback.format_exc())
                self.append_result({'item':item[attribute['sm']], 'cause': "exception" + str(e)}) 

        process = self.export(blocks, block_frame.crs)
        self.export_log(process)

        return process

