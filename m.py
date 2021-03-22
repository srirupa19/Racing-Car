import os, sys
import random
from collections import deque
import pygame
import math

pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size, flags=pygame.NOFRAME)

# resources
bg = pygame.image.load('resources/background.png')
mycar_image = pygame.image.load('resources/mycar/with_shadow.png')
mycar_image = pygame.transform.rotozoom(mycar_image, 0, 0.5)
opp1_image = pygame.image.load('resources/opcar1/with_shadow.png')
opp1_image = pygame.transform.rotozoom(opp1_image, 180, 0.5)
opp2_image = pygame.image.load('resources/opcar2/with_shadow.png')
opp2_image = pygame.transform.rotozoom(opp2_image, 180, 0.5)
opp3_image = pygame.image.load('resources/opcar3/with_shadow.png')
opp3_image = pygame.transform.rotozoom(opp3_image, 180, 0.5)
mycar_image_noshadow = pygame.image.load('resources/mycar/without_shadow.png')
mycar_image_noshadow = pygame.transform.rotozoom(mycar_image_noshadow, 0, 0.5)
opp1_image_noshadow = pygame.image.load('resources/opcar1/without_shadow.png')
opp1_image_noshadow = pygame.transform.rotozoom(opp1_image_noshadow, 180, 0.5)
opp2_image_noshadow = pygame.image.load('resources/opcar2/without_shadow.png')
opp2_image_noshadow = pygame.transform.rotozoom(opp2_image_noshadow, 180, 0.5)
opp3_image_noshadow = pygame.image.load('resources/opcar3/without_shadow.png')
opp3_image_noshadow = pygame.transform.rotozoom(opp3_image_noshadow, 180, 0.5)
fire_image = pygame.image.load('resources/fire.png')
fire_image = pygame.transform.rotozoom(fire_image, 0, 0.4)
fireo_image = pygame.image.load('resources/fireo.png')
fireo_image = pygame.transform.rotozoom(fireo_image, 0, 0.4)
energy_image = pygame.image.load('resources/energy.png')
energy_image = pygame.transform.rotozoom(energy_image, 0, 1)

explosions = list(
    map(
        lambda index: pygame.image.load(
            f"resources/explosions/explosion_{index:0>2d}.png").convert_alpha(
            ), range(1, 49)))

# bounding rects
bg_rect = bg.get_bounding_rect()
mycar_rect = mycar_image_noshadow.get_bounding_rect().inflate(-16, -16)
opp1_rect = opp1_image_noshadow.get_bounding_rect().inflate(-8, -8)
opp2_rect = opp2_image_noshadow.get_bounding_rect().inflate(-8, -8)
opp3_rect = opp3_image_noshadow.get_bounding_rect().inflate(-16, -16)
fire_rect = fire_image.get_bounding_rect()
fireo_rect = fireo_image.get_bounding_rect()
energy_rect = energy_image.get_bounding_rect()
quit_rect = pygame.Rect(280, 300, 70, 30)
playagain_rect = pygame.Rect(230, 350, 170, 30)

# font
font = pygame.font.SysFont('kristenitc,consolas', 24)
font_bigger = pygame.font.SysFont('kristenitc,consolas', 36)
font_color = (0, 0, 0)


def give_image(num):

    if num == 1:
        return opp1_image
    elif num == 2:
        return opp2_image
    else:
        return opp3_image


def give_rect(num):
    if num == 1:
        return opp1_rect
    elif num == 2:
        return opp2_rect
    else:
        return opp3_rect


class Background():
    def __init__(self, y, vely):
        self.y = y
        self.vely = vely

        self.x = 0

        self.accy = 0

    def draw(self):
        if mycar.alive:
            self.y += self.vely
            self.vely = min((self.vely + self.accy), 50)

        return (self.x, self.y)


class MyCar():
    def __init__(self):
        self.x = 300
        self.y = 400
        self.velx = 0
        self.alive = True
        self.moving = False

    def start(self):
        mycar.moving = True

        for bgrn in background:
            bgrn.accy = 1

    def move(self, direction):
        if direction == "left" and self.x > 90:
            self.velx = -7
        elif self.x < 500 and direction == "right":
            self.velx = 7
        else:
            self.velx = 0

        self.x += self.velx

    def shoot(self):
        pass

    def check_dead(self):
        if self.alive:
            for opp in opponent:
                if give_rect(opp.num).move(opp.x, opp.y).colliderect(
                        mycar_rect.move(self.x, self.y)):
                    self.energy = 0
                    self.alive = False
                    self.moving = False


class Opponent():
    def __init__(self, x, y, n):
        self.alive = True
        self.energy = 20
        self.num = n

        self.x = x
        self.y = y

        self.velx = 0
        self.vely = 3

        self.accx = 0
        self.accy = 0

    def move(self):
        self.y += self.vely

        return (self.x, self.y)

    def randomx(self, a):

        self.accx = a
        self.x += self.velx
        self.velx += self.accx

        self.x = int(self.x)

    def randomy(self):
        pass

    def shoot(self):
        pass

    def reinit(self):
        self.alive = True
        self.energy = 20
        self.y = -random.randint(300, 700)
        self.x = random.randint(50, 550)


class Fire:
    def __init__(self, y, x):
        self.y = y
        self.x = x + 12

    # def move(self):
    #     return (self.x , self.y)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.last_time = pygame.time.get_ticks()
        self.size = 0
        self.img = explosions[0]

    def update(self):

        now_time = pygame.time.get_ticks()

        if (now_time - self.last_time) > 30:
            self.size += 1
            self.last_time = now_time
            if self.size < 48:
                self.img = explosions[self.size]

        if self.size == 48:
            self.kill()
        else:
            screen.blit(self.img, (self.x, self.y))


clock = pygame.time.Clock()

# create objects

# background
background = deque(maxlen=2)
background.append(Background(0, 0))
background.append(Background(-height, 0))

# mycar
mycar = MyCar()

# opponent

opponent = deque(maxlen=3)
opponent.append(Opponent(80, -100, 1))
opponent.append(Opponent(480, -370, 2))
opponent.append(Opponent(230, -850, 3))

# fire
fires = deque(maxlen=10)
fires.append(Fire(mycar.y, mycar.x))
for i in range(9):
    fires.append(Fire(fires[-1].y + 50, mycar.x))

fired = False

opp_fires = [deque(maxlen=10) for _ in range(3)]

for i in range(3):
    opp_fires[i].append(Fire(opponent[i].y, opponent[i].x))
    for j in range(9):
        opp_fires[i].append(Fire(opp_fires[i][-1].y - 70, opponent[i].x))

# energy

energy = 100
energy_y = -800
energy_x = random.randint(200, 400)

# score
score = 0

while True:

    for bgrn in background:
        if not mycar.moving or bgrn.vely < 0:
            bgrn.vely = 0
            bgrn.accy = 0

        screen.blit(bg, bgrn.draw())

    # distance += (abs(background[0].vely))
    # speed = int(abs(background[0].vely))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and (
                not mycar.moving) and mycar.alive:
            mycar.start()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and mycar.moving:
            if not fires:
                fires.append(Fire(mycar.y, mycar.x))
                for i in range(9):
                    fires.append(Fire(fires[-1].y + 50, mycar.x))

        if (not mycar.alive and event.type == pygame.MOUSEBUTTONDOWN
                and quit_rect.collidepoint(event.pos)):
            exit()
        if (not mycar.alive and event.type == pygame.MOUSEBUTTONDOWN
                and playagain_rect.collidepoint(event.pos)):

            mycar.alive = True
            mycar.moving = False
            background = deque(maxlen=2)
            background.append(Background(0, 0))
            background.append(Background(-height, 0))
            opponent = deque(maxlen=3)
            opponent.append(Opponent(80, -100, 1))
            opponent.append(Opponent(480, -370, 2))
            opponent.append(Opponent(230, -850, 3))
            mycar = MyCar()
            score = 0
            time_now, start_time = 0, 0
            energy = 100
            fires.append(Fire(mycar.y, mycar.x))
            for i in range(9):
                fires.append(Fire(fires[-1].y + 50, mycar.x))

    key_states = pygame.key.get_pressed()

    if mycar.alive and mycar.moving:

        if key_states[pygame.K_LEFT]:
            mycar.move("left")
        if key_states[pygame.K_RIGHT]:
            mycar.move("right")
        if key_states[pygame.K_UP]:
            fired = True
        else:
            fired = False

    # time and score
    if not mycar.moving:
        start_time = pygame.time.get_ticks()
        if mycar.alive:
            time_now = 0
            distance = 0.0
            speed = 0.0
    else:
        time_now = (pygame.time.get_ticks() - start_time) // 1000

    # background details
    if background[0].y > 480:
        background.append(
            Background(background[-1].y - height, background[-1].vely))

    # energy coins
    if mycar.moving:

        if energy_y > 500:
            energy_y = -3000
            energy_x = random.randint(150, 500)
        else:
            energy_y += 5

        if (energy_rect.move(energy_x, energy_y)).colliderect(
                mycar_rect.move(mycar.x, mycar.y)):
            energy_y = -3000
            energy_x = random.randint(150, 500)
            energy += 25

        screen.blit(energy_image, (energy_x, energy_y))

    screen.blit(mycar_image, (mycar.x, mycar.y))

    # WORKS BUT CREATE FIRE CLASS
    if fired and mycar.moving:

        for fire in fires:

            fire.y -= 15

            if fire.y < 400:

                screen.blit(fire_image, (fire.x, fire.y))

                energy -= 0.05

                for opp in opponent:
                    if fire_rect.move(fire.x, fire.y).colliderect(
                            give_rect(opp.num).move(opp.x, opp.y)):
                        opp.energy -= 2

    if fires[0].y < 0:
        fires.append(Fire(fires[-1].y + 50, mycar.x))

    for opp in opponent:
        if opp.energy <= 0 and opp.alive:
            opp.alive = False
            score += 1
            opp.energy -= 0.1
            explosion = Explosion(opp.x, opp.y)
        if not opp.alive:

            if explosion.size > 48:
                opp.reinit()
            else:

                explosion.update()

    if not fired and mycar.moving:
        for i in range(len(fires)):

            if fires[i].y < 400:

                fires[i].y -= 15

                screen.blit(fire_image, (fires[i].x, fires[i].y))
            else:
                fires[i].x = mycar.x + 12

    if mycar.moving:
        for opp in opponent:
            if opp.alive:
                screen.blit(give_image(opp.num), opp.move())

                if opp.y > 550:
                    opp.reinit()

        for opp in opponent:
            if opp.alive:
                if opp.y < 100 and opp.y > 0:
                    if opp.x < 300:
                        opp.randomx(0.1)
                    else:
                        opp.randomx(-0.1)
                else:
                    opp.velx = 0
                    opp.accx = 0
    else:
        for opp in opponent:
            if opp.alive:
                screen.blit(give_image(opp.num), (opp.x, opp.y))

    # opp fire

    for i in range(3):

        if mycar.moving and opponent[i].alive:

            if opponent[i].y > 150:
                for of in opp_fires[i]:

                    of.y += 15
                    of.x = opponent[i].x + 12
                    if of.y > (opponent[i].y + 70):

                        screen.blit(fireo_image, (of.x, of.y))
                    # fire opp hits mycar
                    if fireo_rect.move(of.x, of.y).colliderect(
                            mycar_rect.move(mycar.x, mycar.y)):
                        energy -= 0.5

            if opp_fires[i][0].y > 500:
                opp_fires[i].append(
                    Fire(opp_fires[i][-1].y - 70, opponent[i].x))

    if energy <= 0:
        mycar.alive = False
        mycar.moving = False

    mycar.check_dead()

    if mycar.alive:

        time_rendered = font.render("TIME : " + str(time_now), True,
                                    font_color)
        screen.blit(time_rendered, (5, 65))
        dist_rendered = font.render("ENERGY : " + str(int(energy)), True,
                                    font_color)
        screen.blit(dist_rendered, (5, 5))
        speed_rendered = font.render("SCORE : " + str(score), True, font_color)
        screen.blit(speed_rendered, (5, 35))

        if not mycar.moving:
            instructions1 = font.render("CLICK TO START ", True,
                                       font_color)
            screen.blit(instructions1, (200, 250))
            instructions2 = font.render("PRESS UP KEY TO SHOOT ", True,
                                       font_color)
            screen.blit(instructions2, (150, 100))

            instructions3 = font.render("PRESS LEFT & RIGHT KEYS TO MOVE ", True,
                                       font_color)
            screen.blit(instructions3, (80, 150))

            instructions4 = font.render("SAVE FUEL TO LIVE LONGER ", True,
                                       font_color)
            screen.blit(instructions4, (120, 300))
            

    else:

        game_over = font.render("GAME OVER ", True, font_color)
        screen.blit(game_over, (235, 250))
        time_rendered = font.render("TIME : " + str(time_now), True,
                                    font_color)
        screen.blit(time_rendered, (5, 65))
        dist_rendered = font.render("ENERGY : " + str(int(energy)), True,
                                    font_color)
        screen.blit(dist_rendered, (5, 5))
        speed_rendered = font.render("SCORE : " + str(score), True, font_color)
        screen.blit(speed_rendered, (5, 35))

        quit_text = font.render("QUIT ", True, font_color)
        screen.blit(quit_text, (280, 300))

        playagain_text = font.render("PLAY AGAIN ", True, font_color)
        screen.blit(playagain_text, (230, 350))

        score_text = font.render("SCORE : " + str(score), True, font_color)
        screen.blit(score_text, (250, 150))

    pygame.display.update()
    clock.tick(30)
