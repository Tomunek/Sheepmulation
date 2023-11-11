import random
from random import uniform


class Sheep:
    # Class variables - shared between all sheep
    max_init_coord = 10.0
    movement_distance = 0.5
    current_sheep_id = 0

    def __init__(self):
        self.id = Sheep.current_sheep_id
        self.alive = True
        Sheep.current_sheep_id += 1
        self.x = uniform(-Sheep.max_init_coord, Sheep.max_init_coord)
        self.y = uniform(-Sheep.max_init_coord, Sheep.max_init_coord)

    def __str__(self) -> str:
        # For nicer printing
        ok = "☠️"
        if self.alive:
            ok = "✔️"

        return f"🐑{ok} [ID: {self.id:03d}] [X: {self.x:+.5f}, Y: {self.y:+.5f}]"

    def move(self) -> None:
        if self.alive:
            # Choose a random direction and move (much intelligence)
            direction = random.choice(['u', 'd', 'l', 'r'])
            match direction:
                case 'u':
                    self.y += Sheep.movement_distance
                case 'd':
                    self.y -= Sheep.movement_distance
                case 'l':
                    self.x -= Sheep.movement_distance
                case 'r':
                    self.x += Sheep.movement_distance
