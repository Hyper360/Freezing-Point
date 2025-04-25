import pygame
from math import *
import pickle
from modules.vector import *
from modules.settings import *
from modules.entity import *
import os

# Everything here is for DDA, level building (levelEditor.py) and rendering
pygame.init()

# Block numbers mapped to blocks
COLORS = {
    1: [(80, 20, 20), (40, 10, 10)],  
    2: [(30, 50, 30), (15, 25, 15)],
    3: [(40, 45, 60), (20, 22, 30)],
    4: [(70, 65, 50), (35, 32, 25)],  
    5: [(60, 60, 60), (30, 30, 30)],
    6: [(50, 40, 50), (25, 20, 25)]
}

# generic white block texture
BLOCKTEXTURE = pygame.image.load("res/block/sprite_0.png")
# Enemy Sprites
backSpritePath = os.listdir("res/spritesheets/enemy/back/")
backLeftSpritePath = os.listdir("res/spritesheets/enemy/backleft/")
backRightSpritePath = os.listdir("res/spritesheets/enemy/backright/")
frontSpritePath = os.listdir("res/spritesheets/enemy/front/")
frontLeftSpritePath = os.listdir("res/spritesheets/enemy/frontleft/")
frontRightSpritePath = os.listdir("res/spritesheets/enemy/frontright/")
leftSpritePath = os.listdir("res/spritesheets/enemy/left/")
rightSpritePath = os.listdir("res/spritesheets/enemy/right/")

intelSpritePath = os.listdir("res/spritesheets/intel/")
exclamationSpritePath = os.listdir("res/spritesheets/exclamation/")
decorationSpritePath = os.listdir("res/sprite/")


# Tints an image a certain color. Better than havng multiple block files.
def tintImage(image: pygame.Surface, color: pygame.Color):
    tintedImage = image.copy()  # Copies the image surface
    
    tintSurface = pygame.Surface(tintedImage.get_size(), flags=pygame.SRCALPHA)
    tintSurface.fill(color)

    tintedImage.blit(tintSurface, (0, 0))

    return tintedImage

# Different block to numbers
numOfBlockFiles = len(os.listdir("res/block/"))
BLOCKS = {}

for i in range(numOfBlockFiles):
    BLOCKS[i+1] = pygame.image.load(f"res/block/sprite_{i}.png")

# Image dictionary
flagPresets = {
                0 : {"vDiv" : 1.7, "uDiv" : 1.7, "vMove" : 96},
                1 : {"vDiv" : 1.1, "uDiv" : 1.1, "vMove" : 32},
                2 : {"vDiv" : 1.8, "uDiv" : 1.8, "vMove" : 64},
                3 : {"vDiv" : 2, "uDiv" : 2, "vMove" : 128, "transformLimit" : 1.5},
                4 : {"vDiv" : 2.5, "uDiv" : 2.5, "vMove" : 128, "transformLimit" : 1.5},
                5 : {"vDiv" : 2.5, "uDiv" : 2.5, "vMove" : 128, "transformLimit" : 1.5},
                6 : {"vDiv" : 2.5, "uDiv" : 2.5, "vMove" : 128, "transformLimit" : 1.5},
}
spritePool = {
    "enemyBack" : [pygame.image.load(f"res/spritesheets/enemy/back/{x}") for x in backSpritePath],
    "enemyBackLeft" : [pygame.image.load(f"res/spritesheets/enemy/backleft/{x}") for x in backLeftSpritePath],
    "enemyBackRight" : [pygame.image.load(f"res/spritesheets/enemy/backright/{x}") for x in backRightSpritePath],
    "enemyFront" : [pygame.image.load(f"res/spritesheets/enemy/front/{x}") for x in frontSpritePath],
    "enemyFrontLeft" : [pygame.image.load(f"res/spritesheets/enemy/frontleft/{x}") for x in frontLeftSpritePath],
    "enemyFrontRight" : [pygame.image.load(f"res/spritesheets/enemy/frontright/{x}") for x in frontRightSpritePath],
    "enemyLeft" : [pygame.image.load(f"res/spritesheets/enemy/left/{x}") for x in leftSpritePath],
    "enemyRight" : [pygame.image.load(f"res/spritesheets/enemy/right/{x}") for x in rightSpritePath],
    "intel" : [pygame.image.load(f"res/spritesheets/intel/{x}") for x in intelSpritePath],
    "exclamation" : [pygame.image.load(f"res/spritesheets/exclamation/{x}") for x in exclamationSpritePath]
}
for x in decorationSpritePath:
    spritePool[x.removesuffix(".png")] = [pygame.image.load(f"res/sprite/{x}")]

