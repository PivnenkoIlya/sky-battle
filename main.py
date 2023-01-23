import os
import random
from random import choice
import sqlite3
import sys
import os

import pygame

pygame.init()
size = width, height = 500, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sky battle")

v = 20
fps = 60
x = 0
clock = pygame.time.Clock()

my_file = open("data/level.txt", "w")
my_file.write('1')
my_file.close()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
ball_grope = pygame.sprite.Group()
player_group = pygame.sprite.Group()


#############################################################


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    def delete(self):
        for i in horizontal_borders:
            horizontal_borders.remove(i)
        for i in vertical_borders:
            vertical_borders.remove(i)


border = Border()


class Block(pygame.sprite.Sprite):
    image = load_image("block.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Block.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pos
        self.rect.bottom = height - 65
        self.rect.left = pos + 40

    def update(self):
        self.rect.y += -20

        if pygame.sprite.spritecollide(self, ball_grope, True):
            pygame.sprite.spritecollide(self, player_group, True)
            my_file = open("data/score.txt", "r")
            file = my_file.readlines()
            score = file[0]
            my_file.close()
            my_file = open("data/score.txt", "w")
            my_file.write(str(int(score) + 1))
            my_file.close()


class Ball(pygame.sprite.Sprite):
    image = load_image("bullet.png")
    image = pygame.transform.scale(image, (50, 50))

    def __init__(self):
        super().__init__(all_sprites)
        self.add(ball_grope)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = random.randint(50, 100)
        self.rect.left = random.randint(50, 450)
        speeds = [1, -1]
        self.vx = choice(speeds)
        self.vy = choice(speeds)

    def update(self):
        file = open("data/do_play.txt", "r")
        do_play = file.readlines()[0]
        file.close()

        file = open("data/score.txt", "r")
        score = file.readlines()[0]
        file.close()

        file = open("data/level.txt", "r")
        level = int(file.readlines()[0])
        file.close()

        if do_play != 'no':
            self.rect = self.rect.move(self.vx, self.vy)
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx

            if pygame.sprite.spritecollide(self, player_group, True):

                file = open("data/score.txt", "w")
                file.write('0')
                file.close()

                file = open("data/score.txt", "w")
                file.write('0')
                file.close()

                file = open("data/do_play.txt", "w")
                file.write('no')
                file.close()

                print(all_sprites.sprites())

                menu.menu_open('lose')


class Player(pygame.sprite.Sprite):
    image = load_image("player.png", -1)
    image = pygame.transform.scale(image, (100, 80))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = height - 70
        self.rect.left = 220
        self.add(player_group)

    def go(self, v):
        if self.rect.x < 0:
            self.rect.x = 300 + self.image.get_size()[0]
        elif self.rect.x > 300 + self.image.get_size()[0]:
            self.rect.x = 0
        self.rect.x += v

    def get_pos(self):
        return self.rect.x


class Play:

    def add_background(self):
        Border(5, 50, width - 5, 50)
        Border(5, height - 5, width - 5, height - 5)
        Border(5, 5, 5, height - 5)
        Border(width - 5, 5, width - 5, height - 5)
        random_background = choice(
            ["background.jpg", 'background_2.jpg', "background_3.jpg", 'background_4.jpg',
             "background_5.jpg"])

        # image = load_image(random_background)
        sprite = pygame.sprite.Sprite()
        # определим его вид
        sprite.image = load_image(random_background)
        sprite.image = pygame.transform.scale(sprite.image, (500, 700))
        # и размеры
        sprite.rect = sprite.image.get_rect()
        # добавим спрайт в группу
        all_sprites.add(sprite)
        # all_sprites.draw(screen)

    def start_game(self, level, win_or_lose):
        print('start game')
        file = open("data/score.txt", "w")
        file.write('0')
        file.close()

        file1 = open("data/do_play.txt", "w")
        file1.write('yes')
        file1.close()
        file1 = open("data/do_play.txt", "r")
        print(file1.readlines())
        file1.close()

        self.add_background()
        player = Player()
        font1 = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        score_text = font1.render(f"Score: 0", 1, (0, 255, 255))

        running = True
        if win_or_lose in ('win', 'default'):
            for i in range(level * 2):
                Ball()

        while running:
            file_ = open("data/score.txt", "r")
            file = file_.readlines()
            score = file[0]
            file_.close()

            file_ = open("data/record.txt", "r")
            file = file_.readlines()
            record = file[0]
            file_.close()

            all_sprites.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    border.delete()
                    running = False
                    file = open("data/record.txt", "w")
                    if int(score) > int(record):
                        file.write(score)
                    else:
                        file.write(record)
                    file.close()
                    pygame.sprite.Group.remove(player_group)
                    # menu.menu_open()
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    menu.menu_open()
                    border.delete()
                    running = False
                    file = open("data/record.txt", "w")
                    if int(score) > int(record):
                        file.write(score)
                    else:
                        file.write(record)
                    file.close()
                    # pygame.sprite.spritecollide(self, player_group, True)
                elif key[pygame.K_RIGHT]:
                    player.go(20)
                elif key[pygame.K_LEFT]:
                    player.go(-20)
                elif key[pygame.K_SPACE]:
                    x = player.get_pos()
                    Block(x)

            file_ = open("data/do_play.txt", "r")
            file = file_.readlines()
            do = file[0]
            file_.close()
            if do != 'yes':
                border.delete()
                running = False

            file_.close()

            score_text = font1.render(f"Score: {score}", 1, (0, 255, 255))
            screen.blit(score_text, (10, 10))

            if int(score) == level * 2:
                file = open("data/do_play.txt", "w")
                file.write('no')
                file.close()

                file = open("data/score.txt", "w")
                file.write('0')
                file.close()

                file = open("data/level.txt", "w")
                file.write(str(level * 2))
                file.close()
                menu.menu_open('win')

            clock.tick(fps)
            all_sprites.update()
            ball_grope.update()
            pygame.display.flip()


play = Play()


class Main_menu:
    def menu_open(self, win_or_lose='default'):
        file = open("data/do_play.txt", "w")
        file.write('yes')
        file.close()
        running = True
        image = load_image("bg_menu.jpg")
        sprite = pygame.sprite.Sprite()
        # определим его вид
        sprite.image = load_image("bg_menu.jpg")
        sprite.image = pygame.transform.scale(image, (500, 700))
        # и размеры
        sprite.rect = sprite.image.get_rect()
        # добавим спрайт в группу
        all_sprites.add(sprite)
        # all_sprites.draw(screen)

        while running:
            file = open("data/level.txt", "r")
            level = int(file.readlines()[0])
            file.close()
            all_sprites.draw(screen)
            font1 = pygame.font.SysFont(pygame.font.get_default_font(), 70)
            font2 = pygame.font.SysFont(pygame.font.get_default_font(), 60)
            font3 = pygame.font.SysFont(pygame.font.get_default_font(), 50)

            if win_or_lose == 'win':
                win_or_lose_text = font1.render("You win :)", 1, (124, 252, 0))
            elif win_or_lose == 'lose':
                win_or_lose_text = font1.render("You lose :(", 1, (225, 0, 0))
            else:
                win_or_lose_text = font1.render("", 1, (0, 0, 0))

            title = font1.render("Sky Battle", 1, (0, 255, 255))

            file = open("data/record.txt", "r")
            temp = file.readlines()
            try:
                record = temp[0]
            except Exception:
                record = '0'
            file.close()

            record = font3.render(f"  level: {int(level)}", 1, (255, 255, 255))
            button_play = font2.render("Play", 1, 'yellow')
            # all_sprites.add(title)
            # all_sprites.add(button_play)
            screen.blit(title, (125, 50))
            screen.blit(record, (180, 300))
            screen.blit(win_or_lose_text, (135, 610))
            #
            screen.blit(button_play, (210, 180))
            button_play_x = 210
            button_play_y = 180

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x >= button_play_x and x <= button_play_x + button_play.get_size()[0]:
                        if y >= button_play_y and y <= button_play_y + button_play.get_size()[1]:
                            running = False
                            play.start_game(level, win_or_lose)

            clock.tick(fps)
            all_sprites.update()
            pygame.display.flip()


menu = Main_menu()
menu.menu_open()
