# TODO: field
# TODO: store wolf and sheep
# TODO: move sheep, then wolf
# TODO: check if any deaths occurred, if yes, log
# TODO: display: round_no, wolf_pos, sheep_no, wolf_chase_id, deaths
from typing import List

from sheep import Sheep
from wolf import Wolf


class Field:
    initial_sheep_count = 15
    sheep_count_len = 2
    max_round = 50
    round_len = 2

    def __init__(self):
        self.round_no = 0
        self.sheep_killed_this_round: Sheep | None = None
        self.wolf = Wolf()
        self.sheep: List[Sheep] = []
        Field.sheep_count_len = len(str(Field.initial_sheep_count))
        Field.round_len = len(str(Field.max_round))
        for i in range(Field.initial_sheep_count):
            self.sheep.append(Sheep())

    def get_alive_sheep(self):
        return len([True for sheep in self.sheep if sheep.alive])

    def simulate_round(self) -> int:
        for sheep in self.sheep:
            sheep.move()
        self.wolf.move(self.sheep)
        self.round_no += 1
        return self.get_alive_sheep()

    def __str__(self) -> str:
        chased_sheep = ""
        if self.wolf.currently_chased_sheep is not None:
            chased_sheep = f" [➡️🐑: {self.wolf.currently_chased_sheep.id:0{Sheep.sheep_id_len}d}]"
        killed_sheep = ""
        if self.sheep_killed_this_round is not None:
            killed_sheep = f" [🐑☠️: {self.sheep_killed_this_round.id:0{Sheep.sheep_id_len}d}]"
        return (f"[⏱: {self.round_no:0{Field.round_len}d}] [🐺 X: {self.wolf.x:+.5f}, Y: {self.wolf.y:+.5f}] "
                f"[🐑✔️: {self.get_alive_sheep():0{Field.sheep_count_len}d}]{chased_sheep}{killed_sheep}")
