from .maze_generator import (
    MazeGenerator,
    Cell,
    MazeGenerationError,
    MazeIOError
)
block_42_pattern = MazeGenerator.block_42_pattern

__all__ = [
    "MazeGenerator",
    "Cell",
    "MazeGenerationError",
    "MazeIOError",
    "block_42_pattern"
]