def displayMiniMap(screen: pygame.Surface, grid, area: pygame.Rect, posV: Vector2F, importantPos : list, enemyPositions : list[Vector2F] = []):
    surface = pygame.Surface((area.w, area.h), flags=pygame.SRCALPHA)
    WIDTHSIZE = area.width / len(grid[0])
    HEIGHTSIZE = area.height / len(grid[0])
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            block = grid[row][col]
            if block == 0:
                pygame.draw.rect(surface, (255, 255, 255, 100), (col * WIDTHSIZE, row * HEIGHTSIZE, WIDTHSIZE, HEIGHTSIZE))
            elif block == 8:
                pygame.draw.rect(surface, (100, 100, 100, 150), (col * WIDTHSIZE, row * HEIGHTSIZE, WIDTHSIZE, HEIGHTSIZE))
            else:
                pygame.draw.rect(surface, (40, 10, 10, 150), (col * WIDTHSIZE, row * HEIGHTSIZE, WIDTHSIZE, HEIGHTSIZE))
    
    for pos in importantPos:
        pygame.draw.circle(surface, (50, 250, 50), vectorMultiply(Vector2F(pos[1], pos[0]), Vector2F(WIDTHSIZE, HEIGHTSIZE)).toTuple(), WIDTHSIZE / 3)
    for pos in enemyPositions:
        pygame.draw.circle(surface, (50, 50, 250), vectorMultiply(Vector2F(pos.x, pos.y), Vector2F(WIDTHSIZE, HEIGHTSIZE)).toTuple(), WIDTHSIZE / 2)

    pygame.draw.circle(surface, (200, 0, 0), vectorMultiply(posV, Vector2F(WIDTHSIZE, HEIGHTSIZE)).toTuple(), WIDTHSIZE / 3)
    screen.blit(surface, (area.x, area.y))



def sortEntities(entities : list[Entity], posV : Vector2F):
    #There should never be a lot of enemies (no more than 20 or 30), so bubblesort will do
    for i in range(len(entities)):
        for j in range(i, len(entities)):
            if (getDistance(posV, entities[i].posV) >= getDistance(posV, entities[j].posV)):
                temp = entities[i]
                entities[i] = entities[j]
                entities[j] = temp
    entities.reverse()


