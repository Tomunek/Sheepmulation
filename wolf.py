import logging
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
                            f" 📐: {self.get_distance_to_sheep(self.currently_chased_sheep):.5f}]")
        return f"🐺✔️ [X: {self.x:+.3f}, Y: {self.y:+.3f}]{chased_sheep}"

    def move(self, sheep_list: List[Sheep]) -> None | Sheep:
        # Only move if there are sheep to chase, else rest
        if any([sheep.alive for sheep in sheep_list]):
            self.currently_chased_sheep = self.find_closest_sheep(sheep_list)
            distance_to_closest_sheep = self.get_distance_to_sheep(self.currently_chased_sheep)
            logging.debug(
                f"Wolf found closest sheep ({self.currently_chased_sheep.id}) "
                f"with distance {distance_to_closest_sheep}")
            if distance_to_closest_sheep <= Wolf.movement_distance:
                # Kill sheep
                self.x = self.currently_chased_sheep.x
                self.y = self.currently_chased_sheep.y
                self.currently_chased_sheep.alive = False
                logging.debug(f"Wolf moved to ({self.y};{self.y}), killing sheep {self.currently_chased_sheep.id}")
                logging.info("Wolf moved")
                logging.info(f"Wolf killed sheep {self.currently_chased_sheep.id}")
                return self.currently_chased_sheep
            else:
                # Chase nearest sheep (move towards it)
                logging.info(f"Wolf is chasing sheep {self.currently_chased_sheep.id}")
                dx = self.currently_chased_sheep.x - self.x
                dy = self.currently_chased_sheep.y - self.y
                distance_in_moves = distance_to_closest_sheep / Wolf.movement_distance
                self.x += dx / distance_in_moves
                self.y += dy / distance_in_moves
                logging.debug(f"Wolf moved to ({self.y};{self.y})")
                logging.info("Wolf moved")
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
