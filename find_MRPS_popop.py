import numpy as np
import random
from typing import List
from pprint import pprint
import yaml

# from utils.fitness import calc_fitness_population
# from utils.operation import initialize_population, merge_population
# from utils.mating import mating_pool
# from utils.selection import  tournament_selection
from utils.lab import popop, popop_n_times_stop_if_fail, find_MRPS_popop
import numpy as np
import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument(
    "-c",
    "--config",
    help="path to train config file",
    default="configs/default_config.yaml",
)
args = parser.parse_args()

# with open(args.config, "r") as f:
#     CFG = yaml.load(f, Loader=yaml.FullLoader)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CFGs = {
    "n_bits": 20,
    "fitness_mode": "trap5",
    "mate_n_select_scale": 4,
    "crossover_mode": "uniform",
    "n_bisections": 10,
    "log_path": "logs/experiment_trap5_ux.log",
}

BASE_RANDOM_SEED = 17520880
np.random.seed(BASE_RANDOM_SEED)

# def find_upper_bound(pop_size:int, n_bits:int, cross_n_mating_size:int , fitness_mode:str, crossover_mode:str):

if __name__ == "__main__":
    with open(CFGs["log_path"], "a") as fp:
        fp.write(f"[Experiment] CFGs: {CFGs}\n")

    for i in range(CFGs["n_bisections"]):
        result_dict = find_MRPS_popop(
            n_bits=CFGs["n_bits"],
            mate_n_select_scale=CFGs["mate_n_select_scale"],
            fitness_mode=CFGs["fitness_mode"],
            crossover_mode=CFGs["crossover_mode"],
        )
        with open(CFGs["log_path"], "a") as fp:
            idx_str = str(i + 1).zfill(2)
            fp.write(f"Bisection #{idx_str}: {result_dict}\n")

        logger.info(f"[MRPSSearch] Found MRPS={result_dict['MRPS']}")
