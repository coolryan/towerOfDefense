import arcade, math, random
from pathlib import Path
from entities.enemyTypes import SkeletonType

# constant
BULLET_SPEED = 7.0
BASE_GOLD_REWARD = 25

RESOURCES_DIR = Path(__file__).resolve().parents[3] / "resources"

SKELETON_IMAGES = {
    SkeletonType.WARRIOR: "images/warriors/skeleton_warriors/skeleton_warrior.png",
    SkeletonType.ARCHER: "images/warriors/skeleton_warriors/skeleton-archer.png",
}

# Each source image is a different resolution with a different amount of
# transparent padding, so scale is tuned per-type to match on-screen
# character size, not raw canvas size (the archer's canvas has almost no
# padding, while the warrior's has a lot).
SKELETON_SCALES = {
    SkeletonType.WARRIOR: 0.107,
    SkeletonType.ARCHER: 0.0251,
}

class Player:
    def __init__(self):
        self.lives = 20
        self.gold = 100

class Enemy(arcade.Sprite):
    def __init__(self, path, skeleton_type: SkeletonType | None = None, level: int = 1):
        skeleton_type = skeleton_type or random.choice(list(SkeletonType))
        super().__init__(
            str(RESOURCES_DIR / SKELETON_IMAGES[skeleton_type]),
            SKELETON_SCALES[skeleton_type],
        )
        self.path = path
        self.path_index = 0
        self.skeleton_type = skeleton_type
        self.level = level

        # Stats
        stats = self.skeleton_type.value
        self.max_health = float(stats.hp)
        self.health = self.max_health
        self.speed = float(stats.speed)
        # Stronger enemy types and higher levels are worth more gold on kill.
        self.gold_value = round(BASE_GOLD_REWARD * stats.gold_multiplier * self.level)

        # State
        self.is_slowed = False
        self.slow_timer = 0.0

        # Position at start of path
        if self.path:
            self.center_x, self.center_y = self.path[0]
        
    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        # handle slow effect duration
        if self.is_slowed:
            self.slow_timer -= delta_time
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

        arcade.draw_rect_filled(arcade.XYWH(x, y, bar_width, bar_height), arcade.color.RED)

        # draw current health foreground
        current_width = bar_width * (self.health / self.max_health)
        arcade.draw_rect_filled(
            arcade.XYWH(x - (bar_width - current_width) / 2, y, current_width, bar_height),
            arcade.color.GREEN
        )

class Projectile:
    """A laser bolt fired by the tower, drawn as a line rather than a sprite so it
    always points exactly along its real direction of travel."""

    LENGTH = 20.0
    COLOR = arcade.color.GREEN
    LINE_WIDTH = 3

    def __init__(self, start_x, start_y, target):
        self.center_x, self.center_y = start_x, start_y
        self.target = target
        self.speed = BULLET_SPEED
        self.alive = True
        self.gold_reward = 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        # Check if target still exists (kill() removes it from all sprite lists)
        if not self.target.sprite_lists:
            self.alive = False
            return

        # Move toward target position
        dx = self.target.center_x - self.center_x
        dy = self.target.center_y - self.center_y
        distance = math.hypot(dx, dy)

        if distance < self.speed:
            # hit target
            self.gold_reward = self.target.gold_value
            self.target.remove_from_sprite_lists() # or real damage
            self.alive = False
        else:
            self.center_x += (dx / distance) * self.speed
            self.center_y += (dy / distance) * self.speed

    def draw(self):
        dx = self.target.center_x - self.center_x
        dy = self.target.center_y - self.center_y
        distance = math.hypot(dx, dy) or 1.0

        tail_x = self.center_x - (dx / distance) * self.LENGTH
        tail_y = self.center_y - (dy / distance) * self.LENGTH
        arcade.draw_line(tail_x, tail_y, self.center_x, self.center_y, self.COLOR, self.LINE_WIDTH)

class Tower(arcade.Sprite):
    """Tower with range, rotation, cooldowns & targeting logoc"""
    def __init__(self, x, y):
        super().__init__(str(RESOURCES_DIR / "images/tiles/towerDefense_tile250.png"), 0.18)
        self.center_x, self.center_y = x, y
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

    def shoot(self, target, projectile_list):
        """Spawns a new projectile if cooldown is ready"""
        if self.cooldown_timer <= 0:
            bullet = Projectile(self.center_x, self.center_y + self.height / 2, target)
            projectile_list.append(bullet)
            self.cooldown_timer = self.cooldown_max

    def on_update(self, delta_time, enemies, projectile_list):
        """Updates cooldown & handles targeting/firing behavor"""
        if self.cooldown_timer > 0:
            self.cooldown_timer -= delta_time

        target = self.update_target(enemies)
        if target:
            self.shoot(target, projectile_list)

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, 20, arcade.color.BLUE)
        arcade.draw_circle_outline(self.x, self.y, self.range, arcade.color.LIGHT_BLUE, 2)
