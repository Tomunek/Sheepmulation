# Sheepmulation

A simple ecosystem simulation consisting of a wolf hunting a pack of sheep

## Usage:

### Run simulation with default settings:

```bash
python3 main.py
```

### Available options:

- `-c <FILE>`/`--config <FILE>` - select config file to modify behaviour of animals
- `-h`/`--help` - display info about all available command line arguments
- `-l <LEVEL>`/`--log <LEVEL>` - select log level (`DEBUG`/`INFO`/`WARNING`/`ERROR`/`CRITICAL`)
- `-r <ROUNDS>`/`--rounds <ROUNDS>` - select number of rounds to be simulated
- `-s <SHEEP>`/`--sheep <SHEEP>` - select initial number of sheep
- `-w`/`--wait` - wait for user after simulating each

### Examples:

Run simulation with

- behavior from config.ini file,
- for 100 rounds,
- with 20 sheep,
- log WARNINGS and ERRORS (CRITICAL too)
- and wait for user after every round

```bash
python3 main.py -c config.ini -l WARNING -r 100 -s 20 -w
```

Show help message:

```bash
python3 main.py --help
```