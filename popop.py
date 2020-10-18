import numpy as np
from utils.lab import popop
import numpy as np
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CFGs = {
    "n_bits": 10,
    "pop_size": 20,
    "fitness_mode": "onemax",
    "mate_n_select_scale": 4,
    "crossover_mode": "uniform",
}

BASE_RANDOM_SEED = 17520880
np.random.seed(BASE_RANDOM_SEED)

if __name__ == "__main__":

    result_dict = popop(
        n_bits=CFGs["n_bits"],
        pop_size=CFGs["pop_size"],
        mate_n_select_scale=CFGs["mate_n_select_scale"],
        fitness_mode=CFGs["fitness_mode"],
        crossover_mode=CFGs["crossover_mode"],
        print_log=True,
    )
    logger.info(f"Result: {result_dict}")
