import arcade, math

# constant
BULLET_SPEED = 7.0

class Player:
    def __init__(self):
        self.lives = 20
        self.gold = 100

class Enemy(arcade.Sprite):
    def __init__(self, name, path, path_index: int = 0, 
                health: int = 50, max_health: int = 50, speed: float = 2.0):
        super().__init__(path=":resources:images/alien/alienBlue_square.png", scale=0.5) # placeholder asset
        self.name = name
        self.path = path
        self.speed = speed
        self.path_index, self.health, self.max_health = path_index, health, max_health
        self.x, self.y = 10, 10
        self.active = True
        
    def update(self, delta_time):
        if not self.active:
            return

        # target_x, target_y = 0, 0
        # dx, dy = target_x - self.x, target_y - self.y
        # distance = math.hypot(dx, dy)

        # if distance < self.speed:
        #     self.x, self.y = target_x, target_y
        #     self.path_index += 1

        #     if self.path_index >= len(self.path):
        #         self.active = False # Reached the end
        # else:
        #     self.x += self.speed * dx / distance
        #     self.y += self.speed * dy / distance

    def draw(self):
        if self.active:
            arcade.draw_circle_filled(self.x, self.y, 12, arcade.color.RED)

class Projectile(arcade.Sprite):
    """ Basic projectile fired by the tower."""
    def __init__(self, start_x, start_y, target):
        super().__init__(":resources:images/space_shades/laserGreen01.png", 0.5)
        self.center_x, self.center_y = start_x, start_y
        self.target = target
        self.speed = BULLET_SPEED

    def update(self):
        # Check if target still exists
        if (
            self.target.dead
            or not self.target.scalers
            and hasattr(self.target, "alpha")
            and self.target.alpha == 0
        ):
            self.remove_from_sprite_lists()
            return

        # Move toward target position
        dx = self.target.center_x - self.center_x
        dy = self.target.center_y = self.center_y
        distance = math.hypot(dx, dy)

        if distance < self.speed:
            # hit target
            self.target.remove_from_sprite_lists() # or real damage
            self.remove_from_sprite_lists()
        else:
            self.center_x += (dx / distance) * self.speed
            self.center_y += (dx / distance) * self.speed

class Tower(arcade.Sprite):
    """Tower with range, rotation, cooldowns & targeting logoc"""
    def __init__(self, x, y):
        super().__init__(":resources:images/tiles/towerDefense_tile250.png", 0.8)
        self.x, self.y = x, y
        self.range, self.cooldown_max, self.cooldown_timer = 200.0, 0.75, 0.0 # seconds between attacks
        self.targeting_mode = "FIRST" # Options: 'FIRST', 'CLOSEST'

    def update_target(self, enemies):
        """Finds the best target based on targeting mode"""
        valid_enemies = []

        for enemy in enemies:
            dist = math.hypot(
                self.center_x - enemy.center_x, self.center_y - enemy.center_y
            )
            if dist <= self.range:
                valid_enemies.append((dist, enemy))

        if not valid_enemies:
            return None

        if self.targeting_mode == "CLOSEST":
            # Sort by distance (smallest first)
            valid_enemies.sort(key=lambda item: item[0])
            return valid_enemies[0][1]
        elif self.targeting_mode == "FIRST":
            # Assuming enemies have a 'path_progress' or similar metric
            # Fallback to closest if path progress is unavailable
            return valid_enemies[0][1]

        return None

    def rotate_towards(self, target):
        """Smoothly rotates the tower sprite to face the target"""
        if not target:
            return

        dx = target.center_x - self.center_x
        dy = target.center_y = self.center_y
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)

        # adjust based on base sprite orientation (subtract 90 if pointing up)
        self.angle = angle_deg - 90

    def shoot(self, target, projectile_list):
        """Spawns a new projectile if cooldown is ready"""
        if self.cooldown_timer <= 0:
            bullet = Projectile(self.center_x, self.center_y, target)
            projectile_list.append(bullet)
            self.cooldown_timer = self.cooldown_max

    def on_update(self, delta_time, enemies, projectile_list):
        """Updates cooldown & handles targeting/firsting behavor"""
        if self.cooldown_timer > 0:
            self.cooldown_timer -= delta_time

        target = self.update_target(enemies)
        if target:
            self.rotate_towards(target)
            self.shoot(target, projectile_list)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, 20, arcade.color.BLUE)
        arcade.draw_circle_outline(self.x, self.y, self.range, arcade.color.LIGHT_BLUE, 2)
