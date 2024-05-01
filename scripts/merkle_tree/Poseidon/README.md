# Poseidon

## Description
Poseidon is a package that interfaces with Circom to compute the results of the Poseidon hash function with the same results as in the Circom library. The python implementation of the poseidon hash does not have the same parameters as in Circom, hence the need of this local package. This use of the hash function will be updated in future work.

## Installation

### Prerequisites
- **[Circom](https://github.com/iden3/circom):** Poseidon requires Circom to compile circuits. Follow the installation instructions on the Circom GitHub page.

### Installing Poseidon
To install locally install Poseidon, ensure you have Python >=3.7 and run the following command, while being on the current directory:
```bash
pip install .
