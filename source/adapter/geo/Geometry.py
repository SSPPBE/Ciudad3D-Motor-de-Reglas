class Geometry:
    def __init__(self) -> None:
        self.__param = dict()
        pass

    def get_name(self) -> str: 
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = value

    def get_framework_value(self):
        return self.__framework_value

    def set_framework_value(self, value):
        self.__framework_value = value     

    def get_param(self) -> dict:
        return self.__param

    def set_param(self, value:dict):
        self.__param = value


        