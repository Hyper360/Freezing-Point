import pygame
from modules.vector import *
from modules.settings import *
import copy

class Entity:
    def __init__(self, spriteName : str = "", spriteLen : int = 1, flags : dict[str,int] = {}):
        self.posV = Vector2F(1, 1)
        self.lastState = None
        self.imgInd = 0
        self.spriteLen = spriteLen
        self.spriteName = spriteName
        self.flags = flags

    def getSpriteFrame(self) -> tuple[str, int]:
        return (self.spriteName, self.imgInd)
    
    def capturePos(self):
        self.lastState = copy.deepcopy(self)
        self.lastState.lastState = None

class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.dirV = Vector2F(-1.0, 0.0)
        self.planeV = Vector2F(0, -0.66)
        self.bullets = []
        self.lastState = None

        # For intel check event
        self.intelTaken = 0
        self.intelKeys = []
        self.intelKeyCounter = 0
        self.quickTime = False


class Enemy(Entity):
    def __init__(self, spriteName : str = "", spriteLen : int = 1):
        Entity.__init__(self, spriteName, spriteLen)
        # Spritesheet is using the sliding window method
        self.path = []
        self.speed = 1
        self.lastFrame = pygame.time.get_ticks()
        self.dirV = Vector2F(0, 0)
        
        # Enemy tracking
        self.suspicion = 0
        self.sight = False
    
    def getTarget(self):
        return self.path[-1]

    def changeSpriteDirection(self, playerV : Vector2F):
        # Getting the sprite direction.
        dirToEnemy = vectorSubtract(playerV , self.posV).norm()
        enemyDir = self.dirV.norm()

        # Relative angle between enemyDir and -dirToEnemy
        dx = -dirToEnemy.x
        dy = -dirToEnemy.y

        angle = atan2(enemyDir.y, enemyDir.x) - atan2(dy, dx)
        angle = degrees(angle) % 360  # Normalizing angle to [0, 360)
        if angle >= 337.5 or angle < 22.5:
            self.spriteName = "enemyBack"
        elif angle < 67.5:
            self.spriteName = "enemyBackRight"
        elif angle < 112.5:
            self.spriteName = "enemyRight"
        elif angle < 157.5:
            self.spriteName = "enemyFrontRight"
        elif angle < 202.5:
            self.spriteName = "enemyFront"
        elif angle < 247.5:
            self.spriteName = "enemyFrontLeft"
        elif angle < 292.5:
            self.spriteName = "enemyLeft"
        else:
            self.spriteName = "enemyBackLeft"

    def followPath(self, deltaTime : float):
        if self.sight:
            self.speed = 2
        else:
            self.speed = 1
        if len(self.path) > 0:
            target = self.getTarget()
            self.dirV = Vector2F(0, 0)
            if self.posV.x < target.x:
                self.posV.x += self.speed * deltaTime
                self.dirV.x = 1
            if self.posV.x > target.x:
                self.posV.x -= self.speed * deltaTime
                self.dirV.x = -1

            if self.posV.y < target.y:
                self.posV.y += self.speed * deltaTime
                self.dirV.y = 1
            if self.posV.y > target.y:
                self.posV.y -= self.speed * deltaTime
                self.dirV.y = -1
            if vectorEquals(self.posV, target):
                self.path.pop(-1)
    
    def update(self, deltaTime : float):
        if (getDeltaTime(pygame.time.get_ticks(), self.lastFrame) >= 0.25):
            self.imgInd = (self.imgInd + 1) % self.spriteLen
            self.lastFrame = pygame.time.get_ticks()
        if not self.sight or self.suspicion >= 30:
            self.followPath(deltaTime)
        
