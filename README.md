<p align="center">
  <img src="https://iili.io/JgM817S.md.png" width="250" height="250">
</p>

# DFly

DFly is a comprehensive solution designed to meet the requirements of EASA's U-space regulation, facilitating the management of UAV operations within designated airspaces. Our primary focus is to streamline the Flight Authorisation Service, ensuring secure and efficient UAV operations.

## Introduction
DFly leverages cutting-edge technologies including Merkle trees for operation categorization and Zero-Knowledge Proofs (ZKP) for operation verification, integrated with blockchain technology via Brownie for secure and transparent transactions.

## Features
- **Flight Authorization**: Partially implemented, it allows for secure UAV flight operations based on verified and approved UAV and operator credentials.
- **Merkle Tree Integration**: Ensures that only approved aircraft and operators can request flight authorizations.
- **Zero-Knowledge Proofs**: Enhances privacy and security by enabling operators to prove their authorization without revealing sensitive information.
- **Blockchain Interaction**: Utilizes Brownie to interact with blockchain technology, ensuring immutable record-keeping and transaction security.

## Installation
To get started with DFly, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/FredericoBaptista/Dfly/tree/main
2. Installing Circom
   - Install dependencies:
      - Node.js:
         ```bash
         sudo apt update
         sudo apt install nodejs
      
      - Rust:
         ```bash
         curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh

      - snarkjs:
         ```bash
         npm install -g snarkjs
   
   - Clone the circom repository:
      ```bash
      git clone https://github.com/iden3/circom.git
   
   - Enter the circom directory and use the cargo build to compile:
      ```bash
      cargo build --release
   - Check if installation is proper by typing:
      ```bash
      circom --help  
3. Install all other needed dependencies:
   ```bash
   pip install -r requirements.txt
## Usage
<p align="center">
<img src="https://pasteboard.co/rz8HxA4Um1mb.png" alt="JrdKQov.md.png" border="0"></a>
</p>


## Contact

