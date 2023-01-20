from datetime import datetime
from usecase.core.ThreadService import ThreadService

class LogService:

    def __init__(self,
                 thread_service:ThreadService) -> None:
        self.__thread_service = thread_service

    def add(self, param:dict):
        param_string = ""
        if (param != None):
            for key in param:
                param_string = param_string + (' > ' if param_string.__len__() > 0 else '') + key + " : " + param[key]
        log = (self.__get_time() + param_string) 
        self.__thread_service.get('log').append(log)
        print(log)

    def __get_time(self):
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + " > " 