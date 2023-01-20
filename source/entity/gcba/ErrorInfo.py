from entity.gcba.ErrorType import ErrorType

class ErrorInfo:

    def __init__(self, type:ErrorType = None, code:str = None, description:str = None ):
        self.__type = type
        self.__code = code
        self.__description = description

    def get_type(self) -> ErrorType: 
        return self.__type

    def set_type(self, type: ErrorType):
        self.__type = type

    def get_code(self) -> str: 
        return self.__code

    def set_code(self, code: str):
        self.__code = code

    def get_description(self) -> str: 
        return self.__description

    def set_description(self, description: str):
        self.__description = description
