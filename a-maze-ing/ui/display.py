import os
from typing import Generator
import time
from mazegen import MazeGenerator as Maze
import shutil

COLOR_PALETTE = [
    # 0: bg,
    # 1: path,
    # 2: font,
    # 3: p42,
    # 4: ec
    # night
    ["\033[48;5;17m",
     "\033[48;5;229m",
     "\033[38;5;129m",
     "\033[48;5;51m",
     "\033[0m"],
    # uzumaki
    ["\033[48;5;166m",
     "\033[48;5;019m",
     "\033[38;5;241m",
     "\033[48;5;220m",
     "\033[0m"],
    # akatsuki
    ["\033[48;5;233m",
     "\033[48;5;238m",
     "\033[38;5;251m",
     "\033[48;5;124m",
     "\033[0m"],
    # dark mode
    ["\033[48;5;233m",
     "\033[48;5;236m",
     "\033[38;5;241m",
     "\033[48;5;220m",
     "\033[0m"],
    # eva01
    ["\033[48;5;128m",
     "\033[48;5;54m",
     "\033[38;5;54m",
     "\033[48;5;76m",
     "\033[0m"],
    # ox
    ["\033[48;5;55m",
     "\033[48;5;177m",
     "\033[38;5;177m",
     "\033[48;5;99m",
     "\033[0m"]
]


class DisplayMazeError(Exception):
    """Exception raised for errors in the maze display process."""
    pass


def print_maze(
        maze: Maze,
        pattern_42: set[tuple[int, int]] | None,
        theme_idx: int = 4,
        ) -> None:
    """
    Print the maze to the terminal with optional
    styling and solution path.
     Args:
            maze (Maze): The maze object to be printed.
            Pattern_42 (set[tuple[int, int]]):
                Set of coordinatesfor the '42' pattern cells.
            solution_path (list[tuple[int, int]], optional):
                List of coordinates for the solution path. Defaults to None.
            theme_idx (int, optional):
                Index for the color theme. Defaults to 4.
     Raises:
            DisplayMazeError:
                If the maze cannot be displayed properly
                due to terminal size constraints.
    """

    bg = COLOR_PALETTE[theme_idx][0]
    ft = COLOR_PALETTE[theme_idx][3]
    font = COLOR_PALETTE[theme_idx][2]
    path = COLOR_PALETTE[theme_idx][1]
    ec = COLOR_PALETTE[theme_idx][4]

    r_style = bg + font

    top_line = r_style

    for x in range(maze.width):
        top_line += "+---"
    top_line += "+" + ec
    print(top_line)

    # For each row of the maze
    for y in range(maze.height):

        # Vertical cells
        line_cells = r_style + "|"

        # Bottom line of cells
        line_bottom = r_style

        for x in range(maze.width):
            cell = maze.grid[x][y]

            # Check if the cell is entry, exit, in 42 pattern or normal cell
            if (x, y) == maze.entry_xy or (x, y) == maze.exit_xy:
                content = path + " * " + ec + r_style
            elif (pattern_42 and (x, y) in pattern_42):
                content = ft + " * " + ec + r_style
            else:
                content = "   "

            # East wall
            east_wall = "|" if cell.walls["E"] else " "

            # Build line of cells
            line_cells += content + east_wall

            # South wall
            if cell.walls["S"]:
                line_bottom += "+---"
            else:
                line_bottom += "+   "

        # Close the line of cells
        line_cells += ec
        line_bottom += "+" + ec

        # Print the two lines
        print(line_cells)
        print(line_bottom)


def header_yield(file_path: str) -> Generator[str, None, None]:
    """
    Read a file and yields its content character by character with a delay.

    Args:
        file_path (str): The path to the file to be read.
    Yields:
        Generator[str, None, None]:
            A generator that yields characters from the file.
    """
    try:
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                for c in line:
                    yield c

    except FileNotFoundError as e:
        print(f"Caught an error: {e}")


def header_animation() -> None:
    """
    Display the header animation by reading the header.txt file
    and printing its content with a delay.
    """
    try:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "header.txt")

        for c in header_yield(file_path):
            print(c, end="", flush=True)
            time.sleep(0.0005)
            print("\033[s", end="")

    except FileNotFoundError as e:
        print(f"Caught an error: {e}")


