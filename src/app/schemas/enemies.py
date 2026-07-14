from dataclasses import dataclass

@dataclass
class EnemySchema:
    id: str
    name: str
    health: float
    speed: float
    reward: int
    sprite_sheet: str