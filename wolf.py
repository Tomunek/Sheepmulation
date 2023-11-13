import math
from typing import List

from sheep import Sheep


class Wolf:
    # Class variables
    movement_distance = 1.0

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.currently_chased_sheep: Sheep | None = None

    def __str__(self) -> str:
        # For nicer printing
        chased_sheep = ""
        if self.currently_chased_sheep is not None:
            chased_sheep = (f" [➡️🐑: {self.currently_chased_sheep.id:0{Sheep.sheep_id_len}d},"
                            f" 📐: {self.get_distance_to_sheep(self.currently_chased_sheep):.8f}]")

        return f"🐺✔️ [X: {self.x:+.5f}, Y: {self.y:+.5f}]{chased_sheep}"

    def move(self, sheep_list: List[Sheep]) -> None | Sheep:
        # Only move if there are sheep to chase, else rest
        if any([sheep.alive for sheep in sheep_list]):
            self.currently_chased_sheep = self.find_closest_sheep(sheep_list)
            if self.get_distance_to_sheep(self.currently_chased_sheep) <= Wolf.movement_distance:
                # Kill sheep
                self.x = self.currently_chased_sheep.x
                self.y = self.currently_chased_sheep.y
                self.currently_chased_sheep.alive = False
                return self.currently_chased_sheep
            else:
                # TODO: chase sheep (move towards it)
                return None
        return None

    def get_distance_to_sheep(self, sheep: Sheep) -> float:
        return math.sqrt(pow(self.x - sheep.x, 2) + pow(self.y - sheep.y, 2))

    def find_closest_sheep(self, sheep_list: List[Sheep]) -> Sheep:
        # This method must not be called when there are no alive sheep
        closest_sheep = sheep_list[0]
        closest_sheep_distance = float("inf")
        for sheep in sheep_list:
            if sheep.alive:
                distance = self.get_distance_to_sheep(sheep)
                if distance < closest_sheep_distance:
                    closest_sheep_distance = distance
                    closest_sheep = sheep
        return closest_sheep
