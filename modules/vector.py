from math import *
from modules.settings import *

# Vector classes for positioning used in the grid.py and main.py files.


# Vector2F and Vector2I have to be "defined" so that Vector2F's and Vector2I's can be passed into the conversion functions
class Vector2F:
    None


class Vector2I:
    None


# Vector 2D Float Class
class Vector2F:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = float(x)
        self.y = float(y)

    def fromVector2F(self, vec: Vector2F):
        # Creates a copy of the passed in Vector2F's values
        self.x = float(vec.x)
        self.y = float(vec.y)
        return self

    def fromVector2I(self, vec: Vector2I):
        # Converts the Vector2I's integers to floats and copies them
        self.x = float(vec.x)
        self.y = float(vec.y)
        return self

    def norm(self):
        # Vector normalization. Returns a new vector with x and y values between 0 and 1
        length = sqrt(self.x ** 2 + self.y ** 2)
        if length == 0:
            return Vector2F(0, 0)  # Return zero vector if input is zero vector
        return Vector2F(self.x / length, self.y / length)


    def __str__(self) -> str:
        # String representation of the Vector
        return f"X: {self.x}, Y:{self.y}"

    def toTuple(self):
        # Returns a Tuple styled version of the vector in (x, y) order
        return (self.x, self.y)
    
    def length(self):
        return sqrt(self.x**2+self.y**2)

    def floor(self):
        return Vector2I(floor(self.x), floor(self.y))


# Vector 2D Integer
# Same as the Vector2F but with integers
class Vector2I:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = int(x)
        self.y = int(y)

    def fromVector2I(self, vec: Vector2I):
        self.x = vec.x
        self.y = vec.y
        return self

    def fromVector2F(self, vec: Vector2F):
        self.x = int(vec.x)
        self.y = int(vec.y)
        return self

    def norm(self):
        if self.x == 0:
            val1 = 1e30
        else:
            val1 = self.x / abs(self.x)
        if self.y == 0:
            val2 = 1e30
        else:
            val2 = self.y / abs(self.y)
        return Vector2I(val1, val2)

    def __str__(self) -> str:
        return f"X: {self.x}, Y:{self.y}"

    def toTuple(self):
        return (self.x, self.y)
    
    def length(self):
        return sqrt(self.x**2, self.y**2)


# vector operation functions
# All of these only work with Vector2F's because why the hell would you do this with integers?

def vectorAdd(v1: Vector2F, v2: Vector2F):
    # Adds the x and y values of 2 vectors and returns them
    return Vector2F(v1.x + v2.x, v1.y + v2.y)


def vectorSubtract(v1: Vector2F, v2: Vector2F):
    # Subtracts the x and y values of 2 vectors and returns them
    return Vector2F(v1.x - v2.x, v1.y - v2.y)


def vectorMultiply(v1: Vector2F, v2: Vector2F):
    # Multiplies the x and y values of 2 vectors and returns them
    return Vector2F(v1.x * v2.x, v1.y * v2.y)


def vectorEquals(v1: Vector2F, v2: Vector2F):
    # Checks if vector floats are ABOUT equal (due to floating point error)
    if abs(v1.x - v2.x) <= FPRANGE and abs(v1.y - v2.y) <= FPRANGE:
        return True
    else:
        return False

def vectorRound(v: Vector2F, decimals : int):
    return Vector2F(round(v.x, decimals), round(v.y, decimals))


def vectorMultiplyF(v: Vector2F, factor: float):
    # Multiplies the values of a vector by a factor
    return Vector2F(v.x * factor, v.y * factor)


def vectorDivideF(v: Vector2F, factor: float):
    # Divides the values of a vector by a factor
    return Vector2F(v.x / factor, v.y / factor)

def vectorDivideV(v1: Vector2F, v2: Vector2F):
    # Divides the values of a vector by another vector
    return Vector2F(v1.x / v2.x, v1.y / v2.y)


def vectorAddF(v: Vector2F, factor: float):
    # Sums the values of a vector by a factor
    return Vector2F(v.x + factor, v.y + factor)

def vectorDot(v1 : Vector2F, v2 :Vector2F):
    return (v1.x*v2.x)+(v1.y*v2.y)


def rotatedPoint(point: Vector2F, radians: float):
    # Returns a new rotated point using radians
    newX = point.x * cos(radians) - point.y * sin(radians)
    newY = point.x * sin(radians) + point.y * cos(radians)

    return Vector2F(newX, newY)


def pointsToRadians(v1: Vector2F, v2: Vector2F):
    # Gets the angle (In radians) between 2 points
    return atan2(v2.y - v1.y, v2.x - v1.x)


# thanks chatGPT :>
def interpolate(p1: Vector2F, p2: Vector2F, t):
    # Interpolate between two points p1 and p2 at position t
    return Vector2F(p1.x + (p2.x - p1.x) * t, p1.y + (p2.y - p1.y) * t)

def getDistance(p1: Vector2F, p2: Vector2F):
    # Gets the euclidean distance between two points
    return ((p1.x - p2.x) ** 2) + ((p1.y - p2.y) ** 2)