from enum import Enum, auto

# Base stats container
class EnemyStats:
    def __init__(self, hp: int, speed: int, damage: int):
        self.hp = hp
        self.speed = speed
        self.damage = damage

# enemy types
class EnemyCategory(Enum):
    "Base category for enemy tiers"
    BASIC = auto()
    ARMORED = auto()
    BOSS = auto()
    UNDEAD = auto()
    MONSTER = auto()

class UndeadEnemy(Enum):
    SKELETON_ARMY = "Skeleton Army"
    DARK_KNIGHT = "Dark Knight"

class MonsterEnemy(Enum):
    TROLL = "Troll"
    DARK_SORCERY = "Dark Sorcery"

# Golins sub-enum
class GoblinType(Enum):
    """ sub-enums specific to the Golin family"""
    PEON = "Goblin Poem"
    WARRIOR = "Armored Goblin Warrior"
    CHIEFTAIN = "Goblin cheftain Boss"

# Dark Knights Sub-Enum
class DarkKnightType(Enum):
    FOOTMAN = EnemyStats(hp=150, speed=2, damage=10)
    ELITE_RIDER = EnemyStats(hp=300, speed=4, damage=25)

# Skeleton Armies Sub-Enum
class SkeletonType(Enum):
    WARRIOR = EnemyStats(hp=50, speed=3, damage=5)
    ARCHER = EnemyStats(hp=40, speed=3, damage=8)

# Trolls Sub-Enum
class TrollType(Enum):
    ROCK_THROWER = EnemyStats(hp=400, speed=1, damage=40)
    BRUTE = EnemyStats(hp=600, speed=1, damage=50)

# Dark Sorcery sub-Enum
class SorceryType(Enum):
    ACOLYTE = EnemyStats(hp=80, speed=2, damage=15)
    NECROMANCER = EnemyStats(hp=120, speed=2, damage=30)

# Master Enemy Faction Enum grouping them together
class EnemyFaction(Enum):
    GOBLIN_TYPE = GoblinType
    DARK_KNIGHTS = DarkKnightType
    SKELETON_ARMY = SkeletonType
    TROLLS = TrollType
    DARK_SORCERY = SorceryType

# Mapping base types to specific enemy attribuates
ENEMY_DATA = {
    GoblinType.PEON: {
        "type": EnemyCategory.BASIC,
        "hp": 50,
        "speed": 2.5,
        "gold": 10,
    },
    GoblinType.WARRIOR: {
        "type": EnemyCategory.ARMORED,
        "hp": 150,
        "speed": 1.5,
        "gold": 25,
    },
    GoblinType.CHIEFTAIN: {
        "type": EnemyCategory.BOSS,
        "hp": 500,
        "speed": 1.0,
        "gold": 100,
    },

    UndeadEnemy.SKELETON_ARMY: {"type": EnemyCategory.UNDEAD, "hp": 50, "speed": 2.0, "gold": 10},
    UndeadEnemy.DARK_KNIGHT: {"type": EnemyCategory.UNDEAD, "hp": 200, "speed": 1.0, "gold": 35},
    MonsterEnemy.TROLL: {"type": EnemyCategory.MONSTER, "hp": 350, "speed": 0.7, "gold": 50},
    MonsterEnemy.DARK_SORCERY: {"type": EnemyCategory.MONSTER, "hp": 80, "speed": 1.5, "gold": 25},
}