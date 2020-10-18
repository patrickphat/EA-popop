import numpy as np
from .fitness import get_fitness_func
from utils.fitness import scarcity


def get_individual_str(individual: np.array):
    """Get string numpy array

    Args:
        individual (np.array): 1D numpy array
    Return:
        individual as str. E.g: "1001"
    """
    ind_str = ""
    for i in individual:
        ind_str += str(i)
    return ind_str


def get_best_individual(
    population: np.array,
    group: np.array,
    fitness_mode: str = "onemax",
    use_scarcity: bool = True,
):

    # Get best individual based on fitness
    fitnesses = []
    fitness_func = get_fitness_func(fitness_mode)
    for individual in group:
        fitnesses.append(fitness_func(individual))

    # If not calculate scarcity, return immediately
    if not use_scarcity:
        best_fitness = max(fitnesses)

        best_idxs = np.where(np.array(fitnesses) == best_fitness)[0]

        chosen_best_idx = np.random.choice(best_idxs)
        try:
            best_indi = group[chosen_best_idx][:]
        except:
            import ipdb

            ipdb.set_trace()
        return best_indi

    # Maintain scarce individual
    best_fitness = max(fitnesses)
    best_idxs = np.where(np.array(fitnesses) == best_fitness)[0]
    best_fitness_group = group[best_idxs]

    scarcities = []
    for individual in best_fitness_group:
        scarcities.append(scarcity(population, individual))

    best_scarcity = max(scarcities)

    best_idx = np.where(np.array(scarcities) == best_scarcity)[0]
    chosen_best_idx = np.random.choice(best_idx)

    best_indi = best_fitness_group[chosen_best_idx][:]
    return best_indi


def tournament_selection(
    population: np.array, tournament_size: int = 4, fitness_mode: str = "onemax"
):
    pop_size = population.shape[0]
    population_ = population.copy()
    # np.random.shuffle(population_)
    n_groups = int(np.ceil(pop_size / tournament_size))
    reserved_individual = []
    groups = np.array_split(population_, n_groups)
    for group in groups:
        # import ipdb

        # ipdb.set_trace()
        best_indi = get_best_individual(population, group, fitness_mode)
        reserved_individual.append(best_indi)

    return np.array(reserved_individual)