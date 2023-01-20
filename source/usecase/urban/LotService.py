from collections import defaultdict

from numpy import number
from entity.urban.Block import Block
from adapter.urban.LotRepository import LotRepository
from entity.urban.Lot import Lot
from adapter.geo.GisLibrary import GisLibrary
from entity.urban.Rivolta import Rivolta
from entity.urban.Buildability import Buildability
from entity.urban.BuildType import BuildType
from entity.urban.CustomBuildability import CustomBuildability
from entity.urban.CustomLotLine import CustomLotLine
from entity.urban.Leveling import Leveling
from usecase.urban.CustomLotLineService import CustomLotLineService
from usecase.urban.CustomBuildabilityService import CustomBuildabilityService
from usecase.urban.BuildTypeService import BuildTypeService
from usecase.urban.FabricService import FabricService
from entity.geo.Geometry import Geometry
from usecase.core.LogService import LogService
from copy import deepcopy
class LotService:

    def __init__(self,
                 lot_repository:LotRepository,
                 fabric_service:FabricService,
                 build_type_service:BuildTypeService,
                 custom_buildability_service:CustomBuildabilityService,
                 custom_lot_line_service:CustomLotLineService,
                 log_service:LogService,
                 gis_library:GisLibrary,
                 prop:dict) -> None:
        self.__lot_repository = lot_repository
        self.__fabric_service = fabric_service
        self.__gis_library = gis_library
        self.__build_type_service = build_type_service
        self.__custom_buildability_service = custom_buildability_service
        self.__log_service = log_service
        self.__custom_lot_line_service = custom_lot_line_service
        self.__prop = prop

    def build_official_line(self, block:Block):
        if (block.has_geometry('official_line')):
            for lot in block.get_lots():
                official_line = self.__gis_library.intersection(block.get_geometry('official_line'), lot)
                lot.add_geometry(official_line, 'official_line')

    def find_by_blocks(self, blocks:list[Block])->list[Lot]:
        return self.__lot_repository.find_by_blocks(blocks)


    def find_complete_by_block(self, block:Block)->list[Lot]:
        lots = self.__lot_repository.find_by_block(block)
        fabrics = self.__fabric_service.find_by_block(block)
        custom_buildabilities = self.__custom_buildability_service.find_by_block(block)
        custom_lot_lines = self.__custom_lot_line_service.find_by_block(block)

        group_fabric = defaultdict(list)
        for x in fabrics:
            group_fabric[x.get_lot().get_name()].append(x)

        group_build = defaultdict(list[CustomBuildability])
        for x in custom_buildabilities:
            group_build[x.get_lot().get_name()].append(x)

        group_custom_line = defaultdict(list[CustomLotLine])
        for x in custom_lot_lines:
            group_custom_line[x.get_lot().get_name()].append(x)

        for lot in lots:
            lot.set_fabrics(group_fabric[lot.get_name()])

            build_types = list[BuildType]()
            for build_info in lot.get_build_infos():
                build_type = self.__build_type_service.find_by_build_info(build_info)
                if (build_type is not None):
                    build_types.append(build_type)

            lot.set_build_types(build_types)
            for build_type in build_types:
                lot.get_heights().append(build_type.get_height())

            if (lot.get_name() in group_build):
                buildabilities = []
                for custom_build in group_build[lot.get_name()]:
                    build = Buildability(custom_build.get_type_buildability())
                    build.set_values(custom_build.get_values())
                    build.set_from(custom_build.get_from())
                    build.set_to(custom_build.get_to())
                    build.set_build_type(custom_build.get_build_type())
                    buildabilities.append(build)
                lot.set_buildabilities(buildabilities)
            
            if (lot.get_name() in group_custom_line):
                lot.set_custom_lot_lines(group_custom_line[lot.get_name()])
            
            if (lot.get_protection() in self.__prop['cataloged']):
                lot.set_cataloged(True)

        return lots
    
    def analize_heights(self, block:Block):

        heights = set()
        for lot in block.get_lots():
            if (len(lot.get_heights()) > 0 and lot.get_heights()[0] is not None):
                heights.add(lot.get_heights()[0])
        block.set_heights(heights)

    def require_corner_area(self, block:Block):

        found = False

        if (block.get_type_block() in self.__prop['not_valid_block']):
            return found

        for lot in block.get_lots():
            for build_type in lot.get_build_types():
                if (build_type.get_no_corner_area()):
                    found = True
                    break
            if (found):
                break

        return not found
            
    def find_leveling(self, block:Block):

        buffer = self.__prop['enrase']['buffer']
        
        block_lines = self.__gis_library.disaggregate(block.get_geometry('block_lines'))
        for line in block_lines.get_values():
            line_buffer = self.__gis_library.buffer(Geometry(line), buffer)
            lots:list[Lot] = []
            for lot in block.get_lots():
                if (lot.has_geometry("official_line") and self.__gis_library.intersects(line_buffer, lot.get_geometry("official_line"))):
                    lots.append(lot)
                    
            order_lots = self.__order_lots(lots)
            
            consolidated = None
            before = []
            distance_consolidated = 0
            for lot in order_lots:

                if (lot.get_consolidation() and lot.get_consolidation().get_consolidated() and lot.get_consolidation().get_percentage() >= 100):

                    if (len(before) >= 3):
                        for lot_before in before:
                            distance_consolidated += self.__gis_library.length(lot_before.get_geometry("official_line")) 
                        if (distance_consolidated >= 26):
                            before = [before[0], before[len(before) - 1]]

                    previous = None
                    for lot_before in before:
                        self.__add_leveling(lot_before, consolidated, consolidated if not previous else previous, lot, distance_consolidated)
                        
                    before = []
                    consolidated = lot

                else:
                    if (consolidated):
                        before.append(lot)
                    else:
                        before = [lot]

            if before and consolidated:
                self.__add_leveling(before[0], consolidated, consolidated)

    def __add_leveling(self, lot:Lot, 
                             consolidated:Lot,
                             before:Lot,
                             next_consolidated:Lot = None,
                             distance_consolidated:number = None):

        if (not consolidated):
            return
        difference_height = self.__prop['enrase']['difference_height']
        difference_height_consolidated = 0
        max_height = consolidated.get_consolidation().get_max_height()
        min_height = consolidated.get_consolidation().get_max_height()
        if not distance_consolidated:
            distance_consolidated = 0

        if (next_consolidated):

            difference_height_consolidated = abs(consolidated.get_consolidation().get_max_height() - next_consolidated.get_consolidation().get_max_height())
            if consolidated.get_consolidation().get_max_height() > next_consolidated.get_consolidation().get_max_height():
                max_height = consolidated.get_consolidation().get_max_height()
                min_height = next_consolidated.get_consolidation().get_max_height()                
            else:
                min_height = consolidated.get_consolidation().get_max_height()
                max_height = next_consolidated.get_consolidation().get_max_height()      
            

        retire = None
        height = None
        lot_official_line = lot.get_geometry("official_line")
        distance_lot = self.__gis_library.length(lot_official_line)  

        if (difference_height_consolidated <= difference_height and distance_consolidated < 26 ):
            # A1
            height = max_height
            pass
        elif (difference_height_consolidated <= difference_height and distance_consolidated > 26 ):
            # A2
            height = max_height
            retire = 8
        elif (difference_height_consolidated > difference_height and distance_lot <= 10):
            # B1
            height = max_height
            retire = distance_lot - 3
        elif (difference_height_consolidated > difference_height and distance_consolidated > 26 and distance_lot > 10 and distance_lot <= 26):
            # B2
            height = min_height
            retire = distance_lot - (13 if distance_lot * 2/3 > 13 else distance_lot * 2/3)
        elif (difference_height_consolidated > difference_height and distance_consolidated > 26 and distance_lot > 26):
            # B3
            height = min_height
            retire = distance_lot - 3 if distance_lot - 3 <= 8 else 8

        levelings:list[Leveling] = []

        if retire:
            adjoinings:list[Geometry] = [consolidated, next_consolidated, before]
            intersection = None
            adjoining = None
            for adjoining_temp in adjoinings:
                intersection = self.__gis_library.intersection(adjoining_temp.get_geometry("official_line"), lot_official_line)
                if intersection:
                    adjoining = adjoining_temp
                    break

            if self.__gis_library.is_gis_type(intersection, 'Point'):
                points = self.__gis_library.convert(lot_official_line, 'Point')
                points = [points[0], points[len(points) - 1]]
                final_point = points[1] if self.__gis_library.intersects(points[0], intersection) else points[0] 
                line_to_adjoining = self.__gis_library.merge([intersection, final_point])
                point_retire = self.__gis_library.interpolate(line_to_adjoining, retire)
                line_retire = self.__gis_library.merge([intersection, point_retire])
                buffer_line = self.__gis_library.buffer(line_retire, 300)
                retire_lot = self.__gis_library.intersection(lot, buffer_line)
                difference_lot = self.__gis_library.difference(lot,[retire_lot])

                if retire_lot:
                    levelingRetire = Leveling()
                    build_type_copy = deepcopy(lot.get_build_types()[0])
                    main_component = None
                    for keyComponent in build_type_copy.get_components():
                        if 'code' in keyComponent and keyComponent['code'].startswith('cuerpo'):
                            main_component = keyComponent
                            break
                    if main_component:
                        main_component['height'] = height
                        levelingRetire.set_build_type(lot.get_build_types()[0])
                        levelingRetire.set_value(retire_lot.get_value())
                        levelings.append(levelingRetire)

                if difference_lot:
                    levelingDifference = Leveling()
                    levelingDifference.set_build_type(lot.get_build_types()[0])
                    levelingDifference.set_value(difference_lot.get_value())
        else:
            leveling = Leveling()
            leveling.set_build_type(lot.get_build_types()[0])
            leveling.set_value(lot.get_value())

        lot.set_levelings(levelings)

    def __order_lots(self, lots) -> list[Lot]:

        relations = defaultdict(list)
        name_lot = {x.get_name(): x for x in lots}
        for lot in lots:
            for lot2 in lots:
                if lot.get_name() != lot2.get_name() \
                   and self.__gis_library.intersects(lot.get_geometry("official_line"), lot2.get_geometry("official_line")):
                   relations[lot.get_name()].append(lot2.get_name())
        first = ""           
        for key, value in relations.items():
            if (len(value) == 1):
                first = key
                break

        result = [] 
        done = []   
        tmp = first
        loop_check = 0
        while True:
            ls = relations[tmp]
            for e in ls:
                if (tmp != e and e not in done):
                    loop_check = 0
                    done.append(tmp)
                    result.append(name_lot[tmp])
                    tmp = e
                elif (len(ls) == 1):
                    done.append(tmp)
                    result.append(name_lot[tmp])
                elif (len(ls) >= 2):
                    loop_check = loop_check + 1
                    if (loop_check > 50):
                        print("ERROR")
                        ls = []

            if len(done) == len(lots) or len(ls) == 0:
                break

        return result


    def find_rivolta(self, block:Block):
        # Ojo con la asignacion de rivolta para casos de 3 lados altura maxima y 1 lado altura minima.
        # EN ESE CASO NO FUNCIONA

        accept_rivolta = True
        for lot in block.get_lots():
            for build_type in lot.get_build_types():
                if (not build_type.get_accept_rivolta()):
                    accept_rivolta = False
                    break

        if (accept_rivolta and block.get_heights().__len__() >= 2):
            min_height = min(block.get_heights())
            buffer = self.__prop['rivolta']['buffer']
            percentage = self.__prop['rivolta']['percentage']
            lfi = self.__gis_library.disaggregate(block.get_geometry('lfi'))
            block_lines = self.__gis_library.disaggregate(block.get_geometry('block_lines'))
            for line in block_lines.get_values():
                block_line = self.__gis_library.parallel_offset(Geometry(line), buffer)
                block_line_distance =  self.__gis_library.length(block_line)
                height_lots = defaultdict(list)
                height_build_type = defaultdict(BuildType)
                for lot in block.get_lots():
                    if (lot.has_heights()):
                        height_build_type[lot.get_heights()[0]] = lot.get_build_types()[0]
                        if (lot.get_heights()[0] != min_height):
                            intersect = self.__gis_library.intersects(lot, block_line)
                            if (intersect):
                                height_lots[lot.get_heights()[0]].append(lot)

                for height, lots in height_lots.items():
                    dissolve = self.__gis_library.dissolve(lots)
                    intersect_line = self.__gis_library.intersection(dissolve, block_line)
                    intersect_distance = self.__gis_library.length(intersect_line)
                    distance_percentage = intersect_distance / block_line_distance * 100
                    if (distance_percentage >= percentage):
                        found_lfi = self.__gis_library.find_closest_parallel(block_line, lfi, 4, 100)
                        if (found_lfi):
                            scaled_found_lfi = self.__gis_library.scale(found_lfi, 4, 4)
                            buffer_found_lfi = None
                            max_area = 0
                            for sign in [-1, 1]:
                                tmp_buffer_found_lfi = self.__gis_library.buffer(scaled_found_lfi, 400, True, sign)
                                interseccion_tmp = self.__gis_library.intersection(tmp_buffer_found_lfi, block)
                                area = self.__gis_library.get_area(interseccion_tmp)

                                if area > max_area:
                                    max_area = area
                                    buffer_found_lfi = tmp_buffer_found_lfi
                                    
                            for lot in block.get_lots():
                                    
                                if (lot.has_heights()):
                                    intersect = self.__gis_library.intersects(lot, buffer_found_lfi)
                                    list_rivolta = []
                                    area = self.__gis_library.get_area(lot)
                                    intersection = self.__gis_library.intersection(buffer_found_lfi, lot)
                                    intersection_area = self.__gis_library.get_area(intersection)
                                    difference = self.__gis_library.difference(lot, buffer_found_lfi)
                                    difference_area = self.__gis_library.get_area(difference)

                                    if (intersection_area > 0 and area != intersection_area):
                                        rivolta = Rivolta()
                                        rivolta.set_lot(Lot(lot.get_name()))
                                        rivolta.add_value(intersection.get_values())
                                        rivolta.set_height(min_height)
                                        rivolta.set_build_type(height_build_type[rivolta.get_height()])
                                        list_rivolta.append(rivolta)

                                    if (difference_area > 0):
                                        rivolta = Rivolta()
                                        rivolta.set_lot(Lot(lot.get_name()))
                                        rivolta.add_value(difference.get_values())
                                        rivolta.set_height(height)
                                        rivolta.set_build_type(height_build_type[rivolta.get_height()])  
                                        lot.add_geometry(scaled_found_lfi, "division_line")
                                        list_rivolta.append(rivolta)
                                        
                                    lot.set_rivoltas(list_rivolta)                                

    def get_build_definition(self):
        return self.__prop['build']  

    def build_buildability(self, block:Block):

        for lot in block.get_lots():

            if (self.validate_buildability(block, lot)):

                geos = []

                if (lot.get_rivoltas()):
                    for rivolta in lot.get_rivoltas():
                        geos.append((rivolta, rivolta.get_build_type()))
                elif (lot.get_levelings()):
                    for leveling in lot.get_levelings():
                        geos.append((leveling, leveling.get_build_type()))
                elif (lot.get_build_types()):
                    geos.append((lot, lot.get_build_types()[0]))

                lot_builds = []
                for geo, build_type in geos:

                    height_temp = 0

                    for build_component in build_type.get_components():
                        list_substract = []

                        for key, substract in build_component['substract'].items():
                            obj = None

                            if ('geometry' in substract):
                                obj = block.get_geometry(substract['geometry'])
                            elif ('lot_geometry' in substract):
                                obj = lot.get_geometry(substract['lot_geometry'])

                            if obj:

                                if ('poligonize' in substract and obj is not None):
                                    obj = self.__gis_library.cast(obj, 'Polygon')

                                if ('buffer' in substract and obj is not None):
                                    obj = self.__gis_library.buffer(obj, substract['buffer'], True)

                                if ('difference_buffer' in substract and obj is not None):
                                    buffer = self.__gis_library.buffer(obj, substract['difference_buffer'], True, -1)
                                    obj = self.__gis_library.difference(obj, buffer)                                

                            if (obj is not None):
                                list_substract.append(obj)

                        difference = self.__gis_library.cast(self.__gis_library.difference(geo, list_substract), 'MultiPolygon')

                        if (lot.get_name() == "X"):
                            print('stop')
