import numpy as np


def one_max(individual_bits: np.array):
    return np.sum(individual_bits)


def trap_n(individual_bits: np.array, n_traps: int = 5):
    num_bits = individual_bits.shape[0]
    sum_all_block = 0

    if num_bits % n_traps != 0:
        raise ValueError(
            f"The input bits should be the multiple of {n_traps}, found {num_bits}"
        )
    else:
        for i in range(0, num_bits, n_traps):
            sum_block = np.sum(individual_bits[i : i + n_traps])
            if sum_block == n_traps:
                sum_all_block += n_traps
            else:
                sum_all_block += n_traps - 1 - sum_block
    return sum_all_block


def scarcity(population: np.array, individual_bits: np.array, sampling_rate: int = 16):
    pop_size = population.shape[0]
    n_bits = population.shape[1]
    sampling_rate = min(sampling_rate, pop_size)
    chosen_idxs = []

    # Sampling a small set from population
    while len(chosen_idxs) < sampling_rate:
        rand_int = np.random.randint(pop_size)
        if rand_int not in chosen_idxs:
            chosen_idxs.append(rand_int)

    # Retrieve a subset of population
    sample_population = population[chosen_idxs]
    individual_bits = individual_bits.reshape(1, -1)

    # Perform element-wise product and take sum
    sum_element_wise_product = (individual_bits * sample_population).sum()

    # Calculate scarcity score
    score = n_bits - sum_element_wise_product / sampling_rate

    return score


def get_fitness_func(fitness_mode: str = "onemax"):
    if fitness_mode == "onemax":
        return one_max
    elif fitness_mode == "trap5":
        return trap_n
    else:
        raise ValueError(f"This fitness function {fitness_mode} does not support")


def calc_fitness_population(population: np.array, fitness_mode: str = "onemax"):
    fitness_func = get_fitness_func(fitness_mode)
    fitnesses = []
    for individual in population:
        fitnesses.append(fitness_func(individual))
    return np.mean(fitnesses)