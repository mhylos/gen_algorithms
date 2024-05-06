from random import randint, sample
import csv


class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value

    def __str__(self):
        return f'{self.name}, Weight: {self.weight}, Value: {self.value}'


class Backpack:
    def __init__(self, items: list[Item] = []):
        self.items = items

    def get_weight(self):
        return sum([x.weight for x in self.items])

    def get_value(self):
        return sum([x.value for x in self.items])

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def remove_random(self):
        self.items.pop(randint(0, len(self.items) - 1))

    def get_binary(self, items):
        binary = []
        for item in items:
            if item in self.items:
                binary.append(1)
            else:
                binary.append(0)
        return binary

    def is_weight_exceeding(self, max_weight):
        return self.get_weight() > max_weight

    def __str__(self):
        return f'Items, {[x.name for x in self.items]}, Weight: {self.get_weight()}, Value: {self.get_value()}'

###


def read_csv(file):
    items = []
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            items.append(Item(row[0], int(row[1]), int(row[2])))
    return items


ITEMS = read_csv('items.csv')


def encoding(items, max_weight: int):
    weight = 0
    available_items = items.copy()
    selected_items = []
    while weight < max_weight:
        item = sample(available_items, 1)[0]
        if weight + item.weight > max_weight:
            break
        selected_items.append(item)
        available_items.remove(item)
        weight += item.weight
    return selected_items


def generate_population(pop_size: int, max_weight: int):
    population = []
    for i in range(pop_size):
        generated_backpack = Backpack(encoding(ITEMS, max_weight))
        # while generated_backpack.is_weight_exceeding(MAX_WEIGHT):
        #     print('Regenerating, weight exceeded ' + str(generated_backpack))
        #     generated_backpack = encoding(ITEMS)
        population.append(generated_backpack)
    return population


def crossover(parent1: Backpack, parent2: Backpack, max_weight: int):
    child = Backpack(parent1.items.copy())
    for item in parent2.items:
        if item not in child.items:
            child.add_item(item)

    while child.is_weight_exceeding(max_weight):
        item = sample(child.items, 1)[0]
        child.remove_item(item)

    return child


def mutation(bp: Backpack, mutation_rate: int, max_weight: int):
    if randint(0, 100) < mutation_rate:
        return bp
    item = sample(ITEMS, 1)[0]
    if item in bp.items:
        bp.remove_item(item)
    else:
        if bp.get_weight() + item.weight > max_weight:
            bp.remove_random()
        else:
            bp.add_item(item)
    return bp


def selection(population: list[Backpack], best_percentage: float, random_percentage: float):
    best = int(len(population) * best_percentage)
    randoms = int(len(population) * random_percentage)

    sorted_pop = sorted(population, key=lambda x: x.get_value(), reverse=True)

    return sorted_pop[:best] + sample(sorted_pop[best:], randoms)


def genetic_algorithm(population: list[Backpack], best_percentage: float, random_percentage: float, mutation_rate: int, max_weight: int):
    new_generation = selection(
        population, best_percentage, random_percentage)
    while len(new_generation) < len(population):
        parent1, parent2 = sample(new_generation, 2)
        child = crossover(parent1, parent2, max_weight)
        new_generation.append(mutation(child, mutation_rate, max_weight))
    # for bp in new_generation:
    #     print(bp)
    return new_generation


# population = generate_population(50)
# for i in range(1000):
#     print('Generation ' + str(i))
#     population = genetic_algorithm(population)
#     print('best of generation:' + str(max(population, key=lambda x: x.get_value())))
