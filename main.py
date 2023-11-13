import argparse
import logging
import pathlib

from field import Field

WELCOME_STRING = r"""
 ____   _                                           _         _    _               
/ ___| | |__    ___   ___  _ __   _ __ ___   _   _ | |  __ _ | |_ (_)  ___   _ __  
\___ \ | '_ \  / _ \ / _ \| '_ \ | '_ ` _ \ | | | || | / _` || __|| | / _ \ | '_ \ 
 ___) || | | ||  __/|  __/| |_) || | | | | || |_| || || (_| || |_ | || (_) || | | |
|____/ |_| |_| \___| \___|| .__/ |_| |_| |_| \__,_||_| \__,_| \__||_| \___/ |_| |_|
                          |_|                                                      
By Tomasz Kowalczyk & Jakub Kalinowski
"""


def load_config_file(filename: str) -> None:
    pass


def process_program_arguments() -> None:
    # Prepare parser
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

    # Get arguments
    arguments = argument_parser.parse_args()

    # Additional argument validation
    config_file_name = vars(arguments)["config_file"]

    log_level = vars(arguments)["log_level"]
    if log_level is not None:
        logging.basicConfig(filename="chase.log", filemode="w", level=log_level,
                            format='[%(asctime)s] [%(levelname)s] %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')
    else:
        logging.disable()

    rounds = vars(arguments)["rounds"]
    if rounds <= 0:
        raise ValueError

    sheep = vars(arguments)["sheep"]
    if sheep <= 0:
        raise ValueError

    wait = vars(arguments)["wait"]

    # Load config file
    if config_file_name is not None:
        if not pathlib.Path(config_file_name).is_file():
            raise ValueError
        load_config_file(config_file_name)
        # TODO: Load config file and apply data do model
        pass

    # Appy arguments to model
    Field.max_round = rounds
    Field.initial_sheep_count = sheep
    Field.wait_between_rounds = wait

    pass


def main():
    try:
        process_program_arguments()
    except ValueError:
        print("Invalid argument value!")
        exit(1)
    except TypeError:
        print("Invalid argument type!")
        exit(1)

    # TODO: add logging
    print(WELCOME_STRING)
    field = Field()
    # Start simulation
    field.run_simulation()


if __name__ == '__main__':
    main()
