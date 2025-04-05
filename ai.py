import time
import player

LIFE = 15
players = [player.Player(0, 500, 40, 1, 0), player.Player(400, 500, 40, 2, 42)]


class AI:
    def __init__(self, x, y, length, num):
        self.x = x
        self.y = y
        self.length = length  # the size of the character
        self.num = num  # the number of the AI(1, 2 or 3)
        self.target = 1  # the player who the AI is after
        self.life = LIFE
        self.anm = 1
        self.wh = 0  # the position of the weapon
        self.printed1 = 0  # this equals 1 if the enemy was printed by player 1
        self.printed2 = 0  # this equals 1 if the enemy was printed by player 2
        self.p1Hit = 0  # this equals 1 if the enemy hit player 1
        self.p2Hit = 0  # this equals 1 if the enemy hit player 2

    def attackLeft(self, step, target, other):
        """
        acts according to the step
        :param step: the next step in the AI's attack sequence
        :param target: the target player
        :param other: the other player
        :return: if the target player was hit
        """
        if step == 15:
            self.anm = 11
        elif step >= 10:
            self.anm = 10
            self.wh = step - self.anm
        else:
            self.anm = step

        hit = False
        if step < 7:
            if player.checkForObstacle(self.x - 10, self.y):
                self.x -= 10

        if step == 8 or step == 9:  # check if one of the players is at the same position as the AI
            if player.compare_positions(self.x, self.y, self.length, target.x, target.y, target.length):
                hit = True
                if target.num == 1:
                    self.p1Hit = 1 # updates that the player was hit
                else:
                    self.p2Hit = 1

            if player.compare_positions(self.x, self.y, self.length, other.x, other.y, other.length):
                if other.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1

        if step == 10 or step == 14:  # check if one of the players is at the same position as the weapon
            if player.compare_positions(self.x - 50, self.y, self.length, target.x, target.y, target.length):
                hit = True
                if target.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1
            if player.compare_positions(self.x - 50, self.y, self.length, other.x, other.y, other.length):
                if other.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1

        if step == 11 or step == 13:
            if player.compare_positions(self.x - 100, self.y, self.length, target.x, target.y, target.length):
                hit = True
                if target.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1
            if player.compare_positions(self.x - 100, self.y, self.length, other.x, other.y, other.length):
                if other.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1

        if step == 12:
            if player.compare_positions(self.x - 150, self.y, self.length, target.x, target.y, target.length):
                hit = True
                if target.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1
            if player.compare_positions(self.x - 150, self.y, self.length, other.x, other.y, other.length):
                if other.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1

        return hit

    def attackRight(self, step, target, other):
        """
        acts according to the step
        :param step: the next step in the AI's attack sequence
        :param target: the target player
        :param other: the other player
        :return: if the target player was hit
        """
        if step == 15:
            self.anm = 22
        elif step >= 10:
            self.anm = 21
            self.wh = step - self.anm + 11
        else:
            self.anm = step + 11

        hit = False
        if step < 7:
            if player.checkForObstacle(self.x + 10, self.y):
                self.x += 10

        if step == 8 or step == 9:  # check if one of the players is at the same position as the AI
            if player.compare_positions(self.x, self.y, self.length, target.x, target.y, target.length):
                hit = True
                if target.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1

            if player.compare_positions(self.x, self.y, self.length, other.x, other.y, other.length):
                if other.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1

        if step == 10 or step == 14:  # check if one of the players is at the same position as the weapon
            if player.compare_positions(self.x + 50, self.y, self.length, target.x, target.y, target.length):
                hit = True
                if target.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1
            if player.compare_positions(self.x + 50, self.y, self.length, other.x, other.y, other.length):
                if other.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1

        if step == 11 or step == 13:
            if player.compare_positions(self.x + 100, self.y, self.length, target.x, target.y, target.length):
                hit = True
                if target.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1
            if player.compare_positions(self.x + 100, self.y, self.length, other.x, other.y, other.length):
                if other.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1

        if step == 12:
            if player.compare_positions(self.x + 150, self.y, self.length, target.x, target.y, target.length):
                hit = True
                if target.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1
            if player.compare_positions(self.x + 150, self.y, self.length, other.x, other.y, other.length):
                if other.num == 1:
                    self.p1Hit = 1  # updates that the player was hit
                else:
                    self.p2Hit = 1

        return hit

    def damaged(self, facing):
        """
        the AI was hit, the function decreases the life by 1 and moves the AI back 3 times
        :param facing: the direction of the hit
        """
        anm = 23
        self.life -= 1
        if facing == 0:
            self.anm = anm + 1
            for x in range(0, 3):
                if player.checkForObstacle(self.x - 20, self.y):
                    self.x -= 20
                    while self.printed1 == 0 and self.printed2 == 0:
                        pass
                    self.printed1 = 0
                    self.printed2 = 0
        else:
            self.anm = anm
            for x in range(0, 3):
                if player.checkForObstacle(self.x + 20, self.y):
                    self.x += 20
                    while self.printed1 == 0 and self.printed2 == 0:
                        pass
                    self.printed1 = 0
                    self.printed2 = 0


def move(enemy):
    """
    the function is the main loop for the AI. it calls the other functions
    that calculate the position of the AI and whether or not he hit one of
    the players.
    :param enemy: the AI object
    """
    cnt = 1  # the next step to perform
    hit = False
    facing = 0

    while enemy.life > 0:
        p1 = players[0]
        p2 = players[1]

        if p1.atk == 1:  # check for each player if the AI was hit by them
            if p1.x > enemy.x:
                facing = 1
            enemy.damaged(facing)
            p1.atk = 0

        elif p2.atk == 1:
            if p2.x > enemy.x:
                facing = 1
            enemy.damaged(facing)
            p2.atk = 0

        elif enemy.target == 1:  # it the target player is 1, follow and attack him
            if enemy.x > p1.x:
                hit = enemy.attackLeft(cnt, p1, p2)
            else:
                hit = enemy.attackRight(cnt, p1, p2)

            if hit:
                enemy.target = 2  # if the target player was hit, change the target
                cnt = 1

        elif enemy.target == 2:  # it the target player is 2, follow and attack him
            if enemy.x > p2.x:
                hit = enemy.attackLeft(cnt, p2, p1)
            else:
                hit = enemy.attackRight(cnt, p2, p1)

            if hit:
                enemy.target = 1
                cnt = 1

        if enemy.p1Hit == 1:  # checks if the enemy hit one of the players
            p2.hit = 1
            enemy.p1Hit = 0
        if enemy.p2Hit == 1:
            p1.hit = 1
            enemy.p2Hit = 0

        if cnt == 16:  # last step is 15 then, repeat all steps
            cnt = 1
        else:
            cnt += 1

        while enemy.printed1 == 0 or enemy.printed2 == 0:  # wait until both players print the AI
            time.sleep(0.08)  # check every 0.08 sec
        enemy.printed1 = 0
        enemy.printed2 = 0
