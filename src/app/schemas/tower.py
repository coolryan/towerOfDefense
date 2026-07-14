from dataclasses import dataclass
from typing import List

@dataclass
class TowerUpgradeSchema:
    level: int
    cost: int
    damage: float
    range: float
    cooldown: float

@dataclass
class TowerSchema:
    id: str
    name: str
    base_cost: int
    projectile_type: str
    upgrades: List[TowerUpgradeSchema]