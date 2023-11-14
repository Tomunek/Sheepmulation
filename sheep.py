import logging
import random
from random import uniform


class Sheep:
    # Class variables - shared between all sheep
    max_init_coord = 10.0
    movement_distance = 0.5
    current_sheep_id = 0
    sheep_id_len = 1

    def __init__(self):
        self.id = Sheep.current_sheep_id
        self.alive = True
        Sheep.sheep_id_len = len(str(Sheep.current_sheep_id))
        Sheep.current_sheep_id += 1
        self.x = uniform(-Sheep.max_init_coord, Sheep.max_init_coord)
        self.y = uniform(-Sheep.max_init_coord, Sheep.max_init_coord)
        logging.debug(f"Initialised sheep {self.id} at position ({self.x};{self.y})")

    def __str__(self) -> str:
        # For nicer printing
        ok = "☠️"
        if self.alive:
            ok = "✔️"
        return f"🐑{ok} [ID: {self.id:0{Sheep.sheep_id_len}d}] [X: {self.x:+.5f}, Y: {self.y:+.5f}]"

    def move(self) -> None:
        if self.alive:
            # Choose a random direction and move (much intelligence)
            direction = random.choice(['u', 'd', 'l', 'r'])
            logging.debug(f"Sheep {self.id} chose direction {direction}")
            match direction:
                case 'u':
                    self.y += Sheep.movement_distance
                case 'd':
                    self.y -= Sheep.movement_distance
                case 'l':
                    self.x -= Sheep.movement_distance
                case 'r':
                    self.x += Sheep.movement_distance
            logging.debug(f"Sheep {self.id} moved to ({self.x};{self.y})")
