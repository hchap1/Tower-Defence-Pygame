import math
class Vector:
    def __init__(self, x=0, y=0, mode="component"):
        if mode == "component":
            self.x = x
            self.y = y
            self.magnitude = math.sqrt(self.x**2 + self.y**2)
            self.direction = compass_atan(self.x, self.y)
        elif mode == "polar":
            self.magnitude = x
            self.direction = y
            self.x = math.sin(math.radians(self.direction)) * self.magnitude
            self.y = math.cos(math.radians(self.direction)) * self.magnitude

    @classmethod
    def from_polar(cls, magnitude, direction):
        return cls(magnitude, direction, mode="polar")
    
    @classmethod
    def component_from_tuple(cls, data):
        return cls(data[0], data[1], mode="component")

    def normalize(self):
        if self.magnitude == 0: return self
        return Vector(self.x / self.magnitude, self.y / self.magnitude)
    
    def subtract(self, point):
        return Vector(self.x - point.x, self.y - point.y)
    
    def add(self, point):
        return Vector(self.x + point.x, self.y + point.y)
    
    def multiply(self, object):
        if type(object) == Vector:
            return None
        else:
            return Vector(self.x * object, self.y * object)
    
    def get_position(self):
        return [self.x, self.y]
    
    def get_str_position(self):
        return [str(self.x), str(self.y)]
    
    def distance_to(self, point):
        dx = self.x - point.x
        dy = self.y - point.y
        return math.sqrt(dx**2 + dy**2)
    
    def change_length(self, change):
        self.magnitude += change
        self.x = math.sin(math.radians(self.direction)) * self.magnitude
        self.y = math.cos(math.radians(self.direction)) * self.magnitude
    
def compass_atan(x, y):
    if y == 0:
        return 0
    value = math.degrees(math.atan(x/y))
    if x >= 0 and y > 0:
        return value
    if y < 0:
        return 180 + value
    if x < 0 and y > 0:
        return 360 + value