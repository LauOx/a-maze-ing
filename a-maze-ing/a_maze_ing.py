#!/usr/bin/env python3
import sys
from config import parse_config, MazeConfigError
from ui import display
from mazegen import Maze
import shutil


def determine_display_mode(
        maze_width: int,
        maze_height: int
    ) -> tuple[bool, bool]:
    """Evaluate terminal values to define forty-two patern and animation-mode display"""
    header_lines: int = 17
    safety_margin: int = 3 
    apply_ft_pattern: bool = maze_width >= 15 and maze_height >= 15

    term_width, term_height = shutil.get_terminal_size(fallback=(80, 24))
    animated_solution: bool = (maze_width + 1 <= term_width and maze_height + safety_margin <= term_height)

    return apply_ft_pattern, animated_solution

def a_maze_ing() -> None:
    """
    
    """
    if len(sys.argv) == 2:
        try:
            file = sys.argv[1]
            maze = Maze(parse_config(file))
            maze._generate_maze()
            solved_path = maze.solve()
            sol_coords: list[tuple[int, int]] = [coord for coord, _ in solved_path]
            directions: list[str] = [direction for _, direction in solved_path]
            apply_pattern, animated_solution = determine_display_mode(maze.width, maze.height)
            ft_pattern: set[tuple[int, int]] = (
                maze._block_42_pattern() if apply_pattern else set()
            )
            display(maze, ft_pattern, sol_coords, animated_solution)
            maze.save_to_file(directions)
        except MazeConfigError as e:
            print(f"Caught an error: {e}")
    else:
        print("No arguments recieved")

a_maze_ing()

#  CAMBIOS PROPUESTOS:

# Cambio nombre de la variable a_maze_ing por "maze" para no pisarse con llamados a la funcion a_maze_ing().

# Añado una funcion que determina el uso adecuado del display segun las dimensiones del maze.

# Ha de refactorizar el bloque try. Errores de parseo MazeConfigError