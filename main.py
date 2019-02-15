import pygame
import os


pygame.init()
size = 720, 480
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(fps)
    pygame.display.flip()



pygame.quit()