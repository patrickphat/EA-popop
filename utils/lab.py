from utils.fitness import calc_fitness_population
from utils.operation import initialize_population, merge_population
from utils.mating import mating_pool
from utils.selection import tournament_selection
import numpy as np
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def popop(
    pop_size: int,
    n_bits: int,
    mate_n_select_scale: int,
    fitness_mode: str,
    crossover_mode: str,
    print_log: bool = False,
):
    n_iters_no_change = 0
    n_evaluations = 0
    population = initialize_population(pop_size=pop_size, n_bits=n_bits)
    last_fitness = calc_fitness_population(population, fitness_mode=fitness_mode)

    while n_iters_no_change < 10:
        # Create new offsprigns
        new_offsprings = mating_pool(
            population, mating_size=mate_n_select_scale, crossover_mode=crossover_mode,
        )

        # Merge new offsprings with new population
        population = merge_population(population, new_offsprings)

        # Calculate current fitness
        current_fitness = calc_fitness_population(population, fitness_mode=fitness_mode)
        if print_log:
            logger.info(f"Current fitness: {current_fitness}")

        # Tournament selection
        population = tournament_selection(
            population, tournament_size=mate_n_select_scale, fitness_mode=fitness_mode
        )

        

        if current_fitness == last_fitness:
            n_iters_no_change += 1
        else:
            n_iters_no_change = 0
        last_fitness = current_fitness
        n_evaluations += 1

    result_dict = {
        "optima": population[0],
        "current_fitness": current_fitness,
        "n_evaluations": n_evaluations,
        "is_success": current_fitness == n_bits,
    }

    return result_dict


def popop_n_times_stop_if_fail(
    pop_size: int,
    n_bits: int,
    mate_n_select_scale: int,
    fitness_mode: str,
    crossover_mode: str,
    n_times: int = 10,
):
    n_evaluations_list = []

    for _ in range(n_times):
        result_dict = popop(
            pop_size=pop_size,
            n_bits=n_bits,
            mate_n_select_scale=mate_n_select_scale,
            fitness_mode=fitness_mode,
            crossover_mode=crossover_mode,
        )
        if result_dict["is_success"] == False:
            result_dict = {"mean_n_evaluations": None, "is_success_all": False}
            return result_dict
        else:
            n_evaluations_list.append(result_dict["n_evaluations"])

    result_dict = {
        "mean_n_evaluations": np.mean(n_evaluations_list),
        "is_success_all": True,
    }
    return result_dict


def find_MRPS_popop(
    n_bits: int,
    mate_n_select_scale: int,
    fitness_mode: str,
    crossover_mode: str,
    n_checks: int = 10,
    thresh: int = 2 ** 13,
):

    # Start pop size
    pivot_size = 4
    is_upper_bound_found = False

    # Step 1: Find upperbound
    while pivot_size <= thresh:
        logger.info(f"[UpperBoundSearch]:: Try running with pop_size = {pivot_size}...")
        result_dict = popop_n_times_stop_if_fail(
            pop_size=pivot_size,
            n_bits=n_bits,
            mate_n_select_scale=mate_n_select_scale,
            fitness_mode=fitness_mode,
            crossover_mode=crossover_mode,
        )

        if result_dict["is_success_all"]:
            is_upper_bound_found = True
            logger.info(f"[UpperBoundSearch]:: Found upperbound={pivot_size}")
            break

        pivot_size *= 2
    if not is_upper_bound_found:
        result_dict = {
            "MRPS": None,
            "mean_n_evaluations": None,
        }
        return result_dict

    # Step 2: Find MRPS using found upperbound
    upper_bound = pivot_size
    lower_bound = int(upper_bound / 2)
    latest_popop_result_dict = result_dict
    while upper_bound - lower_bound > 1:
        logger.info(
            f"[MRPSSearch]:: Finding MRPS with upperbound={upper_bound} & lowerbound={lower_bound}"
        )
        pivot_size = int((upper_bound + lower_bound) / 2)
        popop_result_dict = popop_n_times_stop_if_fail(
            pop_size=pivot_size,
            n_bits=n_bits,
            mate_n_select_scale=mate_n_select_scale,
            fitness_mode=fitness_mode,
            crossover_mode=crossover_mode,
        )

        if popop_result_dict["is_success_all"]:
            upper_bound = pivot_size
            latest_popop_result_dict = popop_result_dict
        else:
            lower_bound = pivot_size

    result_dict = {
        "MRPS": pivot_size,
        "mean_n_evaluations": latest_popop_result_dict["mean_n_evaluations"],
    }
    return result_dict
