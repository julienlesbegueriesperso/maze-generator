from PIL import Image, ImageDraw
from models.maze import Maze, Frontier, MazeSolution


class MazeRenderer:
    def __init__(
        self,
        cell_size: int = 40,
        wall_color: tuple = (0, 0, 0),
        bg_color: tuple = (255, 255, 255),
        start_color: tuple = (0, 255, 0),
        end_color: tuple = (255, 0, 0),
        path_color: tuple = (0, 0, 255),
    ):
        self.cell_size = cell_size
        self.wall_color = wall_color
        self.bg_color = bg_color
        self.start_color = start_color
        self.end_color = end_color
        self.path_color = path_color
        self.wall_width = max(2, cell_size // 10)

    def render(
        self,
        maze: Maze,
        output_path: str,
        solution: MazeSolution = None,
    ) -> None:
        width = maze.nb_cols * self.cell_size
        height = maze.nb_rows * self.cell_size

        img = Image.new("RGB", (width, height), self.bg_color)
        draw = ImageDraw.Draw(img)

        for row in range(maze.nb_rows):
            for col in range(maze.nb_cols):
                self._draw_cell(draw, maze, row, col)

        if solution:
            self._draw_path(draw, solution.path)

        if maze.start:
            self._draw_marker(draw, maze.start, self.start_color, "D")
        if maze.end:
            self._draw_marker(draw, maze.end, self.end_color, "A")

        img.save(output_path)
        print(f"Image sauvegardée : {output_path}")

    def _draw_cell(self, draw: ImageDraw.ImageDraw, maze: Maze, row: int, col: int) -> None:
        cell = maze.cells[row][col]
        x = col * self.cell_size
        y = row * self.cell_size
        size = self.cell_size

        if cell.north_frontier == Frontier.CLOSED:
            draw.line([(x, y), (x + size, y)], self.wall_color, self.wall_width)

        if cell.south_frontier == Frontier.CLOSED:
            draw.line(
                [(x, y + size), (x + size, y + size)], self.wall_color, self.wall_width
            )

        if cell.west_frontier == Frontier.CLOSED:
            draw.line([(x, y), (x, y + size)], self.wall_color, self.wall_width)

        if cell.east_frontier == Frontier.CLOSED:
            draw.line(
                [(x + size, y), (x + size, y + size)], self.wall_color, self.wall_width
            )

    def _draw_path(self, draw: ImageDraw.ImageDraw, path: list) -> None:
        if not path or len(path) < 2:
            return

        for i in range(len(path) - 1):
            row, col = path[i]
            next_row, next_col = path[i + 1]

            x1 = col * self.cell_size + self.cell_size // 2
            y1 = row * self.cell_size + self.cell_size // 2
            x2 = next_col * self.cell_size + self.cell_size // 2
            y2 = next_row * self.cell_size + self.cell_size // 2

            draw.line([(x1, y1), (x2, y2)], self.path_color, self.cell_size // 3)

    def _draw_marker(
        self, draw: ImageDraw.ImageDraw, pos: tuple, color: tuple, text: str
    ) -> None:
        row, col = pos
        x = col * self.cell_size
        y = row * self.cell_size
        size = self.cell_size

        draw.rectangle(
            [x + size // 4, y + size // 4, x + 3 * size // 4, y + 3 * size // 4],
            fill=color,
        )