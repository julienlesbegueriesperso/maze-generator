import json
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from pydantic import BaseModel, field_validator
from pydantic.fields import Field


class Frontier(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class Direction(str, Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class Monster(BaseModel):
    name: str


class Cell(BaseModel):
    row: int
    col: int
    north_frontier: Frontier = Frontier.CLOSED
    south_frontier: Frontier = Frontier.CLOSED
    east_frontier: Frontier = Frontier.CLOSED
    west_frontier: Frontier = Frontier.CLOSED
    monsters: List[Monster] = Field(default_factory=list)

    def get_frontier(self, direction: Direction) -> Frontier:
        return getattr(self, f"{direction.value}_frontier")

    def set_frontier(self, direction: Direction, status: Frontier) -> None:
        setattr(self, f"{direction.value}_frontier", status)

    def is_wall_between(self, other: "Cell", direction: Direction) -> bool:
        return self.get_frontier(direction) == Frontier.CLOSED

    def has_passage_to(self, direction: Direction) -> bool:
        return self.get_frontier(direction) == Frontier.OPEN


class Maze(BaseModel):
    cells: List[List[Cell]] = Field(default_factory=list)
    nb_rows: int = 0
    nb_cols: int = 0

    @field_validator("cells", mode="before")
    @classmethod
    def validate_cells_structure(cls, v):
        if isinstance(v, list) and len(v) > 0 and isinstance(v[0], list):
            return v
        return v

    def __init__(self, **data):
        super().__init__(**data)
        if self.cells and isinstance(self.cells[0], list):
            self.nb_rows = len(self.cells)
            self.nb_cols = len(self.cells[0]) if self.cells else 0

    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        if 0 <= row < self.nb_rows and 0 <= col < self.nb_cols:
            return self.cells[row][col]
        return None

    def get_neighbors(self, cell: Cell) -> Dict[Direction, Optional[Cell]]:
        return {
            Direction.NORTH: self.get_cell(cell.row - 1, cell.col),
            Direction.SOUTH: self.get_cell(cell.row + 1, cell.col),
            Direction.EAST: self.get_cell(cell.row, cell.col + 1),
            Direction.WEST: self.get_cell(cell.row, cell.col - 1),
        }

    def get_corner_cells(self) -> Dict[str, Cell]:
        return {
            "northwest": self.cells[0][0],
            "northeast": self.cells[0][self.nb_cols - 1],
            "southwest": self.cells[self.nb_rows - 1][0],
            "southeast": self.cells[self.nb_rows - 1][self.nb_cols - 1],
        }

    def all_corners_connected(self) -> bool:
        # corners = self.get_corner_cells()
        visited: Set[Tuple[int, int]] = set()
        start = (0, 0)
        queue = [start]
        visited.add(start)

        while queue:
            current = queue.pop(0)
            current_cell = self.get_cell(current[0], current[1])
            if not current_cell:
                continue

            neighbors = self.get_neighbors(current_cell)

            for direction, neighbor in neighbors.items():
                if neighbor and current_cell.has_passage_to(direction):
                    neighbor_pos = (neighbor.row, neighbor.col)
                    if neighbor_pos not in visited:
                        visited.add(neighbor_pos)
                        queue.append(neighbor_pos)  # type:ignore

        corner_coords = {
            (0, 0),
            (0, self.nb_cols - 1),
            (self.nb_rows - 1, 0),
            (self.nb_rows - 1, self.nb_cols - 1),
        }
        return corner_coords.issubset(visited)

    def to_json(self) -> str:
        cells_list = [cell for row in self.cells for cell in row]
        return json.dumps(
            {
                "cells": [cell.model_dump() for cell in cells_list],
                "nb_rows": self.nb_rows,
                "nb_cols": self.nb_cols,
            },
            indent=2,
        )

    def to_ascii(self) -> str:
        lines = []

        for row in range(self.nb_rows):
            top_line = ""
            mid_line = ""
            bot_line = ""

            for col in range(self.nb_cols):
                cell = self.cells[row][col]

                top_line += "+"
                if cell.north_frontier == Frontier.OPEN:
                    top_line += "   "
                else:
                    top_line += "───"

                mid_line += "│" if cell.west_frontier == Frontier.CLOSED else " "
                mid_line += " "
                mid_line += "│" if cell.east_frontier == Frontier.CLOSED else " "

                bot_line += "+"
                if cell.south_frontier == Frontier.OPEN:
                    bot_line += "   "
                else:
                    bot_line += "───"

            top_line += "+"
            mid_line += (
                "│"
                if self.cells[row][self.nb_cols - 1].east_frontier == Frontier.CLOSED
                else " "
            )
            bot_line += "+"

            lines.append(top_line)
            lines.append(mid_line)
            lines.append(bot_line)

        return "\n".join(lines)

    @staticmethod
    def create_empty(rows: int, cols: int) -> "Maze":
        cells = [[Cell(row=r, col=c) for c in range(cols)] for r in range(rows)]
        return Maze(cells=cells, nb_rows=rows, nb_cols=cols)