def static_header() -> None:
    """
    Display the static header without animation.
    """
    try:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "header.txt")

        with open(file_path, encoding='utf-8') as f:
            print(f.read(), end="", flush=True)

    except FileNotFoundError as e:
        print(f"Caught an error: {e}")


def animation(maze: Maze,
              solution_path: list[tuple[tuple[int, int], str]],
              theme_idx: int = 4) -> None:
    """
    Print step by step the solution path with a delay between each step.
    Args:
        maze (Maze): The maze object being displayed.
        solution_path (list[tuple[int, int]]):
            List of coordinates for the solution path.
        theme_idx (int, optional):
            Index for the color theme. Defaults to 4.
    Raises:
        DisplayMazeError:
            If the terminal is resized during the animation,
            which could cause display issues
    Note:
        For better understanding of ANSI code usage
        check the README.md file, resource section
    """
    sol_color = COLOR_PALETTE[theme_idx][1]
    ec = COLOR_PALETTE[theme_idx][4]

    # Check initial terminal size
    initial_size = shutil.get_terminal_size()

    solution_coords = [coords for coords, _ in solution_path]
    print("\033[s", end="")
    for x, y in solution_coords:
        # Check current terminal size
        current_size = shutil.get_terminal_size()
        if current_size != initial_size:
            print("\033[u", end="", flush=True)
            raise DisplayMazeError(
                "Terminal resized during animation. Returning to safe state.")
        print("\033[u", end="")

        # Calculate the vertical Y-axis and the horizontal X-axis
        lines_up = 2 * (maze.height - y)
        cols_right = x * 4 + 2

        move_up = f"\033[{lines_up}A"
        move_right = f"\033[{cols_right}C" if cols_right > 0 else ""

        # Move and print without line breaks and force a flush (required)
        print(f"{move_up}{move_right}{sol_color}•{ec}", end="", flush=True)
        time.sleep(0.05)

    print("\033[u", end="", flush=True)


def check_display_size(
        maze_width: int,
        maze_height: int
        ) -> None:
    """
    Evaluate the terminal size against the maze dimensions to determine
    if the maze can be displayed properly.
     Args:
        maze_width (int): The width of the maze.
        maze_height (int): The height of the maze.
    """

    header_lines = 18
    safety_margin = 3
    menu_lines = 5
    render_width = (maze_width * 4) + 1
    render_height = (maze_height * 2) + 1
    height_needed = (render_height + header_lines + menu_lines + safety_margin)

    term_width, term_height = shutil.get_terminal_size(fallback=(80, 24))
    if term_height < height_needed or term_width < render_width:
        print(f"\033[{header_lines + safety_margin};0H", end="")
        raise DisplayMazeError(
            "Terminal size is too small to display the maze properly."
            "\nPlease resize your terminal and try again.")


def menu_visuals(theme_idx: int) -> None:
    """Display the menu options with the current theme colors.
     Args:
        theme_idx (int): The index of the current color theme."""

    bg = COLOR_PALETTE[theme_idx][0]
    ft = COLOR_PALETTE[theme_idx][3]
    font = COLOR_PALETTE[theme_idx][2]
    ec = COLOR_PALETTE[theme_idx][4]

    style = f"{bg}{font}"

    print()
    print(f"{ft} {font} Lau&Lau Maze menu: {ec}")
    print(f"Press {style}'R'{ec} to regenerate maze")
    print(f"Press {style}'S'{ec} to toggle solution animation")
    print(f"Press {style}'C'{ec} to change color theme")
    print(f"Press {style}'Q'{ec} to quit")


def display_maze(
        maze: Maze,
        pattern_42: set[tuple[int, int]] | None,
        theme_idx: int = 4,
        ) -> None:
    """
    Handle the display of the maze in the terminal, including checking
    if the maze fits within the terminal size
    and printing the maze with the appropriate styling.
     Args:
        maze (Maze): The maze object to be displayed.
        pattern_42 (set[tuple[int, int]]):
            Set of coordinates for the '42' pattern cells.
        solution_path (list[tuple[int, int]], optional):
            List of coordinates for the solution path. Defaults to None.
        theme_idx (int, optional):
            Index for the color theme. Defaults to 4.
     Raises:
        DisplayMazeError:
            If the maze cannot be displayed properly
            due to terminal size constraints.
    """
    check_display_size(maze.width, maze.height)
    print_maze(
        maze,
        pattern_42,
        theme_idx,
        )
