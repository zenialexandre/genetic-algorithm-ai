import numpy as np
from random import randint
import matplotlib.pyplot as plt
import math

def initialize_chromosomes(chromosomes_matrix) -> []:
    for row in range(len(chromosomes_matrix)):
        chromosomes_matrix[row] = np.random.choice(np.arange(20), size=len(chromosomes_matrix), replace=False)
    return chromosomes_matrix

def get_calculated_fitness(chromosomes_matrix, distances_matrix) -> []:
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

def get_chromosomes_merged_with_fitness(chromosomes_matrix, fitness_distances_matrix) -> []:
    return np.hstack((chromosomes_matrix, fitness_distances_matrix))

def get_chromosomes_ordered_by_fitness(chromosomes_matrix) -> []:
    ordering_indexes = np.argsort(chromosomes_matrix[:, -1])
    return chromosomes_matrix[ordering_indexes]

def get_best_chromosomes_from_matrix(chromosomes_matrix) -> []:
    return chromosomes_matrix[:10, :]

def generate_roulette(chromosomes_matrix) -> []:
    return np.repeat(chromosomes_matrix, range(len(chromosomes_matrix), 0, -1), axis=0)

def choose_parent_chromosomes(roulette_array) -> []:
    parents_chromosomes = []
    roulette_array_len = len(roulette_array)

    while (len(parents_chromosomes) < 2):
        parents_chromosomes.clear()
        parents_chromosomes.append(roulette_array[randint(0, roulette_array_len - 1)])
        second_parent_index = randint(0, roulette_array_len - 1)

        if (not np.array_equal(parents_chromosomes[0], roulette_array[second_parent_index])):  
            parents_chromosomes.append(roulette_array[second_parent_index])
        continue

    return parents_chromosomes

def generate_children_chromosomes(roulette_array) -> []:
    final_children_chromosomes = []
    childrens_chromosomes = []
    iteration_counter = 0

    for _ in range(5):
        parents_chromosomes = choose_parent_chromosomes(roulette_array)
        parents_chromosomes_len = len(parents_chromosomes)
        iteration_counter = 0
        childrens_chromosomes.clear()

        while (len(childrens_chromosomes) < 2):
            iteration_counter = iteration_counter + 1

            if (iteration_counter == 1):
                parents_chromosome_access_index = randint(0, parents_chromosomes_len - 1);
                parents_chromosomes[0][parents_chromosome_access_index] = parents_chromosomes[1][parents_chromosome_access_index]
                parents_chromosomes[1][parents_chromosome_access_index] = parents_chromosomes[0][parents_chromosome_access_index]
                _, duplicated_elements_count = np.unique(parents_chromosomes, return_counts=True)

                if (np.any(np.where(duplicated_elements_count < 2))):
                    childrens_chromosomes.extend([parents_chromosomes[0], parents_chromosomes[1]])
            else:
                _, duplicated_elements_count = np.unique(parents_chromosomes, return_counts=True)
                duplicated_element_index = np.where(duplicated_elements_count < 2)
                parents_chromosomes[0][duplicated_element_index[0]] = parents_chromosomes[1][duplicated_element_index[0]]
                parents_chromosomes[1][duplicated_element_index[0]] = parents_chromosomes[0][duplicated_element_index[0]]
                _, new_duplicated_elements_count = np.unique(parents_chromosomes, return_counts=True)

                if (not np.any(np.where(new_duplicated_elements_count < 2))):
                    childrens_chromosomes.extend([parents_chromosomes[0], parents_chromosomes[1]])
                continue

        final_children_chromosomes.extend([childrens_chromosomes[0], childrens_chromosomes[1]])
    
    return generate_mutated_children_chromosomes(final_children_chromosomes)

def generate_mutated_children_chromosomes(final_children_chromosomes) -> []:
    for children_chromosome in final_children_chromosomes:
        children_chromosome_len = len(children_chromosome)
        first_randomized_index = randint(0, children_chromosome_len - 1)
        second_randomized_index = randint(0, children_chromosome_len - 1)

        while (first_randomized_index == second_randomized_index):
            second_randomized_index = randint(0, children_chromosome_len - 1)
        
        children_chromosome[first_randomized_index] = children_chromosome[second_randomized_index]
        children_chromosome[second_randomized_index] = children_chromosome[first_randomized_index]

    return final_children_chromosomes

def get_new_formed_chromosomes(chromosomes_matrix, childrens_chromosomes) -> []:
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
