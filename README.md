# Générateur de Labyrinthe

Un générateur de labyrinthes écrit en Python utilisant l'algorithme de parcours en profondeur (DFS). Le projet produit des labyrinthes parfaits où tous les coins sont accessibles depuis n'importe quel point.

## Prérequis

- Python 3.14 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

1. Clonez le dépôt ou téléchargez les fichiers sources.

2. Installez les dépendances :

```bash
pip install -e .
```

## Utilisation

Lancez le générateur via la ligne de commande :

```bash
python main.py [OPTIONS]
```

### Options disponibles

| Option | Description | Valeur par défaut |
|--------|-------------|-------------------|
| `-r`, `--rows` | Nombre de lignes du labyrinthe | 5 |
| `-c`, `--cols` | Nombre de colonnes du labyrinthe | 5 |
| `-o`, `--output` | Format de sortie : `json`, `png` ou `both` | `png` |
| `-s`, `--seed` | Graine aléatoire pour la reproductibilité | None |
| `--cell-size` | Taille des cellules en pixels (pour PNG) | 40 |

### Exemples d'utilisation

Générer un labyrinthe 5x5 et l'enregistrer en PNG :

```bash
python main.py -r 5 -c 5
```

Générer un labyrinthe 10x10 avec une graine pour reproductibilité :

```bash
python main.py -r 10 -c 10 --seed 42
```

Générer la sortie en JSON :

```bash
python main.py -r 8 -c 8 -o json
```

Générer les deux formats de sortie :

```bash
python main.py -r 6 -c 6 -o both
```

Personnaliser la taille des cellules dans l'image :

```bash
python main.py -r 20 -c 20 --cell-size 30
```

## Structure du projet

```
maze-generator/
├── main.py              # Point d'entrée et interface CLI
├── renderer.py          # Génération d'images PNG
├── models/
│   └── maze.py          # Modèles de données (Cell, Maze, Direction, Frontier)
├── generator/
│   └── generator.py     # Algorithme de génération du labyrinthe
└── pyproject.toml       # Configuration du projet
```

## Détails techniques

### Algorithme de génération

Le générateur utilise un algorithme de parcours en profondeur (DFS) avec backtracking :

1. Commence depuis la cellule (0, 0)
2. Explore aléatoirement les directions disponibles
3. Ouvre les murs entre les cellules accessibles
4. Assure que tous les coins du labyrinthe sont connectés

### Format JSON

La sortie JSON contient :

- `nb_rows` : nombre de lignes
- `nb_cols` : nombre de colonnes
- `cells` : tableau de toutes les cellules avec leurs frontières

Chaque cellule possède les propriétés suivantes :

- `row`, `col` : coordonnées de la cellule
- `north_frontier`, `south_frontier`, `east_frontier`, `west_frontier` : état des frontières (`open` ou `closed`)
- `monsters` : liste des monstres (vide par défaut)

### Format PNG

L'image générée affiche :

- Les murs en noir
- Le fond en blanc
- Les coins marqués par des cercles rouges

## Licence

Voir le fichier LICENSE pour les détails.