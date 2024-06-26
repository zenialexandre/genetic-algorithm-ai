import math
import numpy as np
import matplotlib.pyplot as plt
from random import randint

def initialize_chromosomes(chromosomes_matrix) -> list:
    for row in range(len(chromosomes_matrix)):
        chromosomes_matrix[row] = np.random.choice(np.arange(20), size=len(chromosomes_matrix), replace=False)
    return chromosomes_matrix

def get_calculated_fitness(chromosomes_matrix, distances_matrix) -> list:
    fitness_utility  = []
    total_distance = 0

    for chromosome in chromosomes_matrix:
        for index in range(len(chromosome)):
            if (index == len(chromosome) - 1):
                total_distance += execute_fitness_calculation(distances_matrix[0][chromosome[-1]], 
                                                              distances_matrix[0][chromosome[-1]],
                                                              distances_matrix[1][chromosome[0]],
                                                              distances_matrix[1][chromosome[0]])
            else:
                total_distance += execute_fitness_calculation(distances_matrix[0][chromosome[index]], 
                                                              distances_matrix[0][chromosome[index]],
                                                              distances_matrix[1][chromosome[index + 1]],
                                                              distances_matrix[1][chromosome[index + 1]])
        fitness_utility.append(total_distance)
        total_distance = 0
    return np.reshape(fitness_utility, (20, 1))

def execute_fitness_calculation(origin_chromosome_x, origin_chromosome_y, destiny_chromosome_x, destiny_chromosome_y) -> float:
    return math.sqrt(math.pow(origin_chromosome_x - destiny_chromosome_x, 2) + math.pow(origin_chromosome_y - destiny_chromosome_y, 2))

def get_chromosomes_merged_with_fitness(chromosomes_matrix, fitness_distances_matrix) -> list:
    return np.hstack((chromosomes_matrix, fitness_distances_matrix))

def get_chromosomes_ordered_by_fitness(chromosomes_matrix) -> list:
    ordering_indexes = np.argsort(chromosomes_matrix[:, -1])
    return chromosomes_matrix[ordering_indexes]

def get_best_chromosomes_from_matrix(chromosomes_matrix) -> list:
    return chromosomes_matrix[:10, :]

def generate_roulette(chromosomes_matrix) -> list:
    return np.repeat(chromosomes_matrix, range(len(chromosomes_matrix), 0, -1), axis=0)

def choose_parent_chromosomes(roulette_array) -> list:
    parents_chromosomes = []
    roulette_array_len = len(roulette_array)
    parents_chromosomes.extend([roulette_array[randint(0, roulette_array_len - 1)], roulette_array[randint(0, roulette_array_len - 1)]])
    return parents_chromosomes

def generate_children_chromosomes(roulette_array) -> list:
    children_chromosomes = []

    for _ in range(5):
        chromosome_recombination_completed = False
        parent_chromosomes = choose_parent_chromosomes(roulette_array)
        gene_index = randint(0, 19)

        while (not chromosome_recombination_completed):
            first_parent_value = parent_chromosomes[0][gene_index]
            second_parent_value = parent_chromosomes[1][gene_index]
            parent_chromosomes[0][gene_index] = second_parent_value
            parent_chromosomes[1][gene_index] = first_parent_value
            repeated_indexes = np.where(parent_chromosomes[0] == second_parent_value)[0]

            if (len(repeated_indexes) > 1):
                gene_index = repeated_indexes[np.where(repeated_indexes != gene_index)[0][0]]
            else:
                chromosome_recombination_completed = True
                children_chromosomes.extend([parent_chromosomes[0], parent_chromosomes[1]])
            continue
    return generate_mutated_children_chromosomes(children_chromosomes)

def generate_mutated_children_chromosomes(final_children_chromosomes) -> list:
    for children_chromosome in final_children_chromosomes:
        children_chromosome_len = len(children_chromosome)
        first_randomized_index = randint(0, children_chromosome_len - 1)
        second_randomized_index = randint(0, children_chromosome_len - 1)

        while (first_randomized_index == second_randomized_index):
            second_randomized_index = randint(0, children_chromosome_len - 1)

        first_children_value = children_chromosome[first_randomized_index]
        second_children_value = children_chromosome[second_randomized_index]
        children_chromosome[first_randomized_index] = second_children_value
        children_chromosome[second_randomized_index] = first_children_value
    return final_children_chromosomes

def get_new_formed_chromosomes(chromosomes_matrix, childrens_chromosomes) -> list:
    return np.concatenate((chromosomes_matrix[:, :-1], childrens_chromosomes), axis=0)

def display_fitness_results(fitness_results, ITERATION_RANGE) -> None:
    x_array = []

    for index in range(ITERATION_RANGE):
        x_array.append(index)

    plt.plot(x_array, fitness_results)
    plt.xlabel('Iteration Range')
    plt.ylabel('Fitness Values')
    plt.title('Genetic Algorithm (Salesman Problematic)')
    plt.show()
