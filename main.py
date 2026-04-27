import argparse
from generator import MazeGenerator
from renderer import MazeRenderer


def main():
    parser = argparse.ArgumentParser(description="Générateur de labyrinthe")
    parser.add_argument("--rows", "-r", type=int, default=5, help="Nombre de lignes")
    parser.add_argument("--cols", "-c", type=int, default=5, help="Nombre de colonnes")
    parser.add_argument("--output", "-o", choices=["json", "png", "both"], default="png", help="Format de sortie")
    parser.add_argument("--seed", "-s", type=int, help="Graine aléatoire pour la reproductibilité")
    parser.add_argument("--cell-size", type=int, default=40, help="Taille des cellules pour PNG")

    args = parser.parse_args()

    if args.seed is not None:
        import random
        random.seed(args.seed)

    generator = MazeGenerator(args.rows, args.cols)
    maze = generator.generate()

    if args.output in ["json", "both"]:
        print("=== JSON ===")
        print(maze.to_json())
    
    if args.output in ["png", "both"]:
        output_path = f"maze_{args.rows}x{args.cols}.png"
        if args.output == "both":
            print(f"\n=== PNG ({output_path}) ===")
        renderer = MazeRenderer(cell_size=args.cell_size)
        renderer.render(maze, output_path)


if __name__ == "__main__":
    main()