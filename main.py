from modules.game import *

pygame.init()
pygame.font.init()
pygame.display.set_caption("FREEZING POINT")

game = Game()
while game.running == True:
    game.stateManager()
    if game.restart:
        game = Game(game.restart)
