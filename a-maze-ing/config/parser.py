#!/usr/bin/python3
from typing import TypedDict


# sets of the autorized keys
MANDATORY_KEYS: set[str] = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    }

OPTIONAL_KEYS: set[str] = {
        "RANDOM_COLOR",
        "INSTANT_SOLUTION",
        "SEED",
        "THEME_IDX"
    }

ALLOWED_KEYS: set[str] = MANDATORY_KEYS | OPTIONAL_KEYS

class MazeConfigError(Exception):
    """"""
    pass

class KeyError(MazeConfigError):
    """"""
    pass

class ConfigFormat(TypedDict):
    """Define dictionary that follows the format"""
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None
    theme_idx: int
    instant_solution: bool
    random_color: bool

def parse_coord(value: str) -> tuple[int, int]:
    """Convert exit/entry coordinates into tuples"""
    coor = value.split(',')
    if len(coor) != 2:
        raise ValueError("Invalid format for entry/exit. "
                         "(Expected x,y)")
    return (int(coor[0]), int(coor[1]))
            

def parse_config(config_file_path: str) -> ConfigFormat:
    """
    Parse the maze configuration file.

    Raise:
        MazeConfigError if key or value are invalid
        ValueError if value is not integrer
        FileNotFoundError if config file doesn't exist
    """
    # temporal dictionary to save the data and check
    temp: dict[str, str] = {}
    
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
        raise MazeConfigError(f"OS error opening config file '{config_file_path}': {e}")
    
    # saves in a list of tuples, nb of line and content
    # line.strip() return "" if is an empty line
    data_lines = [(i, line.strip()) for i, line
                    in enumerate(content, start=1)
                    if line.strip() and not line.strip().startswith('#')]
    
    # format check
    for i, line in data_lines:
        if "=" not in line:
            raise MazeConfigError("Invalid format. Expected KEY=VALUE")
        
        key, value = line.split("=")
        key = key.upper()
        if not key:
            raise KeyError(f"'KEY' is empty in line {i}")
        
        if key == "SEED" and not value:
            continue
        
        if key in temp:
            raise KeyError(f"Duplicated key '{key}' in line {i}")

        # Saving {Key: value} in a temprorary variable
        temp[key] = value

    # allowed and missing keys check
    all_keys = temp.keys()
    not_allowed = list(all_keys - ALLOWED_KEYS)
    missing_key = list(MANDATORY_KEYS - all_keys)
    
    if not_allowed:
        raise KeyError("Unknown key(s) in "
                        f"config file: {not_allowed}")
    
    if missing_key:
        raise KeyError(f"Missing required key(s): {missing_key}")
    
    # parsing values
    try:
        # SEED
        seed = None
        if "SEED" in temp and temp["SEED"]:
            try:
                seed = int(temp["SEED"])
            except ValueError:
                raise ValueError(f"'SEED' value '{temp['SEED']}' is not a valid number")
            
        # WIDTH AND HEIGHT
        try:
            width = int(temp["WIDTH"])
            height = int(temp["HEIGHT"])
            if width <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            raise ValueError(f"WIDTH and HEIGHT must be positive integers greater than 0. Entered W: '{temp['WIDTH']}', H: '{temp['HEIGHT']}'")
        

        # ENTRY AND EXIT
        entry_xy = parse_coord(temp["ENTRY"])
        exit_xy = parse_coord(temp["EXIT"])

        # PERFECT MAZE
        perfect_str = temp["PERFECT"].lower()
        if perfect_str not in ("true", "false"):
            raise ValueError(f"PERFECT needs to be 'true' or 'false', got '{temp['PERFECT']}'")
        perfect = (perfect_str == "true")
        
        # UI SETTINGS
        theme_idx = int(temp.get("THEME_IDX", 4))
        instant_solution = temp.get("INSTANT_SOLUTION", "false").lower() == "true"
        random_color = temp.get("RANDOM_COLOR", "false").lower() == "true"

    except ValueError as e:
        # Atrapamos cualquier error de valor (producido por int(), parse_coord(), o nuestros propios raises)
        # y le anexamos el mensaje predefinido original mediante la variable 'e'.
        raise MazeConfigError(f"Configuration value error: {e}")

    # Return ConfigFormat (El contrato perfecto.)
    return {
        "width": width,
        "height": height,
        "entry": entry_xy,
        "exit": exit_xy,
        "output_file": temp["OUTPUT_FILE"],
        "perfect": perfect,
        "seed": seed,
        "theme_idx": theme_idx,
        "instant_solution": instant_solution,
        "random_color": random_color
    }

if __name__ == "__main__":
    import sys
    try:
        diccionario = parse_config("config.txt")
        print("Lectura manual exitosa, aqui está el diccionario: ", diccionario)
    except Exception as e:
        print(f"Test fallido con error:\n{type(e).__name__}: {e}", file=sys.stderr)



# CAMBIOS REALIZADOS EN parser:

# Simplificacion de imports a from typing import TypedDict

# Ampliazcion de Optional_keys y ConfigFormat(TypedDict) class

# Creation of KeyError(MazeConfigError) class
    
# Refactorizacion de parse_config(): 
#     Descomposicion del bloque try monolitico (enorme)
#     Division de responsabilidades en las capturas de exceptions
#     Tratamiento de excepciones elevando error especifico. (ademas del print)

# Comentarios de los cambios empleados.

# Implementaciond el bloque if __name__ == " __main__": para evitar
# la ejecucion involutaria de printeros de debugeo.