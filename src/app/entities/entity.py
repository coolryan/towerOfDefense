import arcade, math

class Player:
    def __init__(self):
        self.lives = 20
        self.gold = 100

class Enemy(arcade.Sprite):
    def __init__(self, name, path, path_index: int = 0, 
                health: int = 50, max_health: int = 50, speed: float = 2.0):
        super().__init__(":resources:images/alien/alienBlue_sq1.png", scale=0.5) # placeholder asset
        self.name = name
        self.path = path
        self.speed = speed
        self.path_index, self.health, self.max_health = path_index, health, max_health
        self.x, self.y = path[0]
        self.active = True
        
    def update(self):
        if not self.active:
            return

        target_x, target_y = self.path[self.path_index]
        dx, dy = target_x - self.x, target_y - self.y
        distance = math.hypot(dx, dy)

        if distance < self.speed:
            self.x, self.y = target_x, target_y
            self.path_index += 1

            if self.path_index >= len(self.path):
                self.active = False # Reached the end
        else:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance

    def draw(self):
        if self.active:
            arcade.draw_circle_filled(self.x, self.y, 12, arcade.color.RED)

class Tower(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/tiles/brickGrey.png", scale=0.75)
        self.x, self.y = x, y
        self.range, self.damage, self.cooldown = 150, 10, 0

    def update(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        for enemy in enemies:
            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)

            if dist <= self.range:
                enemy.health -= self.damage
                self.cooldown = 30 # wait frames before next shot

                if enemy.health <= 0:
                    enemy.active = False
                break

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, 20, arcade.color.BLUE)
        arcade.draw_circle_outline(self.x, self.y, self.range, arcade.color.LIGHT_BLUE, 2)
