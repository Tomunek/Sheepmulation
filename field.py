import csv
import json
import logging
import os
from typing import List

from sheep import Sheep
from wolf import Wolf


class Field:
    initial_sheep_count = 15
    sheep_count_len = 2
    max_round = 50
    round_len = 2
    wait_between_rounds = False
    json_filename = "pos.json"
    csv_filename = "alive.csv"

    def __init__(self):
        self.rounds_simulated = 0
        self.json_state: List[dict] = []
        self.csv_sheep_counts: list[int] = []
        self.sheep_killed_this_round: Sheep | None = None
        self.wolf = Wolf()
        self.sheep: List[Sheep] = []
        Field.sheep_count_len = len(str(Field.initial_sheep_count))
        Field.round_len = len(str(Field.max_round))
        for i in range(Field.initial_sheep_count):
            self.sheep.append(Sheep())
        logging.info(f"Created and initialised {len(self.sheep)} sheep")

    def get_alive_sheep(self) -> int:
        return len([True for sheep in self.sheep if sheep.alive])

    def simulate_round(self) -> None:
        # Simulate one round of simulation: all sheep, then wolf
        logging.info(f"Started round {self.rounds_simulated + 1}")
        for sheep in self.sheep:
            sheep.move()
        logging.info(f"All {self.get_alive_sheep()} alive sheep moved")
        self.sheep_killed_this_round = self.wolf.move(self.sheep)
        logging.info(f"Round {self.rounds_simulated + 1} ended with {self.get_alive_sheep()} sheep alive")
        self.rounds_simulated += 1

    def run_simulation(self) -> None:
        # Display initial state
        print(self)
        self.save_field_state_to_json_state()
        self.csv_sheep_counts.append(self.get_alive_sheep())
        # Simulate until wolf or all sheep die
        while self.rounds_simulated < Field.max_round and self.get_alive_sheep() > 0:
            self.simulate_round()
            print(self)
            self.save_field_state_to_json_state()
            self.csv_sheep_counts.append(self.get_alive_sheep())
            if Field.wait_between_rounds:
                input("Press ENTER to continue...")

        # Display cause of ending simulation
        if self.get_alive_sheep() > 0:
            print(f"[🐑😀] SIMULATION ENDED AFTER {self.rounds_simulated} ROUNDS. SHEEP ALIVE: {self.get_alive_sheep()}")
            logging.info(
                f"Simulation ended with {self.get_alive_sheep()} sheep alive after {self.rounds_simulated} rounds - "
                f"wolf ran out of time")
        else:
            print(f"[🐑☠️] SIMULATION ENDED AFTER {self.rounds_simulated} ROUNDS. ALL SHEEP WERE KILLED.")
            logging.info(f"Simulation ended with no sheep alive after {self.rounds_simulated} rounds")

        # Save results to json file
        if self.save_json_state_to_file(Field.json_filename):
            print(f"[✒️✔️] SAVED RESULTS TO {Field.json_filename}")
        else:
            print("[✒️❌] COULD NOT SAVE RESULTS TO JSON!")

        # Save results to csv file
        if self.save_csv_count_to_file(Field.csv_filename):
            print(f"[✒️✔️] SAVED RESULTS TO {Field.csv_filename}")
        else:
            print("[✒️❌] COULD NOT SAVE RESULTS TO CSV!")

    def __str__(self) -> str:
        chased_sheep = ""
        if self.wolf.currently_chased_sheep is not None:
            chased_sheep = f" [➡️🐑: {self.wolf.currently_chased_sheep.id:0{Sheep.sheep_id_len}d}]"
        killed_sheep = ""
        if self.sheep_killed_this_round is not None:
            killed_sheep = f" [🐑☠️: {self.sheep_killed_this_round.id:0{Sheep.sheep_id_len}d}]"
        return (f"[⏱: {self.rounds_simulated:0{Field.round_len}d}] [🐺 X: {self.wolf.x:+.5f}, Y: {self.wolf.y:+.5f}] "
                f"[🐑✔️: {self.get_alive_sheep():0{Field.sheep_count_len}d}]{chased_sheep}{killed_sheep}")

    def save_field_state_to_json_state(self) -> None:
        # Add current field state to json buffer
        sheep_position_list: list[tuple[float, float] | None] = [
            (sheep.x, sheep.y) if sheep.alive else None
            for sheep in self.sheep
        ]

        field_state: dict[str, (int | tuple[float, float] | None | list[tuple[float, float] | None])] = {
            "round_no": self.rounds_simulated,
            "wolf_pos": (self.wolf.x, self.wolf.y),
            "sheep_pos": sheep_position_list}

        self.json_state.append(field_state)

    def save_json_state_to_file(self, filename: str) -> bool:
        # Save json buffer to file, with nice formatting
        try:
            with open(filename, 'w') as f:
                f.write(json.dumps(self.json_state, indent=4))
        except OSError:
            return False
        logging.debug("Saved data to pos.json")
        return True

    def save_csv_count_to_file(self, filename: str) -> bool:
        # Save csv sheep counts
        try:
            with open(filename, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(["round_no", "alive_sheep"])
                for i, count in enumerate(self.csv_sheep_counts):
                    writer.writerow([i, count])
        except OSError:
            return False
        logging.debug("Saved data to alive.csv")
        return True
