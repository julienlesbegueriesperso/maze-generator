from PIL import Image, ImageDraw
from models.maze import Maze, Frontier


class MazeRenderer:
    def __init__(self, cell_size: int = 40, wall_color: tuple = (0, 0, 0), bg_color: tuple = (255, 255, 255)):
        self.cell_size = cell_size
        self.wall_color = wall_color
        self.bg_color = bg_color
        self.wall_width = max(2, cell_size // 10)

    def render(self, maze: Maze, output_path: str) -> None:
        width = maze.nb_cols * self.cell_size
        height = maze.nb_rows * self.cell_size

        img = Image.new("RGB", (width, height), self.bg_color)
        draw = ImageDraw.Draw(img)

        for row in range(maze.nb_rows):
            for col in range(maze.nb_cols):
                self._draw_cell(draw, maze, row, col)

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
            draw.line([(x, y + size), (x + size, y + size)], self.wall_color, self.wall_width)

        if cell.west_frontier == Frontier.CLOSED:
            draw.line([(x, y), (x, y + size)], self.wall_color, self.wall_width)

        if cell.east_frontier == Frontier.CLOSED:
            draw.line([(x + size, y), (x + size, y + size)], self.wall_color, self.wall_width)

        corners = maze.get_corner_cells()
        if cell in corners.values():
            cx = x + size // 2
            cy = y + size // 2
            r = size // 5
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 0, 0))