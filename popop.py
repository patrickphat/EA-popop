import numpy as np
import random
from typing import List 
from pprint import pprint

# CONFIGs
# Fitness mode: "trap5", "onemax"
FITNESS_MODE = "onemax"

# Crossover mode: "uniform", "onepoint"
CROSSOVER_MODE  = "uniform"

# population and num bits
POP_SIZE = 5
N_BITS  = 4

def initialize_population(pop_size:int = 20, n_bits:int = 40):
    population = np.zeros((pop_size, n_bits))
    if pop_size %2 == 0:
        half_pop = int(pop_size/2)
        population[:half_pop,:] = 1
    else:
        ceil_half_pop = int(np.ceil(pop_size/2))
        population[:ceil_half_pop,:] = 1

    for i in range(n_bits):
        population[:,i] = np.random.permutation(population[:,i])

    return population

def one_max(individual_bits: np.array):
    return np.sum(individual_bits)

def trap_n(individual_bits: np.array, n_traps:int = 5):
    num_bits = individual_bits.shape[0]
    sum_all_block = 0

    if num_bits % n_traps != 0:
        raise ValueError(f"The input bits should be the multiple of {n_traps}, found {num_bits}")
    else:
        for i in range(0,num_bits,n_traps):
            sum_block = np.sum(individual_bits[i: i + n_traps])
            if sum_block == n_traps:
                sum_all_block += n_traps
            else:
                sum_all_block += (n_traps - 1 - sum_block)
    return sum_all_block


def get_fitness_func(fitness_mode:str = "onemax"):
    if fitness_mode == "onemax":
        return one_max
    elif fitness_mode == "trap5":
        return trap_n
    else:
        raise ValueError(f"This fitness function {fitness_mode} does not support")

def calc_fitness_population(population: np.array, fitness_mode:str = "onemax"):
    fitness_func = get_fitness_func(fitness_mode)
    fitnesses = []
    for individual in population:
        fitnesses.append(fitness_func(individual))
    return np.mean(fitnesses)

def get_best_individual(group:np.array, fitness_mode:str = "onemax"):
    fitnesses = []
    fitness_func = get_fitness_func(fitness_mode)
    for individual in group:
        fitnesses.append(fitness_func(individual))
    idx_best_individual = fitnesses.index(max(fitnesses))
    return group[idx_best_individual][:]

def tournament_selection(population: np.array, tournament_size:int = 4, fitness_mode:str = "onemax"):
    pop_size = population.shape[0]
    np.random.shuffle(population)
    n_groups = int(np.ceil(pop_size/tournament_size))
    reserved_individual = []
    groups = np.array_split(population, n_groups)
    for group in groups:
        best_indi = get_best_individual(group, fitness_mode)
        reserved_individual.append(best_indi)
    return np.array(reserved_individual)


def uniform_crossover(individual_1:np.array, individual_2:np.array, thresh: int = 0.5):
    offspring_1 = individual_1.copy()
    offspring_2 = individual_2.copy()
    for i,_ in enumerate(offspring_1):
        ran_num = np.random.uniform()
        if ran_num > thresh:
            # swap 2 bits at i-th position
            temp_bit = offspring_1[i]
            offspring_1[i] = offspring_2[i]
            offspring_2[i] = temp_bit
        else:
            continue
    return [offspring_1, offspring_2]

def one_point_crossover(individual_1:np.array, individual_2:np.array, thresh: int = 0.5):
    offspring_1 = individual_1.copy()
    offspring_2 = individual_2.copy()
    ran_num = np.random.uniform()
    array_size = individual_1.shape[0]
    chosen_idx = int(np.ceil(array_size*ran_num))
    # swap left side 
    temp = offspring_1[:chosen_idx].copy()
    offspring_1[:chosen_idx] = offspring_2[:chosen_idx]
    offspring_2[:chosen_idx] = temp

    # swap right side
    temp = offspring_1[chosen_idx:].copy()
    offspring_1[chosen_idx:] = offspring_2[chosen_idx:]
    offspring_2[chosen_idx:] = temp

    return [offspring_1, offspring_2]
    
def get_mating_func(crossover_mode:str = "uniform"):
    if crossover_mode == "uniform":
        crossover_func = uniform_crossover
    elif crossover_mode == "onepoint":
        crossover_func = one_point_crossover
    else:
        raise ValueError(f"Found no crossover function named \'{crossover_mode}\'")
    return crossover_func
    
def mating_pool(population:np.array, mating_size:int = 4, crossover_mode:str = "uniform"):
    population_ = population.copy()

    old_size = population_.shape[0]
    expected_size = old_size * mating_size
    mating_func = get_mating_func(crossover_mode)
    offsprings = []
    while old_size + len(offsprings) < expected_size:
        for i in range(0,old_size-1,2):
            while old_size + len(offsprings) < expected_size:
                parent_1 = population_[i]
                parent_2 = population_[i+1]
                offspring = mating_func(parent_1,parent_2)
                offsprings += offspring

    return np.array(offsprings)

def merge_population(population_1:np.array, population_2:np.array):
    population = np.vstack((population_1, population_2 ))
    return population

if __name__ =="__main__":
    
    n_iters_no_improve = 0
    population = initialize_population(pop_size = POP_SIZE, n_bits = N_BITS)
    best_fitness = calc_fitness_population(population, fitness_mode = FITNESS_MODE)

    while n_iters_no_improve < 10:
        print(population)

        # Create new offsprigns
        new_offsprings = mating_pool(population, mating_size = 4, crossover_mode =  CROSSOVER_MODE)

        # Merge new offsprings with new population
        population = merge_population(population, new_offsprings)

        # Tournament selection
        population = tournament_selection(population, tournament_size = 4)

        #np.random.shuffle(population)    
        current_fitness = calc_fitness_population(population, fitness_mode = FITNESS_MODE)
        if current_fitness <= best_fitness:
            n_iters_no_improve += 1
        else:
            best_fitness = current_fitness
        print("Current fitness: ", current_fitness)
