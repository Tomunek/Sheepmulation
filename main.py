#!/usr/bin/python3
import argparse
import configparser
import logging
import pathlib
import sys

from field import Field
from sheep import Sheep
from wolf import Wolf

WELCOME_STRING = r"""
 ____   _                                           _         _    _               
/ ___| | |__    ___   ___  _ __   _ __ ___   _   _ | |  __ _ | |_ (_)  ___   _ __  
\___ \ | '_ \  / _ \ / _ \| '_ \ | '_ ` _ \ | | | || | / _` || __|| | / _ \ | '_ \ 
 ___) || | | ||  __/|  __/| |_) || | | | | || |_| || || (_| || |_ | || (_) || | | |
|____/ |_| |_| \___| \___|| .__/ |_| |_| |_| \__,_||_| \__,_| \__||_| \___/ |_| |_|
                          |_|                                                      
By Tomasz Kowalczyk & Jakub Kalinowski
"""


def prepare_argument_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(
        prog="Sheepmulation",
        description="Simulate wolf hunting a herd of sheep",
        epilog="By Tomasz Kowalczyk & Jakub Kalinowski",
        add_help=True)
    argument_parser.add_argument("-c", "--config",
                                 help="path to config file",
                                 action="store",
                                 dest="config_file",
                                 default=None,
                                 type=str)
    argument_parser.add_argument("-l", "--log",
                                 help="logging level",
                                 action="store",
                                 dest="log_level",
                                 default=None,
                                 type=str)
    argument_parser.add_argument("-r", "--rounds",
                                 help="number of rounds to simulate",
                                 action="store",
                                 dest="rounds",
                                 default=50,
                                 type=int)
    argument_parser.add_argument("-s", "--sheep",
                                 help="number of sheep at the start",
                                 action="store",
                                 dest="sheep",
                                 default=15,
                                 type=int)
    argument_parser.add_argument("-w", "--wait",
                                 help="wait for input after each round",
                                 action="store_true",
                                 dest="wait",
                                 default=False)
    return argument_parser


def load_sheep_config_file_and_apply(config_from_file: configparser.ConfigParser) -> None:
    if "InitPosLimit" in config_from_file["Sheep"]:
        try:
            max_init_coord_from_file = float(config_from_file["Sheep"]["InitPosLimit"])
        except ValueError as e:
            raise ValueError(f"config file: invalid InitPosLimit value in config file") from e
        if max_init_coord_from_file <= 0.0:
            raise ValueError(
                f"config file: invalid max initial coord of sheep ({max_init_coord_from_file}) in config file")
        Sheep.max_init_coord = max_init_coord_from_file
        logging.debug(f"Loaded max init sheep coord = {max_init_coord_from_file} from config file")
    if "MoveDist" in config_from_file["Sheep"]:
        try:
            movement_dist_from_file = float(config_from_file["Sheep"]["MoveDist"])
        except ValueError as e:
            raise ValueError(f"config file: invalid Sheep MoveDist value in config file") from e
        if movement_dist_from_file <= 0.0:
            raise ValueError(
                f"config file: invalid movement distance of sheep ({movement_dist_from_file}) in config file")
        Sheep.movement_distance = movement_dist_from_file
        logging.debug(f"Loaded sheep movement distance = {movement_dist_from_file} from config file")


def load_wolf_config_file_and_apply(config_from_file: configparser.ConfigParser) -> None:
    if "MoveDist" in config_from_file["Wolf"]:
        try:
            movement_dist_from_file = float(config_from_file["Wolf"]["MoveDist"])
        except ValueError as e:
            raise ValueError(f"config file: invalid Wolf MoveDist value in config file") from e
        if movement_dist_from_file <= 0.0:
            raise ValueError(
                f"config file: invalid movement distance of wolf ({movement_dist_from_file}) in config file")
        Wolf.movement_distance = movement_dist_from_file
        logging.debug(f"Loaded wolf movement distance = {movement_dist_from_file} from config file")


def load_config_file_and_apply(filename: str) -> None:
    try:
        config_from_file = configparser.ConfigParser()
        try:
            config_from_file.read(filename)
        except OSError as e:
            raise ValueError(f"argument -c/--config: could not read from config file (OSError)") from e
        if "Sheep" in config_from_file:
            load_sheep_config_file_and_apply(config_from_file)
        if "Wolf" in config_from_file:
            load_wolf_config_file_and_apply(config_from_file)
    except configparser.Error as e:
        raise ValueError(f"argument -c/--config: invalid config file format") from e


def validate_program_arguments(arguments: argparse.Namespace) -> argparse.Namespace:
    # Additional argument validation
    log_level = arguments.log_level
    if log_level is not None and log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"argument -l/--log: invalid value: {log_level}!")

    rounds = arguments.rounds
    if rounds <= 0:
        raise ValueError(f"argument -r/--rounds: invalid value: {rounds}!")

    sheep = arguments.sheep
    if sheep <= 0:
        raise ValueError(f"argument -s/--sheep: invalid value: {sheep}!")

    # Load config file
    config_file_name = arguments.config_file
    if config_file_name is not None and not pathlib.Path(config_file_name).is_file():
        raise ValueError(f"argument -c/--config: selected config file ({config_file_name}) does not exist")

    return arguments


def main():
    argument_parser = prepare_argument_parser()

    # Custom exception handler to display program usage with exception and hide call stack
    def exception_handler(exception_type, exception, traceback):
        argument_parser.print_usage()
        print(f"{exception_type.__name__}: {exception}")

    sys.excepthook = exception_handler

    # Get and validate program arguments
    args = validate_program_arguments(argument_parser.parse_args())

    # Set logging level
    if args.log_level is not None:
        logging.basicConfig(filename="chase.log", filemode="w", level=args.log_level,
                            format='[%(asctime)s] [%(levelname)s] %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')
    else:
        logging.disable()

    # Load and apply config from file
    if args.config_file is not None:
        load_config_file_and_apply(args.config_file)

    print("\033[0;32m" + WELCOME_STRING + "\033[0m")
    field = Field(args.sheep, args.rounds, args.wait)
    # Start simulation
    field.run_simulation()


if __name__ == '__main__':
    main()
