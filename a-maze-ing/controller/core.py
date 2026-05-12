import sys
from config import (
    ConfigFormat,
    parse_config,
    maze_validator,
    check_42_pattern_fits,
    validate_entry_exit,
    MazeConfigError,
    ImposibleMazeError,
)
from ui import (
    animation,
    header_animation,
    static_header,
    menu_visuals,
    display_maze,
    DisplayMazeError
)
from mazegen import MazeGenerator as Maze, MazeGenerationError
try:
    import readchar
except ImportError:
    print("ImportError: Library 'readchar' is missing", file=sys.stderr)
    print("please run 'make install' (or: 'pip install .') "
          "to install the required dependencies", file=sys.stderr)
    sys.exit(1)


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
    """Generate the maze and applies the '42' pattern if applicable.
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
    """Handle the display of the maze and the user interaction loop
    for regenerating the maze, toggling the solution animation,
    changing color themes, and quitting the program.
     Args:
        maze (Maze):
            The maze object to be displayed.
        pattern (Set[tuple[int, int]] | None):
e 
            pattern cells, or None if the pattern is not applied.
        config (dict):
            The configuration dictionary containing settings for the maze
            generation and display.
    Raises:
        DisplayMazeError:
            If there is an error during the display
            of the maze or the solution animation.
    Note:
        For better understanding of ANSI code usage
        check the README.md file, resource section"""

    print("\033[H\033[J\033[3J", end="")
    running = True
    show_solution = False
    header_animation()

    while running:

        print("\033[H\033[2J\033[3J", end="", flush=True)

        static_header()

        if pattern is None:
            print("\n[WARNING] Maze dimensions are too small to accommodate "
                  "the '42' pattern. \nThe pattern will be ignored.\n", file=sys.stderr)

        try:
            display_maze(
                maze,
                pattern,
                config["theme_idx"],
            )

        except DisplayMazeError as e:
            print(f"\nDisplayMazeError: {e}")
            return

        try:
            maze.save_to_file(config["output_file"])
        except (OSError, MazeGenerationError) as e:
            error_type = type(e).__name__
            print(f"\n[WARNING] {error_type} saving maze to file: {e}", file=sys.stderr)

        if show_solution:

            try:
                solution = maze.solve()
            except MazeGenerationError as e:
                print(f"\n\nMazeGenerationError: {e}", file=sys.stderr)
                show_solution = False
            else:
                try:
                    animation(maze, solution, config["theme_idx"])

                except DisplayMazeError as e:
                    print(f"\n\nDisplayMazeError: {e}")
                    print("bye!")
                    return

        menu_visuals(config["theme_idx"])

        key = readchar.readkey()

        if key == "q" or key == "Q":
            running = False

        elif key == "r" or key == "R":
            show_solution = False
            try:
                maze, pattern = build_maze(config)
            except (MazeConfigError, ImposibleMazeError, MazeGenerationError) as e:
                print(f"\nError al regenerar: {e}", file=sys.stderr)
                print("Manteniendo el maze actual.", file=sys.stderr)

        elif key == "s" or key == "S":
            show_solution = not show_solution

        elif key == "c" or key == "C":
            config["theme_idx"] = (config["theme_idx"] + 1) % 5

        else:
            print("\a", end="")

    print("\033[H\033[J\033[3J", end="")
    print("bye!")
