# services.py
from atexit import register


class DependencyService:

    def __init__(self):
        self.__factory = {}
        self.__singleton = {}

    def register(self, clazz, function, singleton = True):
        self.register_by_name(clazz.__name__, function, singleton)

    def register_by_name(self, name, function, singleton = True):
        dependency = {}
        dependency['name'] = name
        dependency['singleton'] = singleton
        dependency['function'] = function
        self.__factory[dependency['name']] = dependency

    def get_by_name(self, name, *args, **kwargs):
        dependency = self.__factory.get(name)
        if (dependency == None):
            raise Exception("dependency " + name + " not found")

        if (dependency['singleton'] == True):
            instance = self.__singleton.get(name)
            if (instance):
                return instance
        instance = dependency['function']()   
        if (dependency['singleton'] == True):
            self.__singleton[name] = instance
        return instance

    def get(self, clazz, *args, **kwargs):
        return self.get_by_name(clazz.__name__)


dependencyService = DependencyService()