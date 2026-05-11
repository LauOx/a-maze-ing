from typing import TypedDict, Dict

# sets of the autorized keys
MANDATORY_KEYS: set[str] = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

OPTIONAL_KEYS: set[str] = {
        "SEED"
    }

ALLOWED_KEYS: set[str] = MANDATORY_KEYS | OPTIONAL_KEYS


class MazeConfigError(Exception):
    """Exception raised for errors in the maze configuration."""
    pass


class ImposibleMazeError(MazeConfigError):
    """Exception raised when the maze configuration is impossible."""

    pass


class ConfigFormat(TypedDict):
    """Define dictionary that follows the format

    Raises:
        ValueError if the values are not int.
        MazeConfigError if the value format is not valid
    """
    width: int
    height: int
    entry_xy: tuple[int, int]
    exit_xy: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None
    theme_idx: int


def parse_coord(value: str) -> tuple[int, int]:
    """
    Parse a coordinate string into a tuple of integers.

    Args:
        value (str): The coordinate value from the config file in 'x,y' format.

    Returns:
        tuple[int, int]: A tuple containing the x and y integer coordinates.

    Raises:
        MazeConfigError: If the input string does not contain exactly two elements.
        MazeConfigError: If the coordinate values are not valid integers.
    """
    coor = [c.strip() for c in value.split(',')]

    if len(coor) != 2:
        raise MazeConfigError(
            f"Invalid format for '{value}'. Expected 'x,y' (two values)."
        )

    try:
        x = int(coor[0])
        y = int(coor[1])
    except ValueError as exc:
        raise MazeConfigError(
            f"Invalid coordinate value: '{value}' "
            "(Expected x,y with integers)"
        ) from exc
    return (x, y)


def parse_config(config_file_path: str) -> ConfigFormat:
    """
    Parse the maze configuration file.

    Args (config_file_path): The path to the config file .txt

    Returns (ConfigFormat): TypeDict with Key=name and Value=value
                            of the parameter

    Raises:
        MazeConfigError if key or value are invalid,
        or if the configuration file cannot be opened.
    """
    # Temporal dictionary to save the data and check
    temp: Dict[str, str] = {}
    try:
        with open(config_file_path, mode="r", encoding="utf-8") as file:
            content = file.readlines()

    except FileNotFoundError as e:
        raise MazeConfigError("Config file not found: "
                              f"{config_file_path}: {e}")

    except PermissionError as e:
        raise MazeConfigError("Permission error trying to open: "
                              f"{config_file_path}: {e}")

    except IsADirectoryError as e:
        raise MazeConfigError(f"{config_file_path} is a directory: {e}")

    except OSError as e:
        raise MazeConfigError("OS error opening config file "
                              f"'{config_file_path}': {e}")

    # Saves in a list of tuples, nb of line and content
    data_lines = [(i, line.strip()) for i, line
                  in enumerate(content, start=1)
                  if line.strip() and not line.strip().startswith('#')]

    # Format check
    for i, line in data_lines:
        if "=" not in line:
            raise MazeConfigError("Invalid format. Expected KEY=VALUE")

        key, value = line.split("=")
        key = key.upper()
        if not key:
            raise MazeConfigError(f"'KEY' is empty in line {i}")

        if key == "SEED" and not value:
            continue

        if key in temp:
            raise MazeConfigError(f"Duplicated key '{key}' in line {i}")

        temp[key] = value

    # Allowed and missing keys check
    all_keys = temp.keys()
    not_allowed = [k for k in all_keys - ALLOWED_KEYS]
    missing_key = [k for k in MANDATORY_KEYS - all_keys]

    if not_allowed:
        raise MazeConfigError("Unknown key(s) in "
                              f"config file: {not_allowed}")

    if missing_key:
        raise MazeConfigError(f"Missing required key(s): {missing_key}")

    # Parsing values
    # SEED
    raw_seed = temp.get("SEED")

    if raw_seed is None or raw_seed == "":
        seed = None
    else:
        try:
            seed = int(raw_seed)
        except ValueError:
            raise MazeConfigError(f"'SEED' value '{raw_seed}' "
                                  "is not a valid number")
    # WIDTH AND HEIGHT
    w = temp["WIDTH"]
    h = temp["HEIGHT"]
    try:
        width = int(w)
        height = int(h)
    except ValueError as exc:
        raise MazeConfigError(
            f"WIDTH and HEIGHT must be integers. Entered W: {w} and H: {h}"
        ) from exc
    if width <= 0 or height <= 0:
        raise MazeConfigError('WIDTH and HEIGHT must be positive '
                              'integers greater than 0. Entered '
                              f'W: {w} and H: {h}')
    # ENTRY AND EXIT
    entry_xy = parse_coord(temp["ENTRY"])
    exit_xy = parse_coord(temp["EXIT"])

    # PERFECT MAZE
    perfect_str = temp["PERFECT"].lower()
    if perfect_str not in ("true", "false"):
        raise MazeConfigError("PERFECT needs to be 'true' or 'false'.")
    perfect = (perfect_str == "true")

    # # UI SETTINGS (default values)
    theme_idx = int(temp.get("THEME_IDX", 4))

    # Return ConfigFormat
    return {
            "width": width,
            "height": height,
            "entry_xy": entry_xy,
            "exit_xy": exit_xy,
            "output_file": temp["OUTPUT_FILE"],
            "perfect": perfect,
            "seed": seed,
            "theme_idx": theme_idx,
            }
