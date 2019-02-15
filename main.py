import pygame
import os
import math
from random import choice


def load_image(name, color_key=None): #функция для загрузки изображений
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
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

#создание экрана
pygame.init()
size = 1024, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
#обозначаем группы и выгружаем объекты
all_sp = pygame.sprite.Group()
ball_sp = pygame.sprite.Group(all_sp)
blocks_sp = pygame.sprite.Group(all_sp)
player_sp = pygame.sprite.Group(all_sp)
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
background = load_image('background.jpg')
screen.blit(background, (0, 0))
ballimg = pygame.transform.scale(load_image('ball.png'), (20, 20))


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sp)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Ball(pygame.sprite.Sprite):#класс игрового шара

    def __init__(self):
        super().__init__(all_sp)
        self.add(ball_sp)
        self.image = ballimg
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 - self.rect[3] // 2
        self.rect.y = size[1] - 300
        self.vx = 5
        self.vy = 5

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        #self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, special_effect=None):
        super().__init__(self, blocks_sp)
        self.image = load_image('bricks/' + str(choice[1, 2, 3, 4, 5, 6, 7, 8, 9]) + '.png')
        self.special_effect = special_effect


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sp)
        self.add(player_sp)
        self.image = pygame.transform.scale\
            (load_image('player/' + choice['norm1', 'norm2', 'norm3'] + '.png'), (121, 32))
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 - self.rect[3] // 2
        self.rect.y = size[1] - 50
        self.moving_left = False
        self.moving_right = False

    def update(self):
        self.image = pygame.transform.scale\
            (load_image('player/' + choice['norm1', 'norm2', 'norm3'] + '.png'), (121, 32))
        if self.moving_left:
            self.rect.x -= 1
        if self.moving_right:
            self.rect.x += 1


#отрисовка всего
Ball()
#Paddle()
Border(5, 5, size[0] - 5, 5)
Border(5, size[1] - 5, size[0] - 5, size[1] - 5)
Border(5, 5, 5, size[1] - 5)
Border(size[0] - 5, 5, size[0] - 5, size[1] - 5)

fps = 60
running = True
all_sp.draw(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(fps)
    all_sp.update()
    pygame.display.flip()

pygame.quit()