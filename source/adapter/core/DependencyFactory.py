# services.py
from ezdxf import os
from adapter.core.DependencyService import dependencyService
from adapter.geo.GisLibrary import GisLibrary
from usecase.urban.CustomLineService import CustomLineService
from usecase.output.Ciudad3dService import Ciudad3dService
from usecase.output.FileService import FileService
from usecase.urban.BuildTypeService import BuildTypeService
from usecase.urban.CornerAreaService import CornerAreaService
from usecase.core.DictUtil import DictUtil
from usecase.core.LogService import LogService
from usecase.core.ConfigurationService import ConfigurationService

from adapter.geo.ProcessService import ProcessService
from adapter.core.DbConnector import DbConnector
from usecase.core.ThreadService import ThreadService

from adapter.urban.FabricRepository import FabricRepository
from adapter.urban.FabricDbRepository import FabricDbRepository
from adapter.urban.FabricFileRepository import FabricFileRepository
from usecase.urban.FabricService import FabricService

from adapter.urban.LotRepository import LotRepository
from adapter.urban.LotDbRepository import LotDbRepository
from adapter.urban.LotFileRepository import LotFileRepository
from usecase.urban.LotService import LotService

from adapter.urban.BlockRepository import BlockRepository
from adapter.urban.BlockDbRepository import BlockDbRepository
from adapter.urban.BlockFileRepository import BlockFileRepository
from usecase.urban.BlockService import BlockService

from adapter.urban.RestrictionRepository import RestrictionRepository
from adapter.urban.RestrictionDbRepository import RestrictionDbRepository
from adapter.urban.RestrictionFileRepository import RestrictionFileRepository
from usecase.urban.RestrictionService import RestrictionService

from usecase.urban.CornerAreaService import CornerAreaService

from adapter.urban.ArchaeologicalRiskRepository import ArchaeologicalRiskRepository
from adapter.urban.ArchaeologicalRiskDbRepository import ArchaeologicalRiskDbRepository
from adapter.urban.ArchaeologicalRiskFileRepository import ArchaeologicalRiskFileRepository
from usecase.urban.ArchaeologicalRiskService import ArchaeologicalRiskService

from adapter.urban.CustomBuildabilityRepository import CustomBuildabilityRepository
from adapter.urban.CustomBuildabilityDbRepository import CustomBuildabilityDbRepository
from adapter.urban.CustomBuildabilityFileRepository import CustomBuildabilityFileRepository
from usecase.urban.CustomBuildabilityService import CustomBuildabilityService

from adapter.urban.HydricRiskRepository import HydricRiskRepository
from adapter.urban.HydricRiskDbRepository import HydricRiskDbRepository
from adapter.urban.HydricRiskFileRepository import HydricRiskFileRepository
from usecase.urban.HydricRiskService import HydricRiskService

from adapter.urban.CustomLineRepository import CustomLineRepository
from adapter.urban.CustomLineDbRepository import CustomLineDbRepository
from adapter.urban.CustomLineFileRepository import CustomLineFileRepository
from usecase.urban.CustomLineService import CustomLineService

from adapter.urban.CustomLotLineRepository import CustomLotLineRepository
from adapter.urban.CustomLotLineDbRepository import CustomLotLineDbRepository
from adapter.urban.CustomLotLineFileRepository import CustomLotLineFileRepository
from usecase.urban.CustomLotLineService import CustomLotLineService

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

