import pygame


# Sliding Method for one row spritesheet
class SpriteManager:
    def __init__(self, surface: pygame.Surface, windowWidth: float, windowHeight: float, updateTicks: int):
        self.width = windowWidth
        self.height = windowHeight
        self.sprite = surface.copy()
        self.sprite.convert_alpha()
        self.curFrame = self.sprite.subsurface(0, 0, windowWidth, windowHeight)
        self.indexes = surface.get_width() // windowWidth
        self.index = 0

        self.prevTime = pygame.time.get_ticks()
        self.updateTicks = updateTicks

    def update(self):
        if pygame.time.get_ticks() - self.prevTime >= self.updateTicks:
            self.index = (self.index + 1) % self.indexes
            self.curFrame = self.sprite.subsurface(self.width * self.index, 0, self.width, self.height)
            self.prevTime = pygame.time.get_ticks()

    def draw(self, screen: pygame.Surface, dest: tuple[int, int]):
        screen.blit(self.curFrame, (dest[0], dest[0]))
