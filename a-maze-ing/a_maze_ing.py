#!/usr/bin/env python3
import sys
from controller import setup_config, build_maze, run_visuals, DependencyError
from config import MazeConfigError, ImposibleMazeError
from ui import DisplayMazeError
from mazegen import MazeGenerationError, MazeIOError


def main() -> None:
    """Main function to run the maze generation and visualization."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    try:
        config = setup_config(sys.argv[1])
        maze, pattern = build_maze(config)
        run_visuals(maze, pattern, config)

    except (
        ImposibleMazeError,
        MazeConfigError,
        DependencyError,
        DisplayMazeError,
        MazeIOError,
        MazeGenerationError
    ) as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nUser interrupted. Bye!")
        raise SystemExit(0)
