import pygame
from modules.settings import *
import os

pygame.mixer.init()

class DialogueController:
    def __init__(self, dialoguePath : str, fontPath : str, fontSize : int = 24):
        self.dialogueFont = pygame.font.Font(fontPath, fontSize)
        self.dialogueList = [x.removesuffix("\n") for x in open(dialoguePath, 'r').readlines()]
        self.dialogueIndex = 0
        self.currentRender = self.dialogueFont.render(self.dialogueList[self.dialogueIndex], True, (255, 255, 255))
        self.active = False

        self.last = None
    
    def load(self, dialoguePath : str):
        self.dialogueList = [x.removesuffix("\n") for x in open(dialoguePath, 'r').readlines()]
        self.dialogueIndex = 0
        self.currentRender = self.dialogueFont.render(self.dialogueList[self.dialogueIndex], True, (255, 255, 255))
    
    def makeActive(self):
        self.active = True
        self.last = pygame.time.get_ticks()

    def update(self, screen : pygame.Surface):
        if self.active:
            screen.blit(self.currentRender, (5, HEIGHT - (self.currentRender.get_height()*2)))
            if getDeltaTime(pygame.time.get_ticks(), self.last) >= READINGPACE * len(self.dialogueList[self.dialogueIndex]):
                self.last = pygame.time.get_ticks()
                self.dialogueIndex += 1
                if self.dialogueIndex >= len(self.dialogueList):
                    self.dialogueList.clear()
                    self.dialogueIndex = 0
                    self.active = False
                else:
                    self.currentRender = self.dialogueFont.render(self.dialogueList[self.dialogueIndex], True, (255, 255, 255))

class MusicController:
    def __init__(self, musicPath : str):
        self.music = {}
        self.musicPath = musicPath
        for file in os.listdir(musicPath):
            self.music[file.removesuffix(".mp3")] = self.musicPath+file
        
        self.playing = None

    def setVolume(self, vol : int):
        pygame.mixer.music.set_volume(vol/100)
    
    def getPlaying(self):
        return self.playing

    def play(self, id : str):
        pygame.mixer.music.load(self.music[id])
        pygame.mixer.music.play(-1)
        self.playing = id
    
    def stop(self):
        pygame.mixer.music.stop()

# class Button:
#     def __init__(self, font : pygame.Font):



