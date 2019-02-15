#задаём экран и подключаем всё, что необходимо для начала
import pygame
import os
import math


pygame.init()
size = 720, 480
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
#обозначаем группы
all_sp = pygame.sprite.Group()
ball_sp = pygame.sprite.Group(all_sp)
blocks_sp = pygame.sprite.Group(all_sp)
player_sp = pygame.sprite.Group(all_sp)


def load_image(name, color_key=None): #функция для загрузки изображений
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Ball(pygame.sprite.Sprite):#класс игрового шара
    def __init__(self, rad, x, y):
        super().__init__(all_sp)
        self.add(ball_sp)
        self.


fps = 60
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(fps)
    pygame.display.flip()



pygame.quit()