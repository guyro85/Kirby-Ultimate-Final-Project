import kirby
import pygame
import time

LIFE = 5


class Player:
    def __init__(self, x, y, length, num, amp):
        self.x = x
        self.y = y
        self.length = length  # the size of the character
        self.num = num  # the number of the player(1 or 2)
        self.life = LIFE
        self.anm = 0  # rest
        self.inAir = 0  # if the player is on ground this equals to 0
        self.hit = 0  # if the other player was hit this equals to 1
        self.atk = 0  # this equals 1 if the enemy was hit by the player
        self.amp = amp

    def moveLeft(self, n, win):
        """
        the player moves left. while the A button on the keyboard is being held,
        the player will keep moving left.
        :param n: the network
        :param win: the window/screen
        :return: the direction that the player is facing
        """
        anm = 1
        con = True
        direction = 1

        while con:
            time.sleep(0.04)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    con = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    return self.moveRight(n, win)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.moveJump(n, 1, win)
                    return direction

            if checkForObstacle(self.x - 10, self.y):
                self.x -= 10

            self.anm = anm
            self.print_sequence(n, win)
            anm += 1
            if anm == 9:
                anm = 1
        return direction

    def moveRight(self, n, win):
        """the player moves right"""
        anm = 9
        con = True
        direction = 0

        while con:
            time.sleep(0.04)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP and event.key == pygame.K_d:
                    con = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    return self.moveLeft(n,win)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.moveJump(n,0,win)
                    return direction

            if checkForObstacle(self.x+10, self.y):
                self.x += 10

            self.anm = anm
            self.print_sequence(n, win)
            anm += 1
            if anm == 17:
                anm = 9
        return direction

    def moveJump(self, n, dir, win):
        """
        the player jumps, in the jump there are 3 times going up and 3 times down
        unless it went up less than 3 times duo to an obstacle
        """
        cnt = 0
        rise = 0  # the number of times the character went up
        anm = 17
        amp = 0
        if dir == 0:
            amp = 9
        while anm <= 22:
            time.sleep(0.1)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        if checkForObstacle(self.x + 20, self.y):
                            self.x += 20
                    if event.key == pygame.K_a:
                        if checkForObstacle(self.x - 20, self.y):
                            self.x -= 20
                    if event.key == pygame.K_w:
                        self.flight(n, win, dir)
                        return
            if cnt < 3:
                if checkForObstacle(self.x, self.y - 20):
                    self.y -= 20
                    rise += 1
                cnt += 1
            elif cnt >= 3:
                if checkForObstacle(self.x, self.y + 20) and rise > 0:
                    self.y += 20
                    rise -= 1

            self.anm = anm + amp
            self.print_sequence(n, win)
            anm += 1

    def moveDown(self, n, dir, win):
        """the player ducks"""
        con = True
        anm = 23
        amp = 0
        if dir == 0:
            amp = 9
        while con:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.slide_right(n, win)
                    if event.key == pygame.K_a:
                        self.slide_left(n, win)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_s:
                        con = False

            self.anm = anm + amp
            self.print_sequence(n, win)

    def slide_left(self, n, win):
        self.anm = 24
        facing = 0
        for x in range(0, 3):
            if checkForObstacle(self.x - 10, self.y):
                self.x -= 10

            e1 = n.send('1')
            if compare_positions(self.x, self.y, self.length, e1.x, e1.y, e1.length):
                self.atk = 1

            p2 = n.send(self)
            if p2.hit == 1:
                if e1.x > self.x:
                    facing = 1
                self.damaged(n, win, facing)
                return
            # print sequence
            kirby.drawField(0, win, self.life)
            if p2.life > 0:
                kirby.drawKirby(p2.x, p2.y, p2.anm + p2.amp, win)
            kirby.drawEnm1(e1.x, e1.y, e1.anm, e1.wh, win)
            if self.life > 0:
                kirby.drawKirby(self.x, self.y, self.anm + self.amp, win)

            self.atk = 0
            time.sleep(0.05)

    def slide_right(self, n, win):
        self.anm = 25
        facing = 0
        for x in range(0, 3):
            if checkForObstacle(self.x + 10, self.y):
                self.x += 10

            e1 = n.send('1')
            if compare_positions(self.x, self.y, self.length, e1.x, e1.y, e1.length):
                self.atk = 1

            p2 = n.send(self)
            if p2.hit == 1:
                if e1.x > self.x:
                    facing = 1
                self.damaged(n, win, facing)
                return
            # print sequence
            kirby.drawField(0, win, self.life)
            if p2.life > 0:
                kirby.drawKirby(p2.x, p2.y, p2.anm + p2.amp, win)
            kirby.drawEnm1(e1.x, e1.y, e1.anm, e1.wh, win)
            if self.life > 0:
                kirby.drawKirby(self.x, self.y, self.anm + self.amp, win)

            self.atk = 0
            time.sleep(0.05)

    def flight(self, n, win, dir):
        """
        the player enters to flight mode, meaning he will fall to the ground over time.
        in flight mode the player can move in all directions and can be attacked
        :param n: the network
        :param win: the window
        :param dir: the direction that the player is facing
        :return: the direction that the player is facing
        """
        if dir == 1:
            anm = 37
        else:
            anm = 34

        floor = 500
        self.inAir = 1
        con1 = 0
        con2 = 0
        con3 = 0
        con4 = 1

        while self.inAir:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        con1 = 1
                        if dir == 1:
                            anm = 34
                        dir = 0
                    if event.key == pygame.K_a:
                        con2 = 1
                        if dir == 0:
                            anm = 37
                        dir = 1
                    if event.key == pygame.K_s:
                        con3 = 1
                    if event.key == pygame.K_w:
                        con4 = 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        con1 = 0
                    if event.key == pygame.K_a:
                        con2 = 0
                    if event.key == pygame.K_s:
                        con3 = 0
                    if event.key == pygame.K_w:
                        con4 = 0

            if con1:
                if checkForObstacle(self.x + 20, self.y):
                    self.x += 20
            if con2:
                if checkForObstacle(self.x - 20, self.y):
                    self.x -= 20
            if con3:
                if checkForObstacle(self.x, self.y + 20):
                    self.y += 20
            if con4:
                if checkForObstacle(self.x, self.y - 40):
                    self.y -= 40

            self.anm = anm
            self.y = checkAir(self.y, 1)
            if self.y == floor:
                self.inAir = 0

            self.print_sequence(n, win)

            time.sleep(0.05)
            if anm == 36:
                anm = 34
            elif anm == 39:
                anm = 37
            anm += 1

    def damaged(self, n, win, facing):
        """
        the player was hit, his life is decreased by 1 and he is pushed back
        :param n: the network
        :param win: the window
        :param facing: the direction that the player is facing
        """
        self.life -= 1
        self.anm = 40
        self.hit = 0

        if facing == 0:
            for x in range(0, 3):
                if checkForObstacle(self.x + 20, self.y):
                    self.x += 20

                self.print_sequence(n, win)
                time.sleep(0.05)
        else:
            self.anm += 1
            for x in range(0, 3):
                if checkForObstacle(self.x - 20, self.y):
                    self.x -= 20

                self.print_sequence(n, win)
                time.sleep(0.05)

    def print_sequence(self, n, win):
        """
        the function calls the functions that prints the screen, p1, p2 and the enemy
        :param n: the network
        :param win: the window
        """
        facing = 0
        p2 = n.send(self)
        e1 = n.send('1')
        if p2.hit == 1:
            if e1.x > self.x:
                facing = 1
            self.damaged(n, win, facing)
            return
        kirby.drawField(0, win, self.life)
        if self.life > 0:
            kirby.drawKirby(self.x, self.y, self.anm + self.amp, win)
        if p2.life > 0:
            kirby.drawKirby(p2.x, p2.y, p2.anm + p2.amp, win)
        kirby.drawEnm1(e1.x, e1.y, e1.anm, e1.wh, win)


