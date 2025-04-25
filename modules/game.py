import pygame
import pickle
import random
import datetime

from modules.settings import *
from modules.vector import *
from modules.grid import Grid, displayMiniMap, spritePool
from modules.astar import *
from modules.entity import *
from modules.essentials import *

import pygame

keys = {
    'A': [pygame.K_a, None],
    'B': [pygame.K_b, None],
    'C': [pygame.K_c, None],
    'D': [pygame.K_d, None],
    'E': [pygame.K_e, None],
    'F': [pygame.K_f, None],
    'G': [pygame.K_g, None],
    'H': [pygame.K_h, None],
    'I': [pygame.K_i, None],
    'J': [pygame.K_j, None],
    'K': [pygame.K_k, None],
    'L': [pygame.K_l, None],
    'M': [pygame.K_m, None],
    'N': [pygame.K_n, None],
    'O': [pygame.K_o, None],
    'P': [pygame.K_p, None],
    'Q': [pygame.K_q, None],
    'R': [pygame.K_r, None],
    'S': [pygame.K_s, None],
    'T': [pygame.K_t, None],
    'U': [pygame.K_u, None],
    'V': [pygame.K_v, None],
    'W': [pygame.K_w, None],
    'X': [pygame.K_x, None],
    'Y': [pygame.K_y, None],
    'Z': [pygame.K_z, None],
}

for key in keys:
    keys[key][1] = pygame.image.load(f"res/spritesheets/letters/sprite_{key}.png")

