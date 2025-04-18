from player import *
import pygame
from network import Network


pygame.init()

menu_screen = pygame.image.load("menu_screen.png")
black = (0, 0, 0)
display_height = 600
display_width = 800

# set music
pygame.mixer.music.load("opening_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

gameDisplay = pygame.display.set_mode((display_width, display_height))  # pygame.FULLSCREEN
gameDisplay.fill(black)
clock = pygame.time.Clock()
kirby.menuScreen(gameDisplay, menu_screen)
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
                quit()

n = Network()
p1 = n.getP()

facing = 0
run = True

while run:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False
        pygame.quit()
        quit()

    if keys[pygame.K_0]:  # change music
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

    p1.print_sequence(n, gameDisplay)

    facing = checkForMove(p1, n, facing, gameDisplay)

    pygame.display.update()

    p2 = n.send(p1)
    e1 = n.send('1')
    if (p1.life <= 0 and p2.life <= 0) or e1.life <= 0:  # if both players lost or the AI, quit the main loop
        run = False


wait = True
p2 = n.send(p1)

if p1.life > 0 or p2.life > 0:
    kirby.drawField(1, gameDisplay, 0)  # draw winning screen

else:
    kirby.drawField(2, gameDisplay, 0)  # draw losing screen

pygame.display.update()
while wait:  # wait for the key "space" or "escape" to quit the game
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                wait = False
            if event.key == pygame.K_ESCAPE:
                wait = False

pygame.quit()
