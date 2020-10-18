import numpy as np
from utils.lab import find_MRPS_popop
import numpy as np
import logging

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
