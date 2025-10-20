import time
import player
import random

LIFE = 15
players = [player.Player(0, 410, 60, 1, 0), player.Player(400, 410, 60, 2, 42)]


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

        # New behavior properties
        self.behavior_type = 1  # Behavior type (1, 2, or 3)
        self.is_throwing = False  # Currently throwing weapon
        self.throw_cooldown = 0  # Frames until can throw again
        self.throw_frame = 0  # Current frame of throw animation
        self.throw_direction = 1  # 1 = right, -1 = left
        self.throw_distance = 0  # Distance weapon will travel
        self.throw_target = None  # Target player for current throw
        self.patrol_direction = 1  # 1 = right, -1 = left for roaming
        self.velocityX = 2  # Horizontal movement speed
        self.facing = 0  # 0 = left, 1 = right
        self.immunity_frames = 0  # frames of immunity remaining (1 second = 30 frames)
        self.weapon_spin = 1  # Alternates 1-2 for spinning animation
        self.touch_damage_p1 = 0  # AI touched player 1
        self.touch_damage_p2 = 0  # AI touched player 2
        self.preferred_target = 1  # Which player to focus on (1 or 2)
        self.optimal_distance = 175  # Maintain 150-200px range (middle: 175px)
        self.distance_tolerance = 25  # ±25px gives 150-200px range
        self.stun_frames = 0  # Frames to remain stunned after damage

    def maintain_distance_behavior(self):
        """
        AI maintains optimal throwing distance (150-200px) from preferred target.
        Moves closer if too far, backs away if too close.
        """
        p1, p2 = players[0], players[1]

        # Determine target based on preferred_target
        target = None
        if self.preferred_target == 1 and p1.life > 0:
            target = p1
        elif self.preferred_target == 2 and p2.life > 0:
            target = p2
        elif p1.life > 0:  # Fallback if preferred target is dead
            target = p1
            self.preferred_target = 1
        elif p2.life > 0:
            target = p2
            self.preferred_target = 2

        if target:
            distance = abs(self.x - target.x)

            # Check if distance is outside optimal range
            if distance > self.optimal_distance + self.distance_tolerance:
                # Too far - move closer (toward target)
                if self.x < target.x:
                    new_x = self.x + 4
                    if player.checkForObstacle(new_x, self.y):
                        self.x = new_x
                    self.facing = 1
                    frame = (int(self.x / 10) % 11)
                    self.anm = 12 + frame
                else:
                    new_x = self.x - 4
                    if player.checkForObstacle(new_x, self.y):
                        self.x = new_x
                    self.facing = 0
                    frame = (int(self.x / 10) % 11)
                    self.anm = 1 + frame

            elif distance < self.optimal_distance - self.distance_tolerance:
                # Too close - back away (opposite direction from target)
                if self.x < target.x:
                    # Target is to the right, back away left
                    new_x = self.x - 4
                    if player.checkForObstacle(new_x, self.y):
                        self.x = new_x
                    self.facing = 0  # Face left while backing away
                    frame = (int(self.x / 10) % 11)
                    self.anm = 1 + frame
                else:
                    # Target is to the left, back away right
                    new_x = self.x + 4
                    if player.checkForObstacle(new_x, self.y):
                        self.x = new_x
                    self.facing = 1  # Face right while backing away
                    frame = (int(self.x / 10) % 11)
                    self.anm = 12 + frame
            else:
                # Within optimal range - stand still but face target
                if self.x < target.x:
                    self.facing = 1
                    self.anm = 12  # Idle facing right
                else:
                    self.facing = 0
                    self.anm = 1  # Idle facing left

    def check_throw_range(self, p1, p2):
        """
        Check if any player is within throw range
        Returns (player, distance) if in range, else (None, 0)
        """
        # Calculate distances to both players
        dist_p1 = abs(self.x - p1.x)
        dist_p2 = abs(self.x - p2.x)

        # Throw range: 100 to 350 pixels
        MIN_RANGE = 100
        MAX_RANGE = 350

        # Check which player is in range (prefer closer one)
        target = None
        distance = 0

        if MIN_RANGE <= dist_p1 <= MAX_RANGE and p1.life > 0:
            target = p1
            distance = dist_p1

        if MIN_RANGE <= dist_p2 <= MAX_RANGE and p2.life > 0:
            if target is None or dist_p2 < distance:
                target = p2
                distance = dist_p2

        return target, distance

    def throw_weapon(self, target):
        """
        Throw weapon at target with random range variation
        """
        self.is_throwing = True
        self.throw_frame = 0
        self.throw_target = target
        self.velocityX = 0  # Stop moving

        # Determine throw direction
        self.throw_direction = 1 if target.x > self.x else -1
        self.facing = 1 if self.throw_direction > 0 else 0

        # Randomly select throw distance: short, medium, or long
        distance_type = random.choice(['short', 'medium', 'long'])

        if distance_type == 'short':
            self.throw_distance = random.randint(100, 150)
            self.throw_max_frames = 20  # 10 frames out, 10 back (slower)
        elif distance_type == 'medium':
            self.throw_distance = random.randint(150, 250)
            self.throw_max_frames = 32  # 16 frames out, 16 back (slower)
        else:  # long
            self.throw_distance = random.randint(250, 350)
            self.throw_max_frames = 48  # 24 frames out, 24 back (slower)

    def continue_throw(self, p1, p2):
        """
        Continue the throw animation and check for hits.
        Smoothly animates weapon trajectory out and back.
        """
        self.throw_frame += 1
        half_frames = self.throw_max_frames // 2

        # Calculate weapon position with smooth interpolation
        if self.throw_frame <= half_frames:
            # Weapon going out
            progress = self.throw_frame / half_frames
            weapon_distance = int(self.throw_distance * progress)
        else:
            # Weapon returning
            progress = (self.throw_max_frames - self.throw_frame) / half_frames
            weapon_distance = int(self.throw_distance * progress)

        # Calculate weapon spin animation (alternates every 5 frames)
        self.weapon_spin = ((self.throw_frame // 5) % 2) + 1  # 1 or 2 for WH1/WH2

        # Map weapon distance to discrete wh values for rendering
        # wh=1 at 50px, wh=2 at 100px, wh=3 at 150px, wh=4 at 100px (return), wh=5 at 50px (return)
        if self.throw_frame <= half_frames:
            # Going out
            if weapon_distance >= 125:
                self.wh = 3  # Far position (150px)
            elif weapon_distance >= 75:
                self.wh = 2  # Medium position (100px)
            elif weapon_distance >= 25:
                self.wh = 1  # Close position (50px)
            else:
                self.wh = 0  # Very close / starting
        else:
            # Coming back
            if weapon_distance >= 125:
                self.wh = 3  # Far position (150px)
            elif weapon_distance >= 75:
                self.wh = 4  # Medium position returning (100px)
            elif weapon_distance >= 25:
                self.wh = 5  # Close position returning (50px)
            else:
                self.wh = 0  # Very close / ending

        # Set throw animation based on facing direction
        if self.facing == 1:
            self.anm = 21  # Throwing right
        else:
            self.anm = 10  # Throwing left

        # Calculate weapon position in world space
        weapon_x = self.x + (weapon_distance * self.throw_direction)

        # Check collision with both players using 40px hitbox (reduced from 60px)
        if player.compare_positions(weapon_x, self.y, 40, p1.x, p1.y, p1.length):
            if self.p1Hit == 0:  # Only hit once per throw
                self.p1Hit = 1
        if player.compare_positions(weapon_x, self.y, 40, p2.x, p2.y, p2.length):
            if self.p2Hit == 0:  # Only hit once per throw
                self.p2Hit = 1

        # Check if throw complete
        if self.throw_frame >= self.throw_max_frames:
            self.is_throwing = False
            self.throw_cooldown = 60  # Cooldown frames before next throw (2 seconds at 30 FPS)
            self.wh = 0
            self.velocityX = 2  # Resume walking
            self.patrol_direction = self.throw_direction  # Continue in throw direction

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
        Only applies damage if immunity_frames is 0 (not immune)
        :param facing: the direction of the hit
        """
        # Check immunity - if immune, ignore damage
        if self.immunity_frames > 0:
            return

        anm = 23
        self.life -= 1
        self.immunity_frames = 30  # 1 second immunity at 30 FPS
        self.stun_frames = 30  # 1 second stun at 30 FPS
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
    Frame-based state machine for AI behavior.
    Supports multiple behavior types with smooth animations.
    :param enemy: the AI object
    """
    while enemy.life > 0:
        p1 = players[0]
        p2 = players[1]

        # Priority 1: Handle damage state
        if p1.atk == 1:
            facing = 1 if p1.x > enemy.x else 0
            enemy.damaged(facing)
            p1.atk = 0

        elif p2.atk == 1:
            facing = 1 if p2.x > enemy.x else 0
            enemy.damaged(facing)
            p2.atk = 0

        # Priority 2: Handle throwing state
        elif enemy.is_throwing:
            enemy.continue_throw(p1, p2)

        # Priority 3: Normal behavior based on type
        else:
            if enemy.behavior_type == 1:  # Player Tracker & Thrower
                # Decrement stun frames
                if enemy.stun_frames > 0:
                    enemy.stun_frames -= 1
                    # Stand still animation based on facing
                    if enemy.facing == 1:
                        enemy.anm = 12  # Idle right
                    else:
                        enemy.anm = 1  # Idle left
                else:
                    # Not stunned - normal behavior
                    # Maintain optimal throwing distance (150-200px)
                    enemy.maintain_distance_behavior()

                    # Check if AI is touching either player (collision damage)
                    # Only apply damage if player is not immune
                    if player.compare_positions(enemy.x, enemy.y, enemy.length, p1.x, p1.y, p1.length):
                        if p1.immunity_frames == 0:
                            enemy.touch_damage_p1 = 1

                    if player.compare_positions(enemy.x, enemy.y, enemy.length, p2.x, p2.y, p2.length):
                        if p2.immunity_frames == 0:
                            enemy.touch_damage_p2 = 1

                    # Decrement throw cooldown
                    if enemy.throw_cooldown > 0:
                        enemy.throw_cooldown -= 1

                    # Check for throw opportunity
                    if enemy.throw_cooldown == 0:
                        target, distance = enemy.check_throw_range(p1, p2)
                        if target and random.random() < 0.67:  # 67% chance to throw
                            enemy.throw_weapon(target)

        # Decrement immunity frames
        if enemy.immunity_frames > 0:
            enemy.immunity_frames -= 1

        # Handle hit notifications (weapon throws)
        if enemy.p1Hit == 1:
            p2.hit = 1
            enemy.p1Hit = 0
            # Alternate target after successful hit
            enemy.preferred_target = 2
        if enemy.p2Hit == 1:
            p1.hit = 1
            enemy.p2Hit = 0
            # Alternate target after successful hit
            enemy.preferred_target = 1

        # Handle touch damage notifications
        if enemy.touch_damage_p1 == 1:
            p1.hit = 1
            enemy.touch_damage_p1 = 0
            # Alternate target after successful touch damage
            enemy.preferred_target = 2
        if enemy.touch_damage_p2 == 1:
            p2.hit = 1
            enemy.touch_damage_p2 = 0
            # Alternate target after successful touch damage
            enemy.preferred_target = 1

        # Frame timing for smooth 30 FPS
        time.sleep(0.033)

        # Sync with rendering system
        while enemy.printed1 == 0 or enemy.printed2 == 0:
            time.sleep(0.01)
        enemy.printed1 = 0
        enemy.printed2 = 0
