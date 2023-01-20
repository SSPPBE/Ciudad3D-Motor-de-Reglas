import os
import yaml 
import re

class ConfigurationService():

    def __init__(self):
        name = os.getenv('CONFIGURATION_FOLDER') + "/configuration.yml"
        self.__conf = yaml.load(open(name))
        self.__prop = {}
        self.to_properties(self.__conf, self.__prop, "")

    def get_prop(self) -> dict:
        return self.__prop

    def get_conf(self) -> dict:
        return self.__conf

    def find_by_type(self, clazz) -> any:
        name = clazz.__name__
        key = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        if (key in self.__conf):
            return self.__conf[key]
        else:
            return {}

    def find_by_name(self, name) -> any:
        if (name in self.__conf):
            return self.__conf[name]
        else:
            return {}

    def to_properties(self, value, prop:dict, ant:str):
        if (value == None):
            return

        if isinstance(value, dict):
            for key in value:
                var = ant + ("." if ant != "" else "") + key
                self.to_properties(value[key], prop, var)
        elif isinstance(value, list):
            for idx, x in enumerate(value):
                var = ant + "[" + str(idx) + "]"
                self.to_properties(x, prop, var)
        else:      
            prop[ant] = value