class DependencyFactory:
    def __init__(self):
        self.__service = dependencyService

    def configuration_service(self):
        return ConfigurationService()

    def process_service(self):
        return ProcessService(self.__service.get(ConfigurationService),
                              self.__service.get(RestrictionService),
                              self.__service.get(ThreadService),
                              self.__service.get(LogService),
                              self.__service.get(BlockService),
                              self.__service.get(GisLibrary),
                              self.__service.get(Ciudad3dService),    
                              self.__service.get(FileService),                                      
                              self.__service.get(ArchaeologicalRiskService),    
                              self.__service.get(HydricRiskService),
                              self.__service.get(ConfigurationService).find_by_type(ProcessService)                                     
                              )

    def gis_library(self):
        return GisLibrary(self.__service.get(LogService))

    def dict_util(self):
        return DictUtil()

    def thread_service(self):
        return ThreadService()

    def log_service(self):
        return LogService(self.__service.get(ThreadService))

    def db_connector_pdi(self):
        return DbConnector(self.__service.get(ConfigurationService).find_by_name("db_pdi"))

    def db_connector_cd3(self):
        return DbConnector(self.__service.get(ConfigurationService).find_by_name("db_cd3"))

    def fabric_db_repository(self):
        return FabricDbRepository(self.__service.get_by_name('db_pdi'))
    def fabric_file_repository(self):
        return FabricFileRepository(self.__service.get(ConfigurationService).find_by_type(FabricFileRepository))
    def fabric_repository(self):
        return FabricRepository(self.__service.get(ThreadService),
                                self.__service.get(FabricDbRepository),
                                self.__service.get(FabricFileRepository),
                                self.__service.get(ConfigurationService).find_by_type(FabricRepository))
    def fabric_service(self):
        return FabricService(self.__service.get(FabricRepository),
                             self.__service.get(GisLibrary),
                             self.__service.get(DictUtil),
                             self.__service.get(ConfigurationService).find_by_type(FabricService))

    def lot_db_repository(self):
        return LotDbRepository(self.__service.get_by_name('db_pdi'))
    def lot_file_repository(self):
        return LotFileRepository(self.__service.get(ConfigurationService).find_by_type(LotFileRepository))
    def lot_repository(self):
        return LotRepository(self.__service.get(ThreadService),
                                self.__service.get(LotDbRepository),
                                self.__service.get(LotFileRepository),
                                self.__service.get(ConfigurationService).find_by_type(LotRepository))
    def lot_service(self):
        return LotService(self.__service.get(LotRepository),
                          self.__service.get(FabricService),
                          self.__service.get(BuildTypeService),
                          self.__service.get(CustomBuildabilityService),
                          self.__service.get(CustomLotLineService),
                          self.__service.get(LogService),
                          self.__service.get(GisLibrary),
                          self.__service.get(ConfigurationService).find_by_type(LotService))

    def block_db_repository(self):
        return BlockDbRepository(self.__service.get_by_name('db_pdi'),
                                 self.__service.get(ThreadService))

    def block_file_repository(self):
        return BlockFileRepository(self.__service.get(ConfigurationService).find_by_type(BlockFileRepository))
    def block_repository(self):
        return BlockRepository(self.__service.get(ThreadService),
                                self.__service.get(BlockDbRepository),
                                self.__service.get(BlockFileRepository),
                                self.__service.get(ConfigurationService).find_by_type(BlockRepository))
    def block_service(self):
        return BlockService(self.__service.get(BlockRepository),
                            self.__service.get(LotService),
                            self.__service.get(GisLibrary),
                            self.__service.get(RestrictionService),
                            self.__service.get(FabricService),
                            self.__service.get(DictUtil),
                            self.__service.get(CornerAreaService),
                            self.__service.get(CustomLineService),    
                            self.__service.get(ThreadService), 
                            self.__service.get(LogService),       
                            self.__service.get(BuildTypeService),             
                            self.__service.get(ConfigurationService).find_by_type(BlockService))

    def restriction_db_repository(self):
        return RestrictionDbRepository(self.__service.get_by_name('db_pdi'))
    def restriction_file_repository(self):
        return RestrictionFileRepository(self.__service.get(ConfigurationService).find_by_type(RestrictionFileRepository))
    def restriction_repository(self):
        return RestrictionRepository(self.__service.get(ThreadService),
                                self.__service.get(RestrictionDbRepository),
                                self.__service.get(RestrictionFileRepository),
                                self.__service.get(ConfigurationService).find_by_type(RestrictionRepository))
    def restriction_service(self):
        return RestrictionService(self.__service.get(RestrictionRepository),
                                  self.__service.get(GisLibrary),
                                  self.__service.get(LogService),
                                  self.__service.get(ConfigurationService).find_by_type(RestrictionService))

    def corner_area_service(self):
        return CornerAreaService( self.__service.get(GisLibrary),
                                  self.__service.get(LotService),
                                  self.__service.get(DictUtil), 
                                  self.__service.get(ConfigurationService).find_by_type(CornerAreaService))

    def build_type_service(self):
        return BuildTypeService( self.__service.get(ConfigurationService).find_by_type(BuildTypeService))   

    def ciudad3d_service(self):
        return Ciudad3dService( self.__service.get(GisLibrary),
                                self.__service.get(FileService),
                                self.__service.get_by_name('db_cd3'),
                                self.__service.get(ConfigurationService).find_by_type(Ciudad3dService))  

    def file_service(self):
        return FileService( self.__service.get(GisLibrary),
                            self.__service.get(ConfigurationService).find_by_type(FileService))   

    def archaeologicalRisk_db_repository(self):
        return ArchaeologicalRiskDbRepository(self.__service.get_by_name('db_pdi'))
    def archaeologicalRisk_file_repository(self):
        return ArchaeologicalRiskFileRepository(self.__service.get(ConfigurationService).find_by_type(ArchaeologicalRiskFileRepository))
    def archaeologicalRisk_repository(self):
        return ArchaeologicalRiskRepository(self.__service.get(ThreadService),
                                self.__service.get(ArchaeologicalRiskDbRepository),
                                self.__service.get(ArchaeologicalRiskFileRepository),
                                self.__service.get(ConfigurationService).find_by_type(ArchaeologicalRiskRepository))
    def archaeologicalRisk_service(self):
        return ArchaeologicalRiskService(self.__service.get(ArchaeologicalRiskRepository))

    def customBuildability_db_repository(self):
        return CustomBuildabilityDbRepository(self.__service.get_by_name('db_pdi'))
    def customBuildability_file_repository(self):
        return CustomBuildabilityFileRepository(self.__service.get(ConfigurationService).find_by_type(CustomBuildabilityFileRepository))
    def customBuildability_repository(self):
        return CustomBuildabilityRepository(self.__service.get(ThreadService),
                                self.__service.get(CustomBuildabilityDbRepository),
                                self.__service.get(CustomBuildabilityFileRepository),
                                self.__service.get(ConfigurationService).find_by_type(CustomBuildabilityRepository))
    def customBuildability_service(self):
        return CustomBuildabilityService(self.__service.get(CustomBuildabilityRepository))        

    def hydric_risk_db_repository(self):
        return HydricRiskDbRepository(self.__service.get_by_name('db_pdi'))
    def hydric_risk_file_repository(self):
        return HydricRiskFileRepository(self.__service.get(ConfigurationService).find_by_type(HydricRiskFileRepository))
    def hydric_risk_repository(self):
        return HydricRiskRepository(self.__service.get(ThreadService),
                                self.__service.get(HydricRiskDbRepository),
                                self.__service.get(HydricRiskFileRepository),
                                self.__service.get(ConfigurationService).find_by_type(HydricRiskRepository))
    def hydric_risk_service(self):
        return HydricRiskService(self.__service.get(HydricRiskRepository))

    def custom_line_db_repository(self):
        return CustomLineDbRepository(self.__service.get_by_name('db_pdi'))
    def custom_line_file_repository(self):
        return CustomLineFileRepository(self.__service.get(ConfigurationService).find_by_type(CustomLineFileRepository))
    def custom_line_repository(self):
        return CustomLineRepository(self.__service.get(ThreadService),
                                self.__service.get(CustomLineDbRepository),
                                self.__service.get(CustomLineFileRepository),
                                self.__service.get(ConfigurationService).find_by_type(CustomLineRepository))
    def custom_line_service(self):
        return CustomLineService(self.__service.get(CustomLineRepository),
                                 self.__service.get(GisLibrary))

    def custom_lot_line_db_repository(self):
        return CustomLotLineDbRepository(self.__service.get_by_name('db_pdi'))
    def custom_lot_line_file_repository(self):
        return CustomLotLineFileRepository(self.__service.get(ConfigurationService).find_by_type(CustomLotLineFileRepository))
    def custom_lot_line_repository(self):
        return CustomLotLineRepository(self.__service.get(ThreadService),
                                self.__service.get(CustomLotLineDbRepository),
                                self.__service.get(CustomLotLineFileRepository),
                                self.__service.get(ConfigurationService).find_by_type(CustomLotLineRepository))
    def custom_lot_line_service(self):
        return CustomLotLineService(self.__service.get(CustomLotLineRepository),
                                self.__service.get(GisLibrary))


    def start(self):
        '''
        Main start. Inyects singletons. Set up IoC
        '''

        self.__service.register(ConfigurationService, self.configuration_service)

        self.__service.register_by_name("db_pdi", self.db_connector_pdi)
        self.__service.register_by_name("db_cd3", self.db_connector_cd3)

        self.__service.register(ThreadService, self.thread_service)
        self.__service.register(GisLibrary, self.gis_library)
        self.__service.register(LogService, self.log_service)
        self.__service.register(DictUtil, self.dict_util)

        self.__service.register(Ciudad3dService, self.ciudad3d_service)
        self.__service.register(FileService, self.file_service)

        self.__service.register(ProcessService, self.process_service)

        self.__service.register(FabricDbRepository, self.fabric_db_repository)
        self.__service.register(FabricFileRepository, self.fabric_file_repository)
        self.__service.register(FabricRepository, self.fabric_repository)        
        self.__service.register(FabricService, self.fabric_service)

        self.__service.register(LotDbRepository, self.lot_db_repository)
        self.__service.register(LotFileRepository, self.lot_file_repository)
        self.__service.register(LotRepository, self.lot_repository)        
        self.__service.register(LotService, self.lot_service) 

        self.__service.register(BlockDbRepository, self.block_db_repository)
        self.__service.register(BlockFileRepository, self.block_file_repository)
        self.__service.register(BlockRepository, self.block_repository)        
        self.__service.register(BlockService, self.block_service) 

        self.__service.register(RestrictionDbRepository, self.restriction_db_repository)
        self.__service.register(RestrictionFileRepository, self.restriction_file_repository)
        self.__service.register(RestrictionRepository, self.restriction_repository)        
        self.__service.register(RestrictionService, self.restriction_service) 

        self.__service.register(CornerAreaService, self.corner_area_service) 
        self.__service.register(BuildTypeService, self.build_type_service) 

        self.__service.register(ArchaeologicalRiskDbRepository, self.archaeologicalRisk_db_repository)
        self.__service.register(ArchaeologicalRiskFileRepository, self.archaeologicalRisk_file_repository)
        self.__service.register(ArchaeologicalRiskRepository, self.archaeologicalRisk_repository)        
        self.__service.register(ArchaeologicalRiskService, self.archaeologicalRisk_service) 

        self.__service.register(CustomBuildabilityDbRepository, self.customBuildability_db_repository)
        self.__service.register(CustomBuildabilityFileRepository, self.customBuildability_file_repository)
        self.__service.register(CustomBuildabilityRepository, self.customBuildability_repository)        
        self.__service.register(CustomBuildabilityService, self.customBuildability_service) 

        self.__service.register(HydricRiskDbRepository, self.hydric_risk_db_repository)
        self.__service.register(HydricRiskFileRepository, self.hydric_risk_file_repository)
        self.__service.register(HydricRiskRepository, self.hydric_risk_repository)        
        self.__service.register(HydricRiskService, self.hydric_risk_service) 

        self.__service.register(CustomLineDbRepository, self.custom_line_db_repository)
        self.__service.register(CustomLineFileRepository, self.custom_line_file_repository)
        self.__service.register(CustomLineRepository, self.custom_line_repository)        
        self.__service.register(CustomLineService, self.custom_line_service) 

        self.__service.register(CustomLotLineDbRepository, self.custom_lot_line_db_repository)
        self.__service.register(CustomLotLineFileRepository, self.custom_lot_line_file_repository)
        self.__service.register(CustomLotLineRepository, self.custom_lot_line_repository)        
        self.__service.register(CustomLotLineService, self.custom_lot_line_service) 

        self.ready()
    
    def ready(self):
        '''
        Function to start after IoC is established
        '''
        
        # verify if cron is configured in environment vars
        cron = os.getenv("CRON_JOB") 
        if (cron):
            sched = BackgroundScheduler()
            sched.add_job(self.job_func, CronTrigger.from_crontab(cron))
            sched.start()

        # verify if folders exists. If not, it'll be created
        root = os.getenv("ROOT_FOLDER")
        media = os.getenv("MEDIA")
        tiles = os.getenv("TILES")

        if (not os.path.exists(root + '/' + media)):
            os.makedirs(root + '/' + media)

        if (not os.path.exists(root + '/' + tiles)):
            os.makedirs(root + '/' + tiles)

        # Starts connections
        thread_service:ThreadService = self.__service.get(ThreadService)
        thread_service.set("connector", "db")
        self.__service.get_by_name('db_pdi')
        self.__service.get_by_name('db_cd3')

        # find all blocks
        block_service:BlockService = self.__service.get(BlockService)
        block_service.find_all_blocks()

    def job_func(self):
        process:ProcessService = self.__service.get(ProcessService)
        process.execute([], [], True, "cd3")
