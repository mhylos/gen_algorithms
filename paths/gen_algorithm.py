from random import sample, randint
import numpy as np


class Coords:
    def __init__(self, matrix_index: int, x: int, y: int, name: str):
        self.matrix_index = matrix_index
        self.name = name
        self.x = x
        self.y = y

    def distance_to(self, other: 'Coords', distances_matrix: np.ndarray):
        if distances_matrix[self.matrix_index, other.matrix_index] == 0:
            distances_matrix[self.matrix_index, other.matrix_index] = (
                (self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return distances_matrix[self.matrix_index, other.matrix_index]

    def __str__(self):
        return f'({self.x}, {self.y})'


class Path:
    def __init__(self, coords: list[Coords]):
        self.coords = coords

    def __str__(self):
        return ' -> '.join(str(coord) for coord in self.coords)

    def distance(self, distances_matrix: np.ndarray):
        return sum(
            (self.coords[i].distance_to(self.coords[i + 1], distances_matrix)
             for i in range(len(self.coords) - 1))
        )


def read_csv():
    with open('cities3.csv') as f:
        for index, line in enumerate(f):
            name, x, y = line.strip().split(',')
            yield Coords(index, int(x), int(y), name)


coords = list(read_csv())


def get_max_x():
    return max(coords, key=lambda coord: coord.x).x


def get_max_y():
    return max(coords, key=lambda coord: coord.y).y


def generate_random_path():
    return Path(sample(coords, len(coords)))


def generate_random_population(population_size):
    for _ in range(population_size):
        yield generate_random_path()


def mutation(path: Path, mutation_rate: int):
    if randint(0, 100) > mutation_rate:
        return path
    index1, index2 = sample(range(len(path.coords)), 2)
    path.coords[index1], path.coords[index2] = path.coords[index2], path.coords[index1]
    return path


def crossover(path1: Path, path2: Path):
    cross_point = randint(1, len(path1.coords) - 1)
    child_coords = Path(path1.coords[:cross_point])
    missing_coords = path1.coords[cross_point:]
    for coord in path2.coords[cross_point:]:
        if coord not in child_coords.coords:
            missing_coords.remove(coord)
            child_coords.coords.append(coord)

    return Path(child_coords.coords + missing_coords)


def selection(population: list[Path], best_percentage: float, random_percentage: float, distances_matrix: np.ndarray):
    best = int(len(population) * best_percentage)
    randoms = int(len(population) * random_percentage)

    sorted_population = sorted(
        population, key=lambda path: path.distance(distances_matrix))

    return sorted_population[:best] + sample(sorted_population[best:], randoms)


def genetic_algorithm(population: list[Path], best_percentage: float, random_percentage: float, mutation_rate=int, distances_matrix=np.zeros((len(coords), len(coords)))):
    new_generation = selection(
        population, best_percentage, random_percentage, distances_matrix)
    while len(new_generation) < len(population):
        parent1, parent2 = sample(population, 2)
        child = crossover(parent1, parent2)
        new_generation.append(mutation(child, mutation_rate))
    # for path in new_generation:
    #     print(path, path.distance(distances_matrix))
    return new_generation, distances_matrix


# population = list(generate_random_population(50))
# for i in range(100):
#     print('Generation ' + str(i))
#     population = genetic_algorithm(population)