#                            self.__gis_library.plot([lot])
#                            self.__gis_library.plot(list_substract)
#                            self.__gis_library.plot(difference)

                        if (difference is not None):
                            build = Buildability(build_component['code'])
                            build.set_values(difference.get_values())
                            build.set_from(height_temp)
                            build.set_to(height_temp + build_component['height'])
                            build.set_build_type(build_type)
                            height_temp = build.get_to()
                            lot_builds.append(build)

                lot.set_buildabilities(lot_builds)
                if (lot_builds):
                    geos = self.__gis_library.dissolve_union_list(lot_builds)
                    if (geos):
                        area = 0
                        for geo in geos:
                            area = area + self.__gis_library.get_area(geo)
                        lot.set_buildability_area(area)

    def validate_buildability_block(self, block:Block) -> bool:

        valid = False
        not_valid_block = self.__prop['not_valid_block']
        if (block.get_type_block() not in not_valid_block or (block.get_type_block() in not_valid_block and block.get_disposition() is not None)):
            valid = True
        else:
            cause = {'cause':'block not have disposition'}

        if (not valid):
            self.__log_service.add({'message':'discard lot for buildabilities', 'block':block.get_name(), **cause})

        return valid

    def validate_buildability(self, block:Block, lot:Lot) -> bool:

        valid = False
        if (len(lot.get_buildabilities()) == 0 ):
            if (not lot.get_cataloged()):
                # if (not lot.get_irregular()):
                    valid = True
                # else:
                #     cause = {'cause':'is irregular'}
            else:
                cause = {'cause':'is not valid protection'}
        else:
            cause = {'cause':'already have custom buildabilities'}

        if (not valid):
            self.__log_service.add({'message':'discard lot for buildabilities', 'lot':lot.get_name(), **cause})

        return valid
