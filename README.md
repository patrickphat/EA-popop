<div align="center">

# POPOP Evolutionary Algorithm Implementation

</div>

## ✨ Introduction

🚀 This is the implementation of POPOP Evolutionary Algorithm, including:

1. POPOP algorithm with different settings:

- Problem size
- Tournament selection with size
- Mutation modes: Uniform and Onepoint
- Fitness modes: Onemax and Trap5
- Uniformly initialized population at every bits

2. Searching and analyzing Minimally-Requirement Population Size (MRPS) with n bisections

## ⚙️ Installation

1. Clone this repo to your local machine:

```bash
git clone git@github.com:patrickphat/EA-popop.git
cd EA-popop/
```

2. (Optional) Create an fresh new python 3.8 environment. E.g, with conda:

```bash
conda create -n popop python=3.8
conda activate popop
```

3. Install all the requirements:

```bash
pip install requirements.txt
```

## 📖 Usage

**TASK 1:** Run POPOP algorithm

```bat
python run_popop.py
```

Configs:

- `n_bits` (int): Problem size (number of bits)
- `pop_size` (int): Number of population
- `fitness_mode` (str): Fitness evaluation of population, `onemax` or `trap5`
- `mate_n_select_scale` (int): Group size in tournament selection
- `crossover_mode` (str): Mutation mode, `uniform` or `onepoint`

**TASK 2:** Find Minimally-Requirement Population Size (MRPS)

```bat
python find_MRPS_popop.py
```

Configs:

- `n_bits` (int): Problem size (number of bits)
- `fitness_mode` (str): Fitness evaluation of population
- `mate_n_select_scale` (int): Group size in tournament selection
- `crossover_mode` (str): `uniform` and `onepoint`
- `n_bisections` (int): Number of bisections performed. Default is `10`
- `log_path` (str): Path to log file. Recommended to use `.log` extensions

Please edit the config accordingly in `CFGs` variable of each file to your liking.
