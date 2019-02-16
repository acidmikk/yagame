import pygame
import os
from random import choice
from random import randint


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
vertical_borders = pygame.sprite.Group()
background = load_image('background.jpg')
ballimg = pygame.transform.scale(load_image('ball.png'), (20, 20))
life = 3


def Life(life):
    life -= 1


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
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        while self.vx == 0 or self.vy == 0 or abs(self.vx) < 3 or abs(self.vy) < 3:
            self.vx = randint(-5, 5)
            self.vy = randint(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.rect.y < size[1] // 2:
                self.vy = -self.vy
            else:
                self.rect.x, self.rect.y = self.start
                self.vx = randint(-5, 5)
                self.vy = randint(-5, 5)
                while self.vx == 0 or self.vy == 0 or abs(self.vx) < 3 or abs(self.vy) < 3:
                    self.vx = randint(-5, 5)
                    self.vy = randint(-5, 5)
                Life(life)
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
        # Border(x - 1, y - 1, x - 1, y + 32 - 1)
        # Border(x - 1, y - 1 + 32, x - 1 + 96, y - 1 + 32)
        # Border(x + 96 - 1, y - 1, x + 96 - 1, y + 32 - 1)
        # Border(x - 1, y - 1, x + 96 - 1, y - 1)

    def update(self):
        if pygame.sprite.spritecollideany(self, ball_sp):
            if self.nb in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.nb = self.nb[:1] + 'b' + self.nb[1:]
                self.image = pygame.transform.scale\
                    (load_image('bricks/' + self.nb + '.png'), (96, 32))
            else:
                self.kill()
        if pygame.sprite.spritecollideany(self, ball_sp):
            if ball_sp.sprites()[0].rect.y > self.rect.y + 32:
                ball_sp.sprites()[0].vy = -ball_sp.sprites()[0].vy
            elif ball_sp.sprites()[0].rect.y + 20 < self.rect.y:
                ball_sp.sprites()[0].vy = -ball_sp.sprites()[0].vy
            elif ball_sp.sprites()[0].rect.x + 20 < self.rect.x:
                ball_sp.sprites()[0].vx = -ball_sp.sprites()[0].vx
            elif ball_sp.sprites()[0].rect.x > self.rect.x + 96:
                ball_sp.sprites()[0].vx = -ball_sp.sprites()[0].vx


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
            self.rect.x -= 10
        if self.moving_right:
            self.rect.x += 10


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

while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player_sp.sprites()[0].get_event(event)
        if event.type == pygame.KEYUP:
            player_sp.sprites()[0].get_event(event)
    clock.tick(fps)
    all_sp.draw(screen)
    all_sp.update()
    pygame.display.flip()

pygame.quit()