import Objects
import ScreenGenerator
import pygame
from pygame.draw import *

pygame.init()
FPS = 30
screen = pygame.display.set_mode((400, 400))

gas = Objects.Gas()
screen_gen = ScreenGenerator.ScreenGenerator(gas.get_space())

clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    gas.update()
    screen.blit(screen_gen.update(), (0, 0))
    pygame.display.update()

pygame.quit()