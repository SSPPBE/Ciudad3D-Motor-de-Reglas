from entity.geo.GeometryType import GeometryType

class Geometry: 
    """
    Is essentially a vector where each entry in the vector is a set of shapes corresponding to one observation
    An entry may consist of only one shape (like a single polygon) or multiple shapes 
    that are meant to be thought of as one observation
    """

    def __init__(self, value = None, descriptor = None) -> None:
        self.__values = []
        self.__multiple = False
        self.__type = GeometryType.WKT
        self.__geometry = {}
        self.__attribute = {}
        if (descriptor):
            self.set_descriptor(descriptor)
        if (value):
            self.set_values(value)

    def get_type(self) -> GeometryType: 
        return self.__type

    def set_type(self, type: GeometryType):
        self.__type = type

    def set_value(self, value):
        self.set_values(value)

    def get_value(self):
        if (self.__values.__len__() > 0):
            return self.__values[0]
        else:
            return None        

    def add_value(self, value):
        if isinstance(value, list):    
            for val in value:
                self.add_value(val)
        elif isinstance(value, str):
            self.__values.append(value)
            self.__multiple = self.__values.__len__() > 1

    def get_values(self):
        return self.__values

    def set_values(self, value):
        self.__values = []
        self.add_value(value)

    def get_descriptor(self) -> str: 
        return self.__descriptor

    def set_descriptor(self, value: str):
        self.__descriptor = value
    
    def is_multiple(self):
        return self.__multiple

    def add_geometry(self, geometry, descriptor = None):
        if (geometry is not None and descriptor is not None):
            geometry.set_descriptor(descriptor)
            descriptor = geometry.get_descriptor() 
            self.__geometry[descriptor] = geometry

    def has_geometry(self, descriptor):
        return descriptor in self.__geometry

    def get_geometry(self, key) -> any:
        if key in self.__geometry:
            return self.__geometry[key]
        else:
            return None

    def set_attribute(self, key:str, value):
        self.__attribute[key] = value
    
    def get_attribute(self, key) -> any:
        return self.__attribute[key]

    def get_attributes(self) -> dict:
        return  self.__attribute

    def pop_value(self, index:int):
        self.__values.pop(index)
        self.__multiple = self.__values.__len__() > 1
