import random
from typing import Optional, Set, Tuple

from models.maze import Direction, Frontier, Maze


class MazeGenerator:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

    def generate(self, with_start_end: bool = False) -> Maze:
        maze = Maze.create_empty(self.rows, self.cols)
        visited: Set[Tuple[int, int]] = set()

        self._dfs_generate(maze, 0, 0, visited)

        if not maze.all_corners_connected():
            self._ensure_corner_connectivity(maze)

        if with_start_end:
            self._assign_start_end(maze)

        return maze

    def _assign_start_end(self, maze: Maze) -> None:
        diagonal_pairs = [
            ((0, 0), (self.rows - 1, self.cols - 1)),
            ((0, self.cols - 1), (self.rows - 1, 0)),
        ]
        start, end = random.choice(diagonal_pairs)
        maze.start = start
        maze.end = end

    def _dfs_generate(
        self, maze: Maze, row: int, col: int, visited: Set[Tuple[int, int]]
    ) -> None:
        visited.add((row, col))

        directions = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
        random.shuffle(directions)

        for direction in directions:
            new_row, new_col = self._get_next_position(row, col, direction)

            if self._is_valid_cell(new_row, new_col, visited):
                self._open_wall(maze, row, col, direction)
                self._dfs_generate(maze, new_row, new_col, visited)

    def _get_next_position(
        self, row: int, col: int, direction: Direction
    ) -> Tuple[int, int]:
        offsets = {
            Direction.NORTH: (-1, 0),
            Direction.SOUTH: (1, 0),
            Direction.EAST: (0, 1),
            Direction.WEST: (0, -1),
        }
        offset = offsets[direction]
        return row + offset[0], col + offset[1]

    def _is_valid_cell(self, row: int, col: int, visited: Set[Tuple[int, int]]) -> bool:
        return (
            0 <= row < self.rows and 0 <= col < self.cols and (row, col) not in visited
        )

    def _open_wall(self, maze: Maze, row: int, col: int, direction: Direction) -> None:
        cell = maze.get_cell(row, col)
        if not cell:
            return
        cell.set_frontier(direction, Frontier.OPEN)

        opposite = self._opposite_direction(direction)
        new_row, new_col = self._get_next_position(row, col, direction)
        neighbor = maze.get_cell(new_row, new_col)
        if not neighbor:
            return
        neighbor.set_frontier(opposite, Frontier.OPEN)

    def _opposite_direction(self, direction: Direction) -> Direction:
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }
        return opposites[direction]

    def _ensure_corner_connectivity(self, maze: Maze) -> None:
        corners = maze.get_corner_cells()

        paths_to_check = [
            (corners["northeast"], Direction.WEST, corners["northwest"]),
            (corners["southwest"], Direction.EAST, corners["southeast"]),
            (corners["northwest"], Direction.SOUTH, corners["southwest"]),
        ]

        for start_cell, direction, target_corner in paths_to_check:
            if not start_cell.has_passage_to(direction):
                current = start_cell
                while current != target_corner:
                    neighbors = maze.get_neighbors(current)
                    next_cell = None

                    for d, n in neighbors.items():
                        if n and current.has_passage_to(d) and n != target_corner:
                            continue
                        if n and not current.has_passage_to(d) and d == direction:
                            self._open_wall(maze, current.row, current.col, d)
                            next_cell = n

                            break

                    if next_cell:
                        current = next_cell
                    else:
                        break
