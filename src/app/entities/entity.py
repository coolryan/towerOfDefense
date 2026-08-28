import arcade, math

# constant
BULLET_SPEED = 7.0

class Player:
    def __init__(self):
        self.lives = 20
        self.gold = 100

class Enemy(arcade.Sprite):
    def __init__(self, path):
        super().__init__("character.png", 0.5) # use your sprite image path
        self.path = path
        self.path_index = 0

        # Stats
        self.max_health = 150.0
        self.health = self.max_health
        self.speed, self.gold_value = 2.0, 25

        # State
        self.is_slowed = False
        self.slow_timer = 0.0

        # Position at start of path
        if self.path:
            self.center_x, self.center_y = self.path[0]
        
    def update(self):
        # hnalde slow effect duration
        if self.is_slowed:
            self.slow_timer -= 1 / 60
            if self.slow_timer <= 0:
                self.is_slowed = False

        # move along path
        if self.path_index < len(self.path):
            target_x, target_y = self.path[self.path_index]
            dx = target_x - self.center_x
            dy = target_y - self.center_y
            distance = math.hypot(dx, dy)

            current_speed = self.speed * 0.5 if self.is_slowed else self.speed

            if distance <= current_speed:
                # snap tp waypoint & target next one
                self.center_x, self.center_y = target_x, target_y
                self.path_index += 1
            else:
                # move towards waypoint
                self.center_x += (dx / distance) * current_speed
                self.center_y += (dy / distance) * current_speed

    def apply_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def apply_slow(self, duration):
        self.is_slowed = False
        self.slow_timer = duration

    def draw_health_bar(self):
        # draw background bar
        bar_width, bar_height = 40, 6
        x, y = self.center_x, self.center_y + 30

        arcade.draw_rect_filled(x, y, bar_width, bar_height, arcade.color.RED)

        # draw current health foreground
        current_width = bar_width * (self.health / self.max_health)
        arcade.draw_rect_filled(
            x - (bar_width - current_width) / 2,
            y,
            current_width,
            bar_height,
            arcade.color.GREEN
        )

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
        """Updates cooldown & handles targeting/firing behavor"""
        if self.cooldown_timer > 0:
            self.cooldown_timer -= delta_time

        target = self.update_target(enemies)
        if target:
            self.rotate_towards(target)
            self.shoot(target, projectile_list)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, 20, arcade.color.BLUE)
        arcade.draw_circle_outline(self.x, self.y, self.range, arcade.color.LIGHT_BLUE, 2)
