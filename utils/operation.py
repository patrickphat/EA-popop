import numpy as np

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

def merge_population(population_1:np.array, population_2:np.array):
    population = np.vstack((population_1, population_2 ))
    return population
