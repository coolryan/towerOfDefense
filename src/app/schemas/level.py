from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class WaveSchema:
    enemy_type: str
    count: int
    spawn_delay: float

@dataclass
class LevelSchema:
    name: str
    tile_size: int
    grid_width: int
    grid_height: int
    waypoints: List[Tuple[float, float]]
    waves: List[WaveSchema]