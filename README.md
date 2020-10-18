<div align="center">

# POPOP Evolutionary Algorithm Implementation

</div>

## ✨ Introduction

🚀 This is the implementation of POPOP Evolutionary Algorithm, including:

1. POPOP algorithm with different settings:

- Problem size `n_bits` (int)
- Mating (Mutation) mode: `uniform` (UX) & `onepoint` (1X)
- Fitness mode: `onemax` & `trap5`
- Tournament size with abitrary numbers
- Uniformly initialized population at every bits

2. Searching and analyzing Minimally-Requirement Population Size (MRPS) with n bisections

## ⚙️ Installation

1. Clone this repo to your local machine:

```bash
git clone git@github.com:patrickphat/popop-evolutionary-algorithm.git
cd popop-evolutionary-algorithm
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

## Usage

Task 1: Run POPOP algorithm

```bat
python run_popop.py
```

Task 2: Find Minimally-Requirement Population Size (MRPS)

```bat
python find_MRPS_popop.py
```

Please edit the config accordingly in `CFGs` variable of each file to your liking.
