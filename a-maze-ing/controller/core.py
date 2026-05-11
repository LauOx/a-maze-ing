import sys
from config import (
    ConfigFormat,
    parse_config,
    maze_validator,
    check_42_pattern_fits,
    validate_entry_exit
)
from ui import (
    animation,
    header_animation,
    static_header,
    menu_visuals,
    display_maze
)
from mazegen import MazeGenerator as Maze


class DependencyError(RuntimeError):
    """Exception raised when a required runtime dependency is missing.

    Raised when readchar or other required runtime dependencies cannot be
    imported.
    """
    pass


def _load_readchar():
    try:
        import readchar
    except ImportError as exc:
        raise DependencyError(
            "Library 'readchar' is missing. "
            "Run 'make install' (or: 'pip install .') "
            "to install the required dependencies."
        ) from exc
    return readchar


def setup_config(file_path: str) -> ConfigFormat:
    """
    Initialize the configuration by parsing and validating the config file.
    """

    config = parse_config(file_path)
    maze_validator(config)

    return config


def build_maze(
        config: ConfigFormat
        ) -> tuple[Maze, set[tuple[int, int]] | None]:
    """Generates the maze and applies the '42' pattern if applicable.
    returns the maze object and the pattern cells if the pattern is applied.
    Args:
        config (dict):
            The configuration dictionary containing
            settings for the maze generation.
    Returns:
        tuple[Maze, Set[tuple[int, int]] | None]:
            A tuple containing the generated maze object and a set of
            coordinates for the '42' pattern cells, or None if the pattern
            is not applied."""

    maze = Maze(
        width=config["width"],
        height=config["height"],
        entry_xy=config["entry_xy"],
        exit_xy=config["exit_xy"],
        perfect=config["perfect"],
        seed=config["seed"]
    )
    maze.generate()
    pattern = None
    if check_42_pattern_fits(config):
        pattern = maze.block_42_pattern(maze.width, maze.height)
    if pattern:
        validate_entry_exit(
            maze.width,
            maze.height,
            maze.entry_xy,
            maze.exit_xy
            )

    return maze, pattern


def run_visuals(
        maze: Maze,
        pattern: set[tuple[int, int]] | None,
        config: ConfigFormat
        ) -> None:
    """Handles the display of the maze and the user interaction loop
    for regenerating the maze, toggling the solution animation,
    changing color themes, and quitting the program.
     Args:
        maze (Maze):
            The maze object to be displayed.
        pattern (Set[tuple[int, int]] | None):
            Set of coordinates for the '42'
            pattern cells, or None if the pattern is not applied.
        config (dict):
            The configuration dictionary containing settings for the maze
            generation and display.
    raises:
        DependencyError:
            If the input dependency is missing.
        DisplayMazeError:
            Propagated if there is an error during the display
            of the maze or the solution animation.
        MazeGenerationError:
            If solving or saving the maze fails.
    """

    readchar = _load_readchar()
    print("\033[H\033[J\033[3J", end="")
    running = True
    show_solution = False
    header_animation()

    while running:

        print("\033[H\033[2J\033[3J", end="", flush=True)

        static_header()

        display_maze(
            maze,
            pattern,
            # maze.solve(),
            config["theme_idx"],
            # config["random_color"]
        )

        if show_solution:

            animation(maze, maze.solve(), config["theme_idx"])

        menu_visuals(config["theme_idx"])

        try:

            key = readchar.readkey()

            if key == "q" or key == "Q":
                running = False

            elif key == "r" or key == "R":
                show_solution = False
                maze, pattern = build_maze(config)

            elif key == "s" or key == "S":
                show_solution = not show_solution

            elif key == "c" or key == "C":
                config["theme_idx"] = (config["theme_idx"] + 1) % 5

            else:
                print("\a", end="")

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Bye!...", file=sys.stderr)
            return

        maze.save_to_file(config["output_file"])

    print("\033[H\033[J\033[3J", end="")
    print("bye!")
