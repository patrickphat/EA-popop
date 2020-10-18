import numpy as np


def uniform_crossover(
    individual_1: np.array, individual_2: np.array, thresh: int = 0.5
):
    offspring_1 = individual_1.copy()
    offspring_2 = individual_2.copy()
    for i, _ in enumerate(offspring_1):
        ran_num = np.random.uniform()
        if ran_num > thresh:
            # swap 2 bits at i-th position
            temp_bit = offspring_1[i]
            offspring_1[i] = offspring_2[i]
            offspring_2[i] = temp_bit
        else:
            continue

    return [offspring_1, offspring_2]


def one_point_crossover(
    individual_1: np.array, individual_2: np.array, thresh: int = 0.5
):
    offspring_1 = individual_1.copy()
    offspring_2 = individual_2.copy()
    ran_num = np.random.uniform()
    array_size = individual_1.shape[0]
    chosen_idx = int(np.ceil(array_size * ran_num))

    # swap left side
    temp = offspring_1[:chosen_idx].copy()
    offspring_1[:chosen_idx] = offspring_2[:chosen_idx]
    offspring_2[:chosen_idx] = temp

    # swap right side
    temp = offspring_1[chosen_idx:].copy()
    offspring_1[chosen_idx:] = offspring_2[chosen_idx:]
    offspring_2[chosen_idx:] = temp

    return [offspring_1, offspring_2]


def get_mating_func(crossover_mode: str = "uniform"):
    if crossover_mode == "uniform":
        crossover_func = uniform_crossover
    elif crossover_mode == "onepoint":
        crossover_func = one_point_crossover
    else:
        raise ValueError(f"Found no crossover function named '{crossover_mode}'")
    return crossover_func


def mating_pool(
    population: np.array, mating_size: int = 4, crossover_mode: str = "uniform"
):
    population_ = population.copy()

    old_size = population_.shape[0]
    expected_size = old_size * mating_size
    mating_func = get_mating_func(crossover_mode)
    offsprings = []
    while old_size + len(offsprings) < expected_size:
        for i in range(0, old_size - 1, 2):
            while old_size + len(offsprings) < expected_size:
                parent_1 = population_[i]
                parent_2 = population_[i + 1]
                offspring = mating_func(parent_1, parent_2)
                offsprings += offspring

    return np.array(offsprings)