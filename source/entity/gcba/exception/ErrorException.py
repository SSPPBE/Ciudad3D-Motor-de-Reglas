
from entity.gcba.ErrorType import ErrorType
from entity.gcba.ErrorInfo import ErrorInfo

class ErrorException(Exception):

    def __init__(self) -> None:
        self.__errors = []
        pass

    def get_errors(self) -> list[ErrorType]: 
        return self.__errors

    def set_type(self, errors: list[ErrorType]):
        self.__errors = errors       

    def addErrorInfo(self, errorInfo:ErrorInfo):
        self.__errors.append(errorInfo)

    def add(self,  type:ErrorType = None, code:str = None, description:str = None):
        self.__errors.append(ErrorInfo(type, code, description))