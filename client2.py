from player import *
import pygame
import time
from network import Network


pygame.init()

menu_screen = pygame.image.load("menu_screen.png")
white = (255,255,255)
black = (0,0,0)
display_height = 600
display_width = 800

# set music
pygame.mixer.music.load("opening_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

gameDisplay = pygame.display.set_mode((display_width,display_height))  # pygame.FULLSCREEN
gameDisplay.fill(black)
clock = pygame.time.Clock()
kirby.menuScreen(gameDisplay,menu_screen)
pygame.display.update()

wait = True
run = True

while wait:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                wait = False
            if event.key == pygame.K_ESCAPE:
                wait = False
                run = False
                pygame.quit()

n = Network()
p1 = n.getP()
facing = 0
run = True

while run:

    clock.tick(60)
    p2 = n.send(p1)
    kirby.drawField(0, gameDisplay)
    kirby.drawKirby(p2.x,p2.y,p2.anm,gameDisplay)  # draws kirby

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False
        pygame.quit()

    if keys[pygame.K_0]:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("earrape.mp3")
        pygame.mixer.music.play(-1)

    if keys[pygame.K_9]:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("opening_music.mp3")
        pygame.mixer.music.play(-1)

    if facing:
        p1.anm = 33
    else:
        p1.anm = 0
    kirby.drawKirby(p1.x,p1.y,p1.anm,gameDisplay)  # draws kirby
    facing = checkForMove(p1,n,facing, gameDisplay)

    pygame.display.update()
