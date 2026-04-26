import os
import random
from typing import Generator
import time
from mazegen import Maze, Cell

COLOR_PALETTE = [
    # 0: bg,           1: path,          2: font,          3: p42,          4: ec,           5: sol (inverso)
    # night (bg azul muy oscuro -> sol naranja brillante)
    ["\033[48;5;17m", "\033[48;5;229m", "\033[38;5;195m", "\033[48;5;51m", "\033[0m", "\033[38;5;214m"],
    # dark mode (bg casi negro -> sol rojo brillante)
    ["\033[48;5;233m", "\033[48;5;236m", "\033[38;5;236m", "\033[48;5;220m", "\033[0m", "\033[38;5;196m"],
    # satoru (bg blanco -> sol negro)
    ["\033[48;5;255m", "\033[48;5;235m", "\033[38;5;146m", "\033[48;5;45m", "\033[0m", "\033[38;5;16m"],
    # akatsuki (bg negro -> sol rojo brillante)
    ["\033[48;5;233m", "\033[48;5;251m", "\033[38;5;251m", "\033[48;5;124m", "\033[0m", "\033[38;5;196m"],
    # eva01 (bg púrpura -> sol verde neón)
    ["\033[48;5;128m", "\033[48;5;54m", "\033[38;5;54m", "\033[48;5;76m", "\033[0m", "\033[38;5;118m"],
    # uzumaki (bg naranja -> sol azul brillante)
    ["\033[48;5;208m", "\033[48;5;220m", "\033[38;5;238m", "\033[48;5;238m", "\033[0m", "\033[38;5;21m"],
    # ox (bg púrpura oscuro -> sol amarillo brillante)
    ["\033[48;5;55m", "\033[48;5;177m", "\033[38;5;177m", "\033[48;5;99m", "\033[0m", "\033[38;5;226m"]
]

def print_maze(
        maze: Maze,
        pattern_42: set[tuple[int, int]],
        solution_path: list[tuple[int,int]] | None  = None,
        animated_solution: bool = False,
        theme_idx: int = 4,
        random_color: bool = False
    ) -> int:
    if random_color:
        theme_idx = random.randint(0, len(COLOR_PALETTE) - 1)
        
    bg = COLOR_PALETTE[theme_idx][0]
    ft = COLOR_PALETTE[theme_idx][3]
    font = COLOR_PALETTE[theme_idx][2]
    path = COLOR_PALETTE[theme_idx][1]
    ec = COLOR_PALETTE[theme_idx][4]
    sol = COLOR_PALETTE[theme_idx][5] # Color de la solucion

    r_style = bg + font
    
    sol_set: set[tuple[int, int]] = (
        set(solution_path) if solution_path else set[tuple[int, int]]()
    )

    # 🔹 Linea superior inicial
    top_line = r_style
    for x in range(maze.width):
        top_line += "+---"
    top_line += "+" + ec
    print(top_line)

    # 🔹 Por cada fila del maze
    for y in range(maze.height):

        # 👉 Línea de celdas (verticales)
        line_cells = r_style + "|"

        # 👉 Línea inferior (horizontales)
        line_bottom = r_style

        for x in range(maze.width):
            cell = maze.grid[x][y]

            # ===== CONTENIDO DE LA CELDA =====
            if (x, y) == maze.entry_xy or (x, y) == maze.exit_xy:
                content = path + " * " + ec + r_style
            elif (x, y) in pattern_42:
                content = ft + " * " + ec + r_style
            elif (x, y) in sol_set and not animated_solution:
                # Renderiza la solucion de forma instantanea si se solicito
                content = sol + " • " + ec + r_style
            else:
                content = "   "

            # ===== PARED ESTE =====
            east_wall = "|" if cell.walls["E"] else " "

            # Construir línea de celdas
            line_cells += content + east_wall

            # ===== PARED SUR =====
            if cell.walls["S"]:
                line_bottom += "+---"
            else:
                line_bottom += "+   "

        # cerrar lineas
        line_cells += ec
        line_bottom += "+" + ec

        # imprimir ambas
        print(line_cells)
        print(line_bottom)
        
    return theme_idx


def header_yield(file_path: str) -> Generator[dict, None, None]:
    """
    """
    with open(file_path, encoding='utf-8') as f:
        for line in f:
           for c in line:
                yield c

def animate_solution(maze, solution_path: list, theme_idx: int = 4):
    """
    Dibuja paso a paso la solucion sobre el laberinto ya impreso.
    """
    sol_color = COLOR_PALETTE[theme_idx][5] 
    ec = COLOR_PALETTE[theme_idx][4]
    
    # Guarda la posicion actual del cursor
    print("\033[s", end="")
    
    for (x, y) in solution_path:
        # Reestablece el cursor al checkpoint
        print("\033[u", end="")
        
        # Calcula el eje Y vertical y el eje X horizontal
        lines_up = 2 * (maze.height - y)
        cols_right = x * 4 + 2
        
        move_up = f"\033[{lines_up}A"
        move_right = f"\033[{cols_right}C" if cols_right > 0 else ""
        
        # Mueve e imprime sin salto de linea y forzando el flush(necesario)
        print(f"{move_up}{move_right}{sol_color}•{ec}", end="", flush=True)
        time.sleep(0.05)
        
    # Devuelve el curror al punto de partida(posicion final de la impresion)
    print("\033[u", end="")
    print()


def display(
        maze: Maze,
        pattern_42: set[tuple[int, int]],
        solution_path: list[tuple[int,int]] | None = None,
        animated_solution: bool = False,
        theme_idx: int = 4,
        random_color: bool = False
    ) -> None:
    """
    """
    try:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "header.txt")

        for c in header_yield(file_path):
            print(c, end="", flush=True)
            time.sleep(0.005)

    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError) as e:
        print(f"Caught an error: {e}")

    # print_maze retorna el indice de tema utilizado (util por si fue randomizado)
    applied_theme = print_maze(maze, pattern_42, solution_path, animated_solution, theme_idx, random_color)
    
    if solution_path and animated_solution:
        animate_solution(maze, solution_path, applied_theme)