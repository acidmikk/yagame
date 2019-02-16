import pygame
import os
from random import choice
from random import randint
import sys


def terminate():
    pygame.quit()
    sys.exit()


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
size = 1024, 768
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
#обозначаем группы и выгружаем объекты
all_sp = pygame.sprite.Group()
ball_sp = pygame.sprite.Group(all_sp)
blocks_sp = pygame.sprite.Group(all_sp)
player_sp = pygame.sprite.Group(all_sp)
horizontal_borders = pygame.sprite.Group()
hor_bricks = pygame.sprite.Group(all_sp)
ver_bricks = pygame.sprite.Group(all_sp)
vertical_borders = pygame.sprite.Group()
background = load_image('background.jpg')
ballimg = pygame.transform.scale(load_image('ball.png'), (20, 20))
plife = 3
point = 0


def score():
    global point
    point += 50


def life():
    global plife
    plife -= 1


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
        self.start = size[0] // 2 - self.rect[3] // 2, size[1] - 300
        self.rect.x = self.start[0]
        self.rect.y = self.start[1]
        self.vx = randint(-6, 6)
        self.vy = randint(-6, 6)
        while self.vx == 0 or self.vy == 0 or abs(self.vx) < 4 or abs(self.vy) < 4:
            self.vx = randint(-6, 6)
            self.vy = randint(-6, 6)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.rect.y < size[1] // 2:
                self.vy = -self.vy
            else:
                self.rect.x, self.rect.y = self.start
                self.vx = randint(-6, 6)
                self.vy = randint(-6, 6)
                while self.vx == 0 or self.vy == 0 or abs(self.vx) < 4 or abs(self.vy) < 4:
                    self.vx = randint(-6, 6)
                    self.vy = randint(-6, 6)
                life()
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, player_sp):
            self.vy = -abs(self.vy)


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, special_effect=None):
        super().__init__(all_sp)
        self.add(blocks_sp)
        self.nb = str(choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
        self.image = pygame.transform.scale(load_image('bricks/' + self.nb + '.png'), (96, 32))
        self.special_effect = special_effect
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.borders = [Border(x + 1, y + 1, x + self.rect[2] - 1, y + 1),
                        Border(x + 1, y + self.rect[3] - 1, x + self.rect[2] - 1, y + self.rect[3] - 1),
                        Border(x + 1, y + 1, x + 1, y + self.rect[3] - 1),
                        Border(x + self.rect[2] - 1, y + 1, x + self.rect[2] - 1, y + self.rect[3] - 1)]

    def update(self):
        if pygame.sprite.spritecollideany(self, ball_sp):
            if self.nb in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.nb = self.nb[:1] + 'b' + self.nb[1:]
                self.image = pygame.transform.scale\
                    (load_image('bricks/' + self.nb + '.png'), (96, 32))
            else:
                score()
                self.kill()
                for _ in self.borders:
                    _.kill()


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sp)
        self.add(player_sp)
        self.name = choice(['norm1', 'norm2', 'norm3'])
        self.image = pygame.transform.scale\
            (load_image('player/' + self.name + '.png'), (121, 32))
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 - self.rect[3] // 2
        self.rect.y = size[1] - 30
        self.moving_left = False
        self.moving_right = False

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving_left = True
            if event.key == pygame.K_RIGHT:
                self.moving_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_left = False
            if event.key == pygame.K_RIGHT:
                self.moving_right = False

    def update(self):
        self.name = choice(['norm1', 'norm2', 'norm3'])
        self.image = pygame.transform.scale\
            (load_image('player/' + self.name + '.png'), (121, 32))
        if self.moving_left:
            if self.rect.x < 5:
                pass
            else:
                self.rect.x -= 12
        if self.moving_right:
            if self.rect.x > size[0] - 121 - 5:
                pass
            else:
                self.rect.x += 12


#отрисовка всего
for y in range(5):
    for x in range(10):
        Brick(x * 96 + 30, y * 32 + 20)
Ball()
Paddle()
Border(5, 5, size[0] - 5, 5)
Border(5, size[1] - 5, size[0] - 5, size[1] - 5)
Border(5, 5, 5, size[1] - 5)
Border(size[0] - 5, 5, size[0] - 5, size[1] - 5)

fps = 60
running = True

screen.blit(background, (0, 0))
myfont = pygame.font.Font(None, 50)
text1 = myfont.render('PRESS SPACE TO START', 1, pygame.Color('white'))
place = text1.get_rect(center=(size[0] // 2, size[1] // 2))
screen.blit(text1, place)
pygame.display.flip()
sp = True
while sp:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sp = False

text1 = myfont.render('PRESS SPACE TO CONTINUE', 1, pygame.Color('white'))
place = text1.get_rect(center=(size[0] // 2, size[1] // 2))
lifefont = pygame.font.Font(None, 24)


while running:
    screen.blit(background, (0, 0))
    lifetext = lifefont.render('LIFE: ' + str(plife), 1, pygame.Color('white'))
    screen.blit(lifetext, (30, 5))
    scor = lifefont.render('SCORE: ' + str(point), 1, pygame.Color('white'))
    screen.blit(scor, (910, 5))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            player_sp.sprites()[0].get_event(event)
            if event.key == pygame.K_ESCAPE:
                screen.blit(text1, place)
                pygame.display.flip()
                sp = True
                while sp:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                sp = False
        if event.type == pygame.KEYUP:
            player_sp.sprites()[0].get_event(event)
    clock.tick(fps)
    all_sp.draw(screen)
    all_sp.update()
    pygame.display.flip()
    if not plife:
        screen.blit(background, (0, 0))
        gg = myfont.render('GAME OVER', 1, pygame.Color('white'))
        rgg = gg.get_rect(center=(size[0] // 2, size[1] // 2))
        screen.blit(gg, rgg)
        pygame.display.flip()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    terminate()

pygame.quit()