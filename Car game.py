import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

font = pygame.font.SysFont("Inkfree", 60)
font_small = pygame.font.SysFont("Inkfree", 25)
game_over = font.render("Gotcha Bitch", True, GREEN)

background = pygame.image.load("background-2_0.png")

DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Car Game")

class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
           if pressed_keys[K_LEFT]:
               self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
           if pressed_keys[K_RIGHT]:
               self.rect.move_ip(5, 0)
        if self.rect.top > 0:
           if pressed_keys[K_UP]:
               self.rect.move_ip(0,-5)
        if self.rect.bottom < SCREEN_HEIGHT:
           if pressed_keys[K_DOWN]:
               self.rect.move_ip(0,5)


P1 = Player()
E1 = Enemy()
E2 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)
enemies.add(E2)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(E2)


INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:


    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, RED)
    DISPLAYSURF.blit(scores, (10,10))


    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('crash.wav').play()
          time.sleep(0.5)

          DISPLAYSURF.fill(BLACK)
          DISPLAYSURF.blit(game_over, (40,260))

          pygame.display.update()
          for entity in all_sprites:
                entity.kill()
          time.sleep(2)
          pygame.quit()
          sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
