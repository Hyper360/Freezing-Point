from math import *

# CONSTANTS
TILESIZE = 32
WIDTH = 640
HEIGHT = 640
RESOLUTION = 3.5
HIGHRESOLUTION = 2
REACTIONRATE = 20
READINGPACE = 0.06

# Variables
fps = 60
fullScreen = False
seeThroughWalls = False
highRes = False
miniMap = True
running = True

# Math stuff
rotSpeed = 0.1
MOVESPEED = 3
INVRAD = (cos(-rotSpeed), sin(-rotSpeed))
RAD = (cos(rotSpeed), sin(rotSpeed))
FPRANGE = 0.1

# Helper functions
def floatToVector(v: tuple):
    return (WIDTH * v[0], HEIGHT * v[1])

def getDeltaTime(currentTime : float, pastTime : float) -> float:
    time = (currentTime - pastTime) / 1000
    return time