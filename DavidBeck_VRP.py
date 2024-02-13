import random
import sys
import math
from copy import deepcopy


# Class that represents a load with these params: ID, Pickup, and Dropoff coords
class Load:
    def __init__(self, load_id, pickup, dropoff):
        self.load_id = load_id # Unique id for load
        self.pickup = pickup # Pickup cords (x,y)
        self.dropoff = dropoff # Dropoff cords (x,y)

    # Calculation of Euclidian distance between current load pickup and another point
    def distance(self, other):
        return ((self.pickup[0] - other[0])**2 + (self.pickup[1] - other[1])**2)**0.5

# Parse a string of cordinates and returns a tuple of x,y
def parse_coordinates(coord_str):
    coord_str = coord_str.strip('()')
    x, y = map(float, coord_str.split(','))
    return x, y

#Reads the input file
#Creates Load obj for each line
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

# Calculation of the total distance of a route 
def total_route_distance(route):
    distance = 0
    depot = (0, 0) # Start and end point denoted as the depot
    current_location = depot
    for load in route:
        # Adding distance from current location to loads's pickup and its dropoff
        distance += load.distance(current_location) + load.distance(load.dropoff)
        current_location = load.dropoff
    distance += Load(0, current_location, depot).distance(depot)  # Add the distance and then Return to depot
    return distance

# Vailidity function to ensure its below the max time allowed
def is_valid_route(route, max_time=720):
    return total_route_distance(route) <= max_time

# Crossover operation betweed 2 parent routes to produce "offspring"
def crossover(parent1, parent2):
    child1, child2 = [], [] # Create child routes
    idx1, idx2 = sorted(random.sample(range(len(parent1)), 2)) # Select 2 random crossover points
    # Copy  segments from parents to children
    child1.extend(parent1[idx1:idx2])
    child2.extend(parent2[idx1:idx2])
    # Fill remaining slots in children with loads that are not already included
    child1.extend([item for item in parent2 if item not in child1])
    child2.extend([item for item in parent1 if item not in child2])
    return child1, child2

# Mutates a given route based on a mutation rate
def mutate(route, mutation_rate):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            # Select a random load in the route and swap it with another
            swap_with = random.randint(0, len(route) - 1)
            route[i], route[swap_with] = route[swap_with], route[i]
    return route

# Main algorithim for solving the VRP
def genetic_algorithm(loads, population_size=50, generations=100, mutation_rate=0.01):
    # Initialize populaton filled with rand routes
    population = [random.sample(loads, len(loads)) for _ in range(population_size)]
    for _ in range(generations):

        # Sort the population off of route distance "fitness"
        population = sorted(population, key=lambda x: total_route_distance(x))

        # Implement Elitism: Carry the best solutions to the next generation
        new_population = population[:2]  
        # Generate a new pop through crossover function and also mutation function
        while len(new_population) < population_size:
            # Take top 10 solutions and select the parents that will make the children
            parent1, parent2 = random.sample(population[:10], 2)
            # Use crossover function to create the children
            child1, child2 = crossover(parent1, parent2)
            # Mutate children and add them to new population
            new_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])
        # Update the population with the newly generated children
        population = new_population
    # ID the best solution for the final population
    best_solution = min(population, key=lambda x: total_route_distance(x))
    # Make routes based on the above best solution
    routes = []
    current_route = []
    for load in best_solution:
        current_route.append(load)
        # Make sure the current route is valid, if not then start new route
        if not is_valid_route(current_route):
            current_route.pop()  
            routes.append(current_route)
            current_route = [load]
    # Append any remaining
    if current_route:
        routes.append(current_route)
    # Return the list of routes.
    # Each route contains load ID's
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