def compare_positions(x1, y1, len1, x2, y2, len2):
    """
    the function checks if two characters are one inside another
    """
    if x1 <= x2 <= x1 + len1 and y1 <= y2 <= y1 + len1:
        return 1
    elif x1 <= x2 + len2 <= x1 + len1 and y1 <= y2 <= y1 + len1:
        return 1
    elif x1 <= x2 <= x1 + len1 and y1 <= y2 + len2 <= y1 + len1:
        return 1
    elif x1 <= x2 + len2 <= x1 + len1 and y1 <= y2 + len2 <= y1 + len1:
        return 1
    else:
        return 0


def checkForObstacle(x, y):
    """
    checks if the player or com can fit to a location.
    """
    floor = 500

    if (x > 760 or x < 0) or (y > floor or y < 0):
        return 0  # does not fit to the location
    else:
        return 1


def checkAir(y, l):
    """
    :param y: the y position
    :param l: the level (1 - 3)
    :return: if the player is in air or not, if it is return the y value after the height drop
    """
    floor = 500
    if y + 20 > floor:
        return floor
    return y + 20


def checkForMove(p, n, facing, win):
    """
    :param p: the player
    :param n: the network
    :param win: the window, gameDisplay
    :param facing: the direction that the player is facing
    the function checks if a key is being pressed
    :return the direction that the player is facing 0 for right, 1 for left
    """
    keys = pygame.key.get_pressed()
    direction = facing

    if keys[pygame.K_a]:
        direction = p.moveLeft(n, win)

    if keys[pygame.K_d]:
        direction = p.moveRight(n, win)

    if keys[pygame.K_SPACE]:
        p.moveJump(n, direction, win)

    if keys[pygame.K_s]:
        p.moveDown(n, direction, win)

    return direction