class Game:
    def __init__(self, restart : bool = False):
        # Screen, gameclock etc...
        if restart:
            self.screen = pygame.display.get_surface()
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.HWACCEL|pygame.SCALED)
        self.defaultFont = pygame.font.Font("res/fonts/BebasNeue-Regular.ttf", 24)
        self.fpsFont = pygame.font.Font("res/fonts/Orbitron-Variable.ttf", 15)
        self.resultFont = pygame.font.Font("res/fonts/Orbitron-Variable.ttf", 32)
        self.title = self.defaultFont.render("FREEZING POINT", False, (255, 255, 255))
        self.clock = pygame.time.Clock()
        self.skyBox = pygame.transform.smoothscale(pygame.image.load("res/skybox.jpg"), (WIDTH, HEIGHT))
        self.seeThroughWalls = False
        self.highRes = False
        # Current screen saves the last render of the screen BTW
        self.currentScreen = pygame.Surface((WIDTH / RESOLUTION, HEIGHT / RESOLUTION), flags=pygame.SRCALPHA | pygame.HWACCEL)
        self.state = 0
        self.running = True
        self.restart = False

        # Player object and timing
        self.p = Player()
        self.time = 0

        # Dialogue controller
        self.dia = DialogueController("res/dialogue/intro-dialogue.txt", "res/fonts/Orbitron-Variable.ttf", 15)

        #Music controller
        self.musicPlayer = MusicController("res/sound/music/")
        self.musicPlayer.setVolume(100)
        self.musicPlayer.play("introMusic")

        # Sound effects
        self.quickTime = pygame.mixer.Sound("res/sound/effects/quicktimesuccess.mp3")

        # Initial Grid object
        Grid.gridDict = pickle.load(open("levels/level0.sob", "rb"))
        self.grid = Grid.gridDict[0]
        # Cast initial rays so the screen does not start black
        self.grid.castRays(self.currentScreen, self.p.posV, self.p.dirV, self.p.planeV, [], self.seeThroughWalls)

        # Enemies, timing mechnaisms for spritesheets etc...
        self.prevTime = pygame.time.get_ticks()
        self.curTime = pygame.time.get_ticks()
        self.enemies = {}
        self.loadEnemies()

    def loadEnemies(self):
        if self.grid.id not in self.enemies:
            self.enemies[self.grid.id] = []
            for pos in self.grid.enemyPositions:
                e = Enemy("enemyBack", len(spritePool["enemyBack"]))
                e.posV = Vector2F(pos[1], pos[0])
                self.enemies[self.grid.id].append(e)

    def checkRoom(self):
        # This function checks whether the player has entered a new room
        if self.p.posV.y < 0 or self.p.posV.x < 0 or self.p.posV.y >= self.grid.rows or self.p.posV.x >= self.grid.cols:
            if self.p.posV.x < 0:
                if self.grid.neighbors["left"] != None:
                    self.grid = self.grid.gridDict[self.grid.neighbors["left"]]
                    self.p.posV.x += self.grid.cols
                    self.loadEnemies()
            elif self.p.posV.y < 0:
                if self.grid.neighbors["up"] != None:
                    self.grid = self.grid.gridDict[self.grid.neighbors["up"]]
                    self.p.posV.y += self.grid.rows
                    self.loadEnemies()
            elif self.p.posV.x > self.grid.cols - 1:
                if self.grid.neighbors["right"] != None:
                    self.grid = self.grid.gridDict[self.grid.neighbors["right"]]
                    self.p.posV.x -= self.grid.cols
                    self.loadEnemies()
            elif self.p.posV.y > self.grid.rows - 1:
                if self.grid.neighbors["down"] != None:
                    self.grid = self.grid.gridDict[self.grid.neighbors["down"]]
                    self.p.posV.y -= self.grid.rows
                    self.loadEnemies()
    
    def movePlayerVector(self, deltaTime : float):
        key = pygame.key.get_pressed()

        finalSpeed = (MOVESPEED * deltaTime)
        # ROTATION: rotating the angle of the players view (in radians)
        if key[pygame.K_RIGHT]:
            oldX = self.p.dirV.x
            self.p.dirV.x = self.p.dirV.x * RAD[0] - self.p.dirV.y * RAD[1]
            self.p.dirV.y = oldX * RAD[1] + self.p.dirV.y * RAD[0]

            oldPlaneX = self.p.planeV.x
            self.p.planeV.x = self.p.planeV.x * RAD[0] - self.p.planeV.y * RAD[1]
            self.p.planeV.y = oldPlaneX * RAD[1] + self.p.planeV.y * RAD[0]

        elif key[pygame.K_LEFT]:
            oldX = self.p.dirV.x
            self.p.dirV.x = self.p.dirV.x * INVRAD[0] - self.p.dirV.y * INVRAD[1]
            self.p.dirV.y = oldX * INVRAD[1] + self.p.dirV.y * INVRAD[0]

            oldPlaneX = self.p.planeV.x
            self.p.planeV.x = self.p.planeV.x * INVRAD[0] - self.p.planeV.y * INVRAD[1]
            self.p.planeV.y = oldPlaneX * INVRAD[1] + self.p.planeV.y * INVRAD[0]

        # MOVEMENT: Moving the player itself 
        if key[pygame.K_UP]:
            self.p.posV.x += self.p.dirV.x * finalSpeed
            self.checkRoom()
            if self.grid.grid[int(self.p.posV.y)][int(self.p.posV.x)] != 0:
                self.p.posV.x -= self.p.dirV.x * finalSpeed
            self.p.posV.y += self.p.dirV.y * finalSpeed
            self.checkRoom()
            if self.grid.grid[int(self.p.posV.y)][int(self.p.posV.x)] != 0:
                self.p.posV.y -= self.p.dirV.y * finalSpeed

        if key[pygame.K_DOWN]:
            self.p.posV.x -= self.p.dirV.x * finalSpeed
            self.checkRoom()
            if self.grid.grid[int(self.p.posV.y)][int(self.p.posV.x)] != 0:
                self.p.posV.x += self.p.dirV.x * finalSpeed
            self.p.posV.y -= self.p.dirV.y * finalSpeed
            self.checkRoom()
            if self.grid.grid[int(self.p.posV.y)][int(self.p.posV.x)] != 0:
                self.p.posV.y += self.p.dirV.y * finalSpeed

    def run(self):
        global miniMap, fps
        mousePos = Vector2F(*pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Set program state to one, exit program
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Toggling fullscreen
                    pygame.display.toggle_fullscreen()
                
                if event.key == pygame.K_SPACE:
                    self.grid.castMelee(self.currentScreen.get_width(), self.p.posV, self.p.dirV, self.p.planeV, 2.5)
                    self.currentScreen.fill((0, 0, 0, 0))
                
                key = pygame.key.get_pressed()
                if key[pygame.K_LCTRL]:
                    if event.key == pygame.K_z:
                        # Toggle translucent walls
                        self.seeThroughWalls = not self.seeThroughWalls

                    if event.key == pygame.K_s:
                        # Checking if the player has a savestate. if it does, revert back to it
                        if self.p.lastState != None:
                            self.p = self.p.lastState
                            for enemy in self.enemies[self.grid.id]:
                                enemy = enemy.lastState

                    if event.key == pygame.K_r:
                        # High res mode or low res mode
                        if self.highRes:
                            self.currentScreen = pygame.Surface(
                                (WIDTH / RESOLUTION, HEIGHT / RESOLUTION), flags=pygame.SRCALPHA | pygame.HWACCEL
                            )
                            fps = 60
                        else:
                            self.currentScreen = pygame.Surface((WIDTH / HIGHRESOLUTION, HEIGHT / HIGHRESOLUTION), flags=pygame.SRCALPHA | pygame.HWACCEL)
                            fps = 30

                        self.highRes = not self.highRes
                    if event.key == pygame.K_m:
                        miniMap = not miniMap

        # Timing for spritesheets, copies etc go here:
        deltaTime = getDeltaTime(pygame.time.get_ticks(), self.curTime)
        self.time += deltaTime
        self.curTime = pygame.time.get_ticks()
        timeDiff = getDeltaTime(self.curTime, self.prevTime)
        if timeDiff >= 10:
            self.p.capturePos()
            for enemy in self.enemies[self.grid.id]:
                enemy.capturePos()
            self.prevTime = self.curTime

        key = pygame.key.get_pressed()
        for enemy in self.enemies[self.grid.id]:
            if len(enemy.path) == 0:
                targetCol = random.randrange(0, self.grid.cols)
                targetRow = random.randrange(0, self.grid.rows)
                if self.grid.grid[targetRow][targetCol] == 0:
                    enemy.path = aStar(self.grid.grid, enemy.posV, 
                                                Vector2F(targetCol, targetRow))
            enemy.changeSpriteDirection(self.p.posV)
            enemy.update(deltaTime)

        if not self.p.quickTime:
            self.movePlayerVector(deltaTime)

            for i, intel in enumerate(self.grid.intelPositions):
                if getDistance(self.p.posV, Vector2F(intel[1], intel[0])) < 1:
                    self.grid.intelPositions.pop(i)
                    
                    # Initiate quick time event
                    self.p.intelKeys = random.choices(list(keys.keys()), k=5)
                    self.p.quickTime = True
        elif self.p.quickTime:
            if key[keys[self.p.intelKeys[self.p.intelKeyCounter]][0]]: # Checking if the correct key was pressed in the correct order
                self.p.intelKeyCounter += 1
                self.quickTime.play()
            if self.p.intelKeyCounter >= 5:
                self.p.intelKeys = []
                self.p.intelKeyCounter = 0
                self.p.quickTime = False

                self.p.intelTaken += 1
                self.dia.load(f"res/dialogue/Intel{self.p.intelTaken}-dialogue.txt")
                self.dia.makeActive()
            if self.p.intelTaken == 8:
                self.state = 3
                self.musicPlayer.stop()
                self.recordTime("WIN0")
                
        for enemy in self.enemies[self.grid.id]:
            if len(enemy.path) > 0:
                resVec = vectorSubtract(enemy.getTarget(), enemy.posV)
                unitVec = vectorDivideF(resVec, resVec.length())
                dirVec = vectorRound(unitVec, 0)

                if enemy.suspicion >= 30:
                    enemy.path = aStar(self.grid.grid, enemy.posV, self.p.posV)
                if self.p.posV.floor().toTuple() in self.grid.getRow(enemy.posV, dirVec):
                    enemy.suspicion = min(enemy.suspicion + (REACTIONRATE/fps), 100)
                    enemy.sight = True
                else:
                    enemy.suspicion = max(enemy.suspicion - ((REACTIONRATE/fps)/4), 0)
                    enemy.sight = False
        
        self.grid.updateDoors(self.p.posV)

        self.currentScreen.fill((0, 0, 0, 0))
        self.grid.castRays(self.currentScreen, self.p.posV, self.p.dirV, self.p.planeV, self.enemies[self.grid.id], self.seeThroughWalls)

        self.screen.fill((50, 50, 50), (0, 0, WIDTH, HEIGHT/2))
        self.screen.fill((70, 70, 70), (0, HEIGHT/2, WIDTH, HEIGHT/2))

        self.screen.blit(pygame.transform.scale(self.currentScreen, (WIDTH, HEIGHT)), (0, 0))

        self.screen.blit(self.fpsFont.render(f"FPS: {round(self.clock.get_fps(), 2)}", True, "red"), (0, 0))
        self.screen.blit(self.defaultFont.render(f"TIME: {floor(self.time/60)}:{floor(self.time%60)}", True, "red"), (0, 30))
        
        ratio = max([e.suspicion for e in self.enemies[self.grid.id]])/100
        excDim = spritePool["exclamation"][2].get_width()
        if ratio > 0:
            excText = self.defaultFont.render(f"ALERT: {round(ratio*100, 1)}% DETECTION", True, (255, 255, 255, 100))
            if ratio < 0.3 and ratio > 0:
                if self.musicPlayer.getPlaying() != "bgsus1": self.musicPlayer.play("bgsus1")
                self.screen.blit(spritePool["exclamation"][2],
                                ((WIDTH/2) - (excDim/2), (HEIGHT/2) - (excDim/2)))
            if ratio >= 0.3 and ratio < 0.6:
                if self.musicPlayer.getPlaying() != "bgsus2": self.musicPlayer.play("bgsus2")
                self.screen.blit(spritePool["exclamation"][1],
                                ((WIDTH/2) - (excDim/2), (HEIGHT/2) - (excDim/2)))
            if ratio >= 0.6 and ratio <= 1:
                if self.musicPlayer.getPlaying() != "bgsus3": self.musicPlayer.play("bgsus3")
                self.screen.blit(spritePool["exclamation"][0],
                                ((WIDTH/2) - (excDim/2), (HEIGHT/2) - (excDim/2)))
            if ratio > 0.9:
                self.state = 2
                self.musicPlayer.stop()
                self.dia.load("res/dialogue/losing-dialogue.txt")
                self.dia.makeActive()
                self.recordTime("LOSE")
            
            self.screen.blit(excText,
                            ((WIDTH/2) - (excText.get_width()/2), 0))
        else:
            if self.musicPlayer.getPlaying() != "bgsus1": self.musicPlayer.play("bgsus1")
        
        if self.dia.active:
            self.dia.update(self.screen)
        if miniMap and not self.p.quickTime:
            displayMiniMap(self.screen, self.grid.grid, pygame.Rect(WIDTH-200, 0, 200, 200), self.p.posV, self.grid.intelPositions, [x.posV for x in self.enemies[self.grid.id]])
        
        pygame.draw.circle(self.screen, (0, 255, 0), (WIDTH / 2, HEIGHT / 2), 5)
        if self.p.quickTime:
            self.screen.blit(keys[self.p.intelKeys[self.p.intelKeyCounter]][1], ((WIDTH/2)-64, (HEIGHT/2)-64))

        pygame.display.flip()
    
    def mainMenu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Prologue music should go here or something
                    self.dia.makeActive()
                    self.state = 1
                if event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
        
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.title, ((WIDTH/2)-self.title.get_width()/2, HEIGHT/2))

        pygame.display.flip()
    
    def gameOver(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Creates a new game object and restarts
                    self.restart = True
        
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.resultFont.render("You were caught. Press SPACE to Restart", True, (255, 255, 255)), (0, 0))

        if self.dia.active:
            self.dia.update(self.screen)

        pygame.display.flip()
 
    def youWin(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Creates a new game object and restarts
                        self.restart = True
            
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.resultFont.render("YOU WIN!!! Press SPACE to Restart", True, (255, 255, 255)), (0, 0))

            if self.dia.active:
                self.dia.update(self.screen)

            pygame.display.flip()
    
    def recordTime(self, win : str):
        with open("times.txt", "a") as f:
            date = datetime.datetime.now()
            
            line = f"{date.year}-{date.month}-{date.day} | {int(floor(self.time/60))}:{floor(self.time%60)} - {win}\n"
            f.write(line)
            f.close()
            

    def stateManager(self):
        match self.state:
            case 0:
                self.mainMenu()
            case 1:
                self.run()
            case 2:
                self.gameOver()
            case 3:
                self.youWin()
            case _:
                print(f"ERROR: unknown game state {self.state}!")
                pygame.quit()
                exit(1)

        self.clock.tick(fps)