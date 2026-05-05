import argparse
import sys

from generator.generator import MazeGenerator
from renderer import MazeRenderer

sys.setrecursionlimit(10**6)


def main():
    parser = argparse.ArgumentParser(description="Générateur de labyrinthe")
    parser.add_argument("--rows", "-r", type=int, default=5, help="Nombre de lignes")
    parser.add_argument("--cols", "-c", type=int, default=5, help="Nombre de colonnes")
    parser.add_argument(
        "--output",
        "-o",
        choices=["json", "png", "both"],
        default="png",
        help="Format de sortie",
    )
    parser.add_argument(
        "--seed", "-s", type=int, help="Graine aléatoire pour la reproductibilité"
    )
    parser.add_argument(
        "--cell-size", type=int, default=40, help="Taille des cellules pour PNG"
    )
    parser.add_argument(
        "--with-solution",
        action="store_true",
        help="Générer avec un point de départ et d'arrivée aléatoires et afficher la solution",
    )

    args = parser.parse_args()

    if args.rows > 500:
        print("Nombre de lignes trop élevé, limité à 500")
        args.rows = 500

    if args.cols > 500:
        print("Nombre de colonnes trop élevé, limité à 500")
        args.cols = 500

    if args.seed is not None:
        import random

        random.seed(args.seed)

    generator = MazeGenerator(args.rows, args.cols)
    maze = generator.generate(with_start_end=args.with_solution)

    if maze.start and maze.end:
        solution = maze.find_path()
        if solution:
            print(f"Chemin trouvé: {len(solution.path)} étapes")
        else:
            print("Aucun chemin trouvé")
    else:
        solution = None

    if args.output in ["json", "both"]:
        print("=== JSON ===")
        print(maze.to_json())

    if args.output in ["png", "both"]:
        base_name = f"maze_{args.rows}x{args.cols}"
        if args.with_solution:
            output_path_no_solution = f"{base_name}.png"
            output_path = f"{base_name}_with_solution.png"
            print(f"\n=== PNG ({output_path_no_solution}) ===")
            renderer = MazeRenderer(cell_size=args.cell_size)
            renderer.render(maze, output_path_no_solution, solution=None)
            print(f"\n=== PNG ({output_path}) ===")
            renderer.render(maze, output_path, solution=solution)
        else:
            output_path = f"{base_name}.png"
            print(f"\n=== PNG ({output_path}) ===")
            renderer = MazeRenderer(cell_size=args.cell_size)
            renderer.render(maze, output_path, solution=solution)


if __name__ == "__main__":
    main()
