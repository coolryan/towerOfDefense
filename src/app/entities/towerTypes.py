from enum import Enum
import arcade

# Base stats container
class TowerStats:
    def __init__(
        self,
        name: str,
        cost: int,
        damage: float,
        range: float,
        cooldown: float,
        color,
        slow_duration: float = 0.0,
        sound_speed: float = 1.0,
    ):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.range = range
        self.cooldown = cooldown  # seconds between shots
        self.color = color  # tints the tower and its laser bolts
        self.slow_duration = slow_duration  # seconds a hit slows the enemy (0 = no slow)
        self.sound_speed = sound_speed  # laser sound pitch: below 1 is deeper, above 1 is higher

# Tower types, in the order of the number keys that select them (1, 2, 3, ...).
# Skeletons have 40-50 hp at level 1 and 3x that at level 2.
class TowerType(Enum):
    BASIC = TowerStats("Basic", cost=50, damage=20, range=200, cooldown=0.75,
                       color=arcade.color.WHITE)
    HEAVY = TowerStats("Heavy", cost=100, damage=60, range=170, cooldown=2.0,
                       color=arcade.color.ORANGE_RED, sound_speed=0.6)
    RAPID = TowerStats("Rapid", cost=75, damage=8, range=180, cooldown=0.25,
                       color=arcade.color.YELLOW, sound_speed=1.5)
    SNIPER = TowerStats("Sniper", cost=120, damage=80, range=400, cooldown=2.5,
                        color=arcade.color.PURPLE, sound_speed=0.8)
    FROST = TowerStats("Frost", cost=80, damage=5, range=180, cooldown=1.0,
                       color=arcade.color.LIGHT_BLUE, slow_duration=2.0, sound_speed=1.2)
