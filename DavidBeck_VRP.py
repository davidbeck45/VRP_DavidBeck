import random
import sys
import math
from copy import deepcopy

class Load:
    def __init__(self, load_id, pickup, dropoff):
        self.load_id = load_id
        self.pickup = pickup
        self.dropoff = dropoff

    def distance(self, other):
        #euclid dist between 2 pts
        return ((self.pickup[0] - other[0])**2 + (self.pickup[1] - other[1])**2)**0.5


def parse_coordinates(coord_str):
    coord_str = coord_str.strip('()')
    x, y = map(float, coord_str.split(','))
    return x, y

def read_input_file(filename):
    loads = []
    with open(filename, 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            parts = line.strip().split()
            load_id = int(parts[0])
            pickup = parse_coordinates(parts[1])
            dropoff = parse_coordinates(parts[2])
            loads.append(Load(load_id, pickup, dropoff))
    return loads

def total_route_distance(route):
    distance = 0
    depot = (0, 0)
    current_location = depot
    for load in route:
        distance += load.distance(current_location) + load.distance(load.dropoff)
        current_location = load.dropoff
    distance += Load(0, current_location, depot).distance(depot)  # Return to depot
    return distance

def is_valid_route(route, max_time=720):
    return total_route_distance(route) <= max_time

def crossover(parent1, parent2):
    child1, child2 = [], []
    idx1, idx2 = sorted(random.sample(range(len(parent1)), 2))
    child1.extend(parent1[idx1:idx2])
    child2.extend(parent2[idx1:idx2])
    child1.extend([item for item in parent2 if item not in child1])
    child2.extend([item for item in parent1 if item not in child2])
    return child1, child2

def mutate(route, mutation_rate):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            swap_with = random.randint(0, len(route) - 1)
            route[i], route[swap_with] = route[swap_with], route[i]
    return route

def genetic_algorithm(loads, population_size=50, generations=100, mutation_rate=0.01):
    population = [random.sample(loads, len(loads)) for _ in range(population_size)]
    for _ in range(generations):
        population = sorted(population, key=lambda x: total_route_distance(x))
        new_population = population[:2]  # Elitism: Carry the best solutions to the next generation
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:10], 2)  # Select from the top 10 solutions
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])
        population = new_population

    best_solution = min(population, key=lambda x: total_route_distance(x))
    routes = []
    current_route = []
    for load in best_solution:
        current_route.append(load)
        if not is_valid_route(current_route):
            current_route.pop()  
            routes.append(current_route)
            current_route = [load]
    if current_route:
        routes.append(current_route)
    return [[load.load_id for load in route] for route in routes]
            
def main():
    if len(sys.argv) < 2:
        print("Usage: python vrp_solver.py <input_file_path>")
        sys.exit(1)

    input_filename = sys.argv[1]
    loads = read_input_file(input_filename)
    driver_routes = genetic_algorithm(loads)

    # Output the solution
    for route in driver_routes:
        print(route)

if __name__ == "__main__":
    main()