class Grid:
    CURRENTID = 0
    gridDict = {}
    openedDoors = []

    def __init__(self, rows, cols, tilesize):
        self.id = self.CURRENTID

        self.neighbors = {"up": None, "down": None, "left": None, "right": None}

        self.rows = rows
        self.cols = cols
        self.tilesize = tilesize
        self.grid = [[0] * self.cols]
        for r in range(self.rows):
            self.grid.append([0] * self.cols)
        self.enemyPositions = set()
        self.intelPositions = []
        self.spritePositions = {}

        self.gridDict[self.id] = self
        self.portals = {
            "upPortal": Vector2I(self.cols // 2, 0),
            "downPortal": Vector2I(self.cols // 2, self.rows - 1),
            "leftPortal": Vector2I(0, self.rows // 2),
            "rightPortal": Vector2I(self.cols - 1, self.rows // 2),
        }

    def plotIntel(self, row : int, col : int, remove : bool = False):
        if remove == True and (row+0.5, col+0.5) in self.intelPositions:
            self.intelPositions.remove((row+0.5, col+0.5))
            return True
        elif remove == False and self.grid[row][col] == 0:
            if (row+0.5, col+0.5) not in self.intelPositions:
                self.intelPositions.append((row+0.5, col+0.5))
                if len(self.intelPositions) > 3:
                    self.intelPositions.pop(0)
                return True
        return False

    def plotEnemy(self, row : int, col : int, remove : bool = False):
        if remove == True and (row+0.5, col+0.5) in self.enemyPositions:
            self.enemyPositions.remove((row+0.5, col+0.5))
            return True
        elif remove == False and self.grid[row][col] == 0:
            self.enemyPositions.add((row+0.5, col+0.5))
            return True
        return False

    def plotPoint(self, row: int, col: int, tile: int):
        # Placement of tiles
        # Ensures you are not placing points on level connection points
        if (col, row) == self.portals["upPortal"].toTuple() and self.neighbors["up"] != None:
            return False
        elif (col, row) == self.portals["downPortal"].toTuple() and self.neighbors["down"] != None:
            return False
        elif (col, row) == self.portals["leftPortal"].toTuple() and self.neighbors["left"] != None:
            return False
        elif (col, row) == self.portals["rightPortal"].toTuple() and self.neighbors["right"] != None:
            return False
        elif (row+0.5, col+0.5) not in self.enemyPositions:
            self.grid[row][col] = tile

    def plotSprite(self, row : int, col : int, tile : int, remove : bool = False):
        if remove == True and (row, col) in self.spritePositions:
            self.spritePositions.pop((row, col))
            return True
        elif remove == False and self.grid[row][col] == 0:
            if tile in flagPresets:
                e = Entity(f"sprite_{tile}", flags=flagPresets[tile])
            else:
                e = Entity(f"sprite_{tile}")
            e.posV = Vector2F(col, row) 
            self.spritePositions[(row, col)] = e
            return True
        return False

    def loadLevel(self, path: str):
        self.grid = pickle.load(open("levels/level.sob", "rb"))
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def getRow(self, pos : Vector2F, dir : Vector2I):
        curPos = Vector2I().fromVector2F(pos.floor())
        validPositions = []
        tile = self.grid[int(floor(curPos.y))][int(floor(curPos.x))]
        while tile == 0:
            validPositions.append(curPos.toTuple())
            curPos = vectorAdd(curPos, dir)
            try:
                tile = self.grid[int(floor(curPos.y))][int(floor(curPos.x))]
            except:
                tile = -1
        
        return validPositions

    def castRays(self, screen: pygame.Surface, posV: Vector2F, dirV: Vector2F, planeV: Vector2F, enemies : list, alpha: bool):
        # Technique derived from Lodevs DDA raycasting demonstration: https://lodev.org/cgtutor/raycasting.html
        width = screen.get_width()
        zBuf = [0.0 for x in range(width)]
        height = screen.get_height()

        blitTargets = []
        for x in range(width):
            # getting the x position of the camera, the direction of the ray and map position
            cameraX = ((2 * x) / float(width)) - 1
            rayDir = Vector2F(dirV.x + planeV.x * cameraX, dirV.y + planeV.y * cameraX)
            mapPos = Vector2I(posV.x, posV.y)

            sideDist = Vector2F()
            deltaDist = Vector2F()

            if rayDir.x != 0:
                # deltaDist.x = sqrt(1 + ((rayDir.y + 1e-20) ** 2) / ((rayDir.x + 1e-20) ** 2))
                # deltaDist.x = abs(1 + (rayDir.y / rayDir.x))
                deltaDist.x = abs(1 / (rayDir.x + 1e-20)) 
            else:
                deltaDist.x = float("inf")
            if rayDir.y != 0:
                # deltaDist.y = sqrt(1 + ((rayDir.x + 1e-20) ** 2) / ((rayDir.y + 1e-20) ** 2))
                # deltaDist.y = abs(1 + (rayDir.x/rayDir.y)) # Simplified
                deltaDist.y = abs(1 / (rayDir.y + 1e-20)) # Even more simplified
            else:
                deltaDist.y = float("inf")

            perpWallDist = 0

            stepV = Vector2I()

            # Setting up initial side distance
            hit = False
            side = 0
            if rayDir.x < 0:
                stepV.x = -1
                sideDist.x = (posV.x - mapPos.x) * deltaDist.x
            else:
                stepV.x = 1
                sideDist.x = (mapPos.x + 1.0 - posV.x) * deltaDist.x
            if rayDir.y < 0:
                stepV.y = -1
                sideDist.y = (posV.y - mapPos.y) * deltaDist.y
            else:
                stepV.y = 1
                sideDist.y = (mapPos.y + 1.0 - posV.y) * deltaDist.y

            # The raycasting algorithm begins
            curGrid = self
            gridDistance = Vector2I().fromVector2I(mapPos)
            while not hit:
                if sideDist.x < sideDist.y:
                    sideDist.x += deltaDist.x
                    gridDistance.x += stepV.x
                    mapPos.x += stepV.x
                    side = 0
                else:
                    sideDist.y += deltaDist.y
                    gridDistance.y += stepV.y
                    mapPos.y += stepV.y
                    side = 1

                # Moving into another grid
                if mapPos.x < 0:
                    if curGrid.neighbors["left"] != None:
                        curGrid = Grid.gridDict[curGrid.neighbors["left"]]
                        mapPos.x = self.cols - 1
                    else:
                        break
                elif mapPos.x >= self.cols:
                    if curGrid.neighbors["right"] != None:
                        curGrid = Grid.gridDict[curGrid.neighbors["right"]]
                        mapPos.x = 0
                    else:
                        break
                elif mapPos.y < 0:
                    if curGrid.neighbors["up"] != None:
                        curGrid = Grid.gridDict[curGrid.neighbors["up"]]
                        mapPos.y = self.rows - 1
                    else:
                        break
                elif mapPos.y >= self.rows:
                    if curGrid.neighbors["down"] != None:
                        curGrid = Grid.gridDict[curGrid.neighbors["down"]]
                        mapPos.y = 0
                    else:
                        break
                if curGrid.grid[int(floor(mapPos.y))][int(floor(mapPos.x))] != 0:  # Switch x and y if needed
                    hit = True
                    block = curGrid.grid[int(floor(mapPos.y))][int(floor(mapPos.x))]

            if side == 0:
                perpWallDist = abs((gridDistance.x - posV.x + (1.0 - stepV.x) / 2.0) / rayDir.x)
                wallX = posV.y + perpWallDist * rayDir.y
            else:
                perpWallDist = abs((gridDistance.y - posV.y + (1.0 - stepV.y) / 2.0) / rayDir.y)
                wallX = posV.x + perpWallDist * rayDir.x
            
            # Updating the zBuffer, now that we have perpendicular wall distance
            zBuf[x] = perpWallDist

            lineHeight = abs(int(height / (perpWallDist + 1e-10)))

            drawStart = max(0, (-lineHeight / 2) + (height / 2))
            drawEnd = min(height - 1, (lineHeight / 2) + (height / 2))

            if not hit:
                pygame.draw.line(screen, (0, 0, 0, 100), (x, drawStart), (x, drawEnd), 1)
            else:
                texWidth = BLOCKS[block].get_width()
                texHeight = BLOCKS[block].get_height()
                wallX -= floor(wallX)
                texX = int(wallX * float(texWidth))
                if side == 0 and rayDir.x > 0:
                    texX = texWidth - texX - 1
                if side == 1 and rayDir.y < 0:
                    texX = texWidth - texX - 1
                texYStart = int((drawStart - height / 2 + lineHeight / 2) * (texHeight / lineHeight))
                texYStart = max(0, min(texYStart, texHeight - 1))
                texYEnd = int((drawEnd - height / 2 + lineHeight / 2) * (texHeight / lineHeight))
                texYEnd = max(0, min(texYEnd, texHeight - 1))
                textureStrip = pygame.transform.scale(
                    BLOCKS[block].subsurface((texX, texYStart, 1, (texYEnd - texYStart))), (1, drawEnd - drawStart)
                )

                if alpha == True:
                    textureStrip.set_alpha(100)
                if side == 0:
                    blitTargets.append((textureStrip, (x, drawStart)))
                else:
                    blitTargets.append((tintImage(textureStrip, (0, 0, 0, 20)), (x, drawStart)))
        screen.blits(blitTargets)

        self.drawSprites(enemies, zBuf, screen, posV, planeV, dirV)
    
    def drawSprites(self, entities : list, zBuf : list, screen : pygame.Surface, cameraPos : Vector2F, planeV : Vector2F, dirV : Vector2F):
        totalEntities = []
        for intel in self.intelPositions:
            i = Entity("intel", flags={"vDiv" : 1.3,
                                       "uDiv" : 1.3,
                                       "vMove" : 64})
            i.posV = Vector2F(intel[1], intel[0])
            totalEntities.append(i)
        
        totalEntities.extend(entities)
        totalEntities.extend(list(self.spritePositions.values()))
        sortEntities(totalEntities, cameraPos)

        for entity in totalEntities:
            w = screen.get_width()
            h = screen.get_height()


            # Here, we are getting the relative camera position of the sprite 
            relPos = vectorSubtract(entity.posV, cameraPos)
            #Then we transform the sprite with the inverse camera matrix to get the final screen position
            inv = 1.0 / (planeV.x * dirV.y - dirV.x * planeV.y)
            transformV = Vector2F(
                x = inv * (dirV.y * relPos.x - dirV.x * relPos.y),
                y = inv * (-planeV.y * relPos.x + planeV.x * relPos.y)
            ) # Take note how I am treating y as the depth, as usually it would be the z axis, but there is none. Lodev Explains this in his tutorial

            transformV.y = max(transformV.y, 1e-6)

            # Sprite transformations
            if "uDiv" in entity.flags:
                uDiv = entity.flags["uDiv"]
            else:
                uDiv = 1
            if "vDiv" in entity.flags:
                vDiv = entity.flags["vDiv"]
            else:
                vDiv = 1
            if "vMove" in entity.flags:
                vMove = entity.flags["vMove"]
            else:
                vMove = 0
            if "transformLimit" in entity.flags:
                transformLimit = entity.flags["transformLimit"]
            else:
                transformLimit = 1
            vMoveScreen = int(vMove/transformV.y)
            
            # Getting x positon of the sprite
            screenXPos = int(w/2) * (1+transformV.x / transformV.y)

            # Calculate the final height of the sprite on the screen (height will get smaller as distance increases)
            spriteDim = Vector2I()
            drawStartV = Vector2I()
            drawEndV = Vector2I()
            
            # Getting start and ending y pos for the sprite
            spriteDim.y = abs(int(h/transformV.y)) / vDiv
            drawStartV.y = (-spriteDim.y / 2) + (h / 2) + vMoveScreen
            if drawStartV.y < 0: drawStartV.y = 0
            drawEndV.y = (spriteDim.y/ 2) + (h / 2) + vMoveScreen
            if drawEndV.y >= h: drawEndV.y = h - 1

            # Getting start and ending x pos for the sprite
            spriteDim.x = abs(int(w/transformV.y)) / uDiv
            drawStartV.x = (-spriteDim.x / 2) + screenXPos
            if drawStartV.x < 0: drawStartV.x = 0
            drawEndV.x = (spriteDim.x / 2) + screenXPos
            if drawEndV.x >= w: drawEndV.x = w - 1

            # Then we draw each indivisual vertical stripe along the x from start to finish
            # TODO: FIX VECTOR FLOATING POINTS IN Vector2I OBJECT
            for s in range(int(drawStartV.x), int(drawEndV.x)):
                # getting the current frame of the sprite
                spriteName = entity.getSpriteFrame()[0]
                spriteInd = entity.getSpriteFrame()[1]
                spriteImg = spritePool[spriteName][spriteInd]
                
                tex = Vector2I()
                tex.x = int((s - (-spriteDim.x/2 + screenXPos)) * (spriteImg.get_width()/spriteDim.x))

                # We want to make sure each stripe is:
                # In front of the camera, on the screen and within the perpendicular distance
                if (transformV.y > transformLimit and s > 0 and s < w and transformV.y < zBuf[s] and tex.x > 0 and tex.x < spriteImg.get_width()):
                    texSlice = spriteImg.subsurface(tex.x, 0, 1, spriteImg.get_height())
                    scaledSlice = pygame.transform.scale(texSlice, (1,drawEndV.y - drawStartV.y))
                    screen.blit(scaledSlice, (s, drawStartV.y))

                    zBuf[s] = transformV.y

    def castMelee(self, screenWidth: int, posV: Vector2F, dirV: Vector2F, planeV: Vector2F, blockRange: float):
        # Literally same as raytracing but we cast one ray
        x = screenWidth / 2
        cameraX = ((2 * x) / float(screenWidth)) - 1
        rayDir = Vector2F(dirV.x + planeV.x * cameraX, dirV.y + planeV.y * cameraX)
        mapPos = Vector2I(posV.x, posV.y)

        sideDist = Vector2F()
        deltaDist = Vector2F()

        if rayDir.x != 0:
            deltaDist.x = sqrt(1 + ((rayDir.y + 1e-20) ** 2) / ((rayDir.x + 1e-20) ** 2))
            # deltaDist.x = abs(1 + (rayDir.x))
        else:
            deltaDist.x = float("inf")
        if rayDir.y != 0:
            deltaDist.y = sqrt(1 + ((rayDir.x + 1e-20) ** 2) / ((rayDir.y + 1e-20) ** 2))
            # deltaDist.x = abs(1 + (rayDir.y))
        else:
            deltaDist.y = float("inf")

        perpWallDist = 0

        stepV = Vector2I()

        hit = False
        side = 0
        if rayDir.x < 0:
            stepV.x = -1
            sideDist.x = (posV.x - mapPos.x) * deltaDist.x
        else:
            stepV.x = 1
            sideDist.x = (mapPos.x + 1.0 - posV.x) * deltaDist.x
        if rayDir.y < 0:
            stepV.y = -1
            sideDist.y = (posV.y - mapPos.y) * deltaDist.y
        else:
            stepV.y = 1
            sideDist.y = (mapPos.y + 1.0 - posV.y) * deltaDist.y

        curGrid = self
        gridDistance = Vector2I().fromVector2I(mapPos)
        curDist = 0
        while not hit and curDist < blockRange:
            if sideDist.x < sideDist.y:
                sideDist.x += deltaDist.x
                curDist = sideDist.x
                gridDistance.x += stepV.x
                mapPos.x += stepV.x
                side = 0
            else:
                sideDist.y += deltaDist.y
                curDist = sideDist.y
                gridDistance.y += stepV.y
                mapPos.y += stepV.y
                side = 1

            if mapPos.x < 0:
                if curGrid.neighbors["left"] != None:
                    curGrid = Grid.gridDict[curGrid.neighbors["left"]]
                    mapPos.x = self.cols - 1
                else:
                    break
            elif mapPos.x >= self.cols:
                if curGrid.neighbors["right"] != None:
                    curGrid = Grid.gridDict[curGrid.neighbors["right"]]
                    mapPos.x = 0
                else:
                    break
            elif mapPos.y < 0:
                if curGrid.neighbors["up"] != None:
                    curGrid = Grid.gridDict[curGrid.neighbors["up"]]
                    mapPos.y = self.rows - 1
                else:
                    break
            elif mapPos.y >= self.rows:
                if curGrid.neighbors["down"] != None:
                    curGrid = Grid.gridDict[curGrid.neighbors["down"]]
                    mapPos.y = 0
                else:
                    break
            if curGrid.grid[int(floor(mapPos.y))][int(floor(mapPos.x))] == 8:  # Switch x and y if needed
                hit = True
                curGrid.grid[int(floor(mapPos.y))][int(floor(mapPos.x))] = 0
                Grid.openedDoors.append(((int(floor(mapPos.y)), int(floor(mapPos.x))), pygame.time.get_ticks(), self.id))
    
    def updateDoors(self, playerPos : Vector2F):
        i = 0
        playerRow = int(floor(playerPos.y))
        playerCol = int(floor(playerPos.x))
        while i < len(self.openedDoors):
            door = self.openedDoors[i]
            d = getDeltaTime(pygame.time.get_ticks(), door[1])
            if d >= 2.5 and door[0][0] != playerRow and door[0][1] != playerCol:
                    Grid.gridDict[door[2]].grid[door[0][0]][door[0][1]] = 8
                    Grid.openedDoors.pop(i)
                    i -= 1
            i+=1


    def draw(self, screen : pygame.Surface):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != 0:
                    # screen.blit(
                    #     pygame.transform.scale(tintImage(BLOCKTEXTURE, COLORS[self.grid[row][col]][0]), (self.tilesize, self.tilesize)),
                    #     (col * self.tilesize, row * self.tilesize)
                    # )
                    screen.blit(
                        pygame.transform.scale(BLOCKS[self.grid[row][col]], (self.tilesize, self.tilesize)),
                        (col * self.tilesize, row * self.tilesize)
                    )
                pygame.draw.line(screen, "grey", (col * self.tilesize, 0), (col * self.tilesize, self.rows * self.tilesize))
            pygame.draw.line(screen, "grey", (0, row * self.tilesize), (self.cols * self.tilesize, row * self.tilesize))
        
        for enemyPos in self.enemyPositions:
            pygame.draw.circle(screen, (190, 0, 0), (enemyPos[1] * self.tilesize, enemyPos[0] * self.tilesize), self.tilesize/2)
        for intelPos in self.intelPositions:
            pygame.draw.circle(screen, (190, 190, 0), (intelPos[1] * self.tilesize, intelPos[0] * self.tilesize), self.tilesize/4)
        for spritePos in self.spritePositions:
            spriteName = self.spritePositions[spritePos].spriteName
            screen.blit(
                pygame.transform.scale(spritePool[spriteName][0], (self.tilesize, self.tilesize)),
                (spritePos[1] * self.tilesize, spritePos[0] * self.tilesize)
            )