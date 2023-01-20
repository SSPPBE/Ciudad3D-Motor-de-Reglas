from poplib import POP3
from sqlalchemy import intersect
from entity.urban.Lot import Lot
from entity.urban.Consolidation import Consolidation
from usecase.core.DictUtil import DictUtil
from entity.urban.Block import Block
from entity.urban.CornerArea import CornerArea
from adapter.geo.GisLibrary import GisLibrary
from entity.urban.Extension import Extension
from usecase.urban.LotService import LotService
from entity.geo.Geometry import Geometry

class CornerAreaService:

    def __init__(self,
                 gis_library:GisLibrary,
                 lot_service:LotService,
                 dict_util:DictUtil,
                 prop:dict) -> None:
        self.__prop = prop
        self.__gis_library = gis_library
        self.__lot_service = lot_service
        self.__dict_util = dict_util


    def build(self, block:Block):

        buffer = self.__prop['buffer']
        self.__lot_service.analize_heights(block)
        require_corner_area = self.__lot_service.require_corner_area(block)

        if (require_corner_area):    
            distance = self.__prop['corner_area']['distance']
            divided = self.__prop['corner_area']['divided']
            vertices_adjacents = self.__gis_library.find_vertice_and_adjacent(block.get_geometry('block_restrictions'))
            for vertice_adjacents in vertices_adjacents:
                vertice, adjacents = vertice_adjacents
                lines = []
                for adjacent in adjacents:
                    line_adjacent = self.__gis_library.merge([vertice, adjacent])
                    length = (self.__gis_library.length(line_adjacent) / divided) + 9
                    length = length if length < distance else distance
                    
                    point_interpolated = self.__gis_library.interpolate(line_adjacent, length)
                    line = self.__gis_library.merge([vertice, point_interpolated])
                    lines.append(line)

                corner_area = CornerArea()
                corner_area.add_value(self.__gis_library.merge(lines).get_value())
                block.get_corner_areas().append(corner_area)
        
            self.__build_regular_extension(block)

            for corner_area in block.get_corner_areas():
                if (corner_area.get_extension() is not None):
                    corner_lots = self.__complete_consolidation(block, corner_area, buffer)
                    irregular = False
                    for lot in corner_lots:
                        if (lot.get_consolidation() is not None):
                            irregular =  lot.get_consolidation().get_touched()
                            if irregular:
                                break
                    if (irregular):
                        #self.__build_irregular_extension(block, corner_area, corner_lots)
                        for lot in corner_lots:
                            lot.set_irregular(True)

            if (block.has_geometry('lfi') and not block.has_geometry("lfi_extension")):
                geos = [self.__gis_library.cast(block.get_geometry('lfi'), 'Polygon')]
                for corner_area in block.get_corner_areas():
                    geos.append(corner_area.get_extension())
                geos = self.__gis_library.snap(geos)
                lfi_extension = self.__gis_library.dissolve(geos)
                # lfi_extension = self.__gis_library.difference(lfi_extension, [block.get_geometry('minimal_band')])
                if (lfi_extension):
                    block.add_geometry(lfi_extension, 'lfi_extension')            

        if block.get_geometry('lfi_extension') == None and block.has_geometry('lfi'):
            block.add_geometry(self.__gis_library.poligonize(block.get_geometry("lfi")), 'lfi_extension')

    def __complete_consolidation(self, block:Block, corner_area:CornerArea, buffer) -> list[Lot]:
        lines = self.__gis_library.disaggregate(corner_area)
        corner_lots:list[Lot] = []
        for line in lines.get_values():
            buffered_line = self.__gis_library.buffer(Geometry(line), buffer)
            for lot in block.get_lots():
                intersects = self.__gis_library.intersects(lot, buffered_line)
                if (intersects):
                    corner_lots.append(lot)
                    if (lot.get_consolidation() is not None):
                        consolidated = (lot.get_consolidation() and lot.get_consolidation().get_consolidated()) or lot.get_cataloged()
                        lot.get_consolidation().set_consolidated(consolidated)
                        if (consolidated):
                            lot.get_consolidation().set_touched(self.__gis_library.intersects(corner_area.get_extension(), lot.get_consolidation()))                         
        return corner_lots

    def __build_irregular_extension(self, block:Block, corner_area:CornerArea, corner_lots:list[Lot]):

        buffer_intersection = self.__prop['irregular']['buffer_intersection']
        buffer_opossite = self.__prop['irregular']['buffer_opossite']
       
        # return 
        buffer_bottom = self.__prop['irregular']['buffer_bottom']

        lines =  self.__gis_library.disaggregate(corner_area)
        irregular_list = []

        consolidated_lots:list[Lot] = []
        name_consolidated_lots = []
        for lot in corner_lots:
            consolidated = lot.get_consolidation() and lot.get_consolidation().get_consolidated()
            if (consolidated):
                if lot.get_name() not in name_consolidated_lots:
                    consolidated_lots.append(lot)
                    name_consolidated_lots.append(lot.get_name())

        for lot in consolidated_lots:
            borders:list[Lot] = []
            difference_consolidation = self.__gis_library.difference(lot,lot.get_consolidation())
            if difference_consolidation:
                # difference_consolidation = self.__gis_library.difference(difference_consolidation, [block.get_geometry('minimal_band')])
                irregular_list.append(difference_consolidation)


            for line_value in lines.get_values():
                line = Geometry(line_value)
                for border_lot in corner_lots:
                    if (border_lot.get_name() != lot.get_name()
                        and border_lot.get_name() not in name_consolidated_lots
                        and border_lot.get_custom_lot_lines()
                        and self.__gis_library.intersects(line, lot)
                        and self.__gis_library.intersects(line, border_lot)
                        and self.__gis_library.intersects(lot, border_lot) ):
                        
                        borders.append(border_lot)
            if (borders):
                difference = self.__gis_library.difference(lot, lot.get_consolidation())
                list_difference = self.__gis_library.disaggregate_list(difference, 'Polygon')
                for it_difference in list_difference:
                    lines_difference = self.__gis_library.cast(it_difference, 'LineString')
                    for border in borders:
                        points = []
                        intersection = self.__gis_library.intersection(lines_difference, border)
                        if (intersection is not None and self.__gis_library.is_gis_type(intersection, 'LineString')):
                            intersection_offset = self.__gis_library.parallel_offset(intersection, buffer_intersection)
                            if intersection_offset:
                                lines = []
                                other_lines_analize = self.__gis_library.disaggregate_list(self.__gis_library.difference(self.__gis_library.cast(lot, 'LineString'), lot.get_geometry('official_line')))
                                other_lines = []
                                for other_line in other_lines_analize:
                                    if (not self.__gis_library.intersects(other_line, intersection)):
                                        other_lines.append(other_line)
                                if (other_lines):
                                    other = self.__gis_library.merge(other_lines)
                                    lines.append(intersection)
                                    lines.append(intersection_offset)
                                    irregular_lines = []
                                    for line in lines:
                                        points = self.__gis_library.disaggregate_list(line, 'MultiPoint')
                                        if (len(points) == 2):
                                            interpolate_points = [self.__gis_library.interpolate(line, buffer_opossite), self.__gis_library.interpolate(line, buffer_opossite * -1)]
                                            interpolate_line = self.__gis_library.merge(interpolate_points)
                                            point_opposite = self.__gis_library.intersection(other, interpolate_line)
                                            line_max_length = 0
                                            line_max = None
                                            for point in points:
                                                line_temp = self.__gis_library.merge([point, point_opposite])
                                                length = self.__gis_library.length(line_temp)
                                                if (length > line_max_length):
                                                    line_max = line_temp
                                                    line_max_length = length
                                            if (line_max):
                                                irregular_lines.append(line_max)
                                    irregular_point = []
                                    for idx, irregular_line in enumerate(irregular_line):
                                        irregular_line_point = self.__gis_library.disaggregate_list(irregular_line, 'MultiPoint')
                                        irregular_point.append(irregular_line_point[0 if idx == 0 else 1])
                                        irregular_point.append(irregular_line_point[1 if idx == 1 else 0])
                                    irregular = self.__gis_library.merge(irregular_point)
                                    if irregular:
                                        irregular_list.append(irregular)
                                        bottom_line = self.__gis_library.merge(border.get_custom_lot_lines())
                                        bottom_buffer = self.__gis_library.buffer(bottom_line, buffer_bottom, True)
                                        irregular_list.append(bottom_buffer)

        if irregular_list:
            new_irregular_list = []
            for irregular in irregular_list:
                new_irregular_list.extend(self.__gis_library.disaggregate_list(irregular, "Polygon"))
            irregular_geo = self.__gis_library.dissolve(self.__gis_library.snap(new_irregular_list))
            extension = Extension()
            extension.set_value(irregular_geo.get_value())
            extension.set_type_extension("IRRREGULAR")
            corner_area.set_extension(extension)

    def __build_regular_extension(self, block:Block):

        vertices_adjacents = self.__gis_library.find_vertice_and_adjacent(block.get_geometry('lfi'))
        angles = self.__prop['extension']['angles']
        distance_to_parallel = self.__prop['extension']['parallel']['distance']
        scale_x = self.__prop['extension']['parallel']['scale_x']
        scale_y = self.__prop['extension']['parallel']['scale_y']
        for idv, vertice_adjacents in enumerate(vertices_adjacents):
            vertice, adjacents = vertice_adjacents
            angle = self.__gis_library.angle(vertice, adjacents)
            angle_definition = self.__dict_util.find_in_range(angles, angle)
            if (angle_definition):

                distance = angle_definition['distance']

                lines = []
                for adjacent in adjacents:
                    lines.append(self.__gis_library.merge([vertice, adjacent]))

                point_line = [None] * 2
                scaled_parallel_line = [None] * 2
                end_point_line = [None] * 2
                point_parallel = [None] * 2

                for idx, line in enumerate(lines):
                    #find point in line
                    point_line[idx] = self.__gis_library.interpolate(line, distance)
                    #find parallel to line
                    temp_parallel_line = self.__gis_library.parallel_offset(line, distance_to_parallel, 'right' if idx == 0 else 'left')
                    scaled_parallel_line[idx] = self.__gis_library.scale(temp_parallel_line, scale_x, scale_y)
                    points = self.__gis_library.disaggregate(scaled_parallel_line[idx], 'MultiPoint')
                    points.pop_value(1 if idx == 0 else 0)
                    end_point_line[idx] = points

                opposite_vertice = self.__gis_library.intersection(scaled_parallel_line[0], scaled_parallel_line[1])
                # if (opposite_vertice is None):
                #     self.__gis_library.plot([block.get_geometry('lfi'), scaled_parallel_line[0], scaled_parallel_line[1]])
                distance_plus_opposite = self.__gis_library.find_side_rectangle([vertice, opposite_vertice], distance_to_parallel)
                distance_parallel = distance + distance_plus_opposite
               
                for idx, line in enumerate(lines):
                    parallel_line = self.__gis_library.merge([opposite_vertice, end_point_line[idx]])
                    point_parallel[idx] = self.__gis_library.interpolate(parallel_line, distance_parallel)

                # geo_points = [vertice, point_line[0], point_parallel[0], opposite_vertice, point_parallel[1], point_line[1], vertice]
                geo_points = [vertice, point_line[1], point_parallel[1], opposite_vertice, point_parallel[0], point_line[0], vertice]                
                extension = Extension()
                geo = self.__gis_library.merge(geo_points)
                
                valid = self.__validate_extension(geo, block)

                if (valid):
                    geo = self.__gis_library.cast(geo, 'Polygon')
                    geo = self.__gis_library.difference(geo, [block.get_geometry('minimal_band')])
                    extension.add_value(geo.get_value())
                    extension.set_type_extension("REGULAR")
                    block.get_corner_areas()[idv].set_extension(extension)

    def __validate_extension(self, extension:Extension, block:Block) -> bool:
        valid = False
        for lot in block.get_lots():
            touched = self.__gis_library.intersects(lot, extension)
            if (not touched):
                valid = True
            else:
                difference = self.__gis_library.difference(extension, [lot])
                if (difference is not None):
                    valid = True
                else:
                    valid = False
                    cause = {'cause':'extension is inside lot', 'lot':lot.get_name()}
                    break
        return valid
            

