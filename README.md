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
   git clone https://github.com/FredericoBaptista/Dfly
2. Installing Circom
   - Install dependencies:
      - Node.js:
         ```bash
         sudo apt update
         sudo apt install nodejs
      
      - Rust:
         ```
         curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
      
      Choose the default instalation by pressing enter.

      - snarkjs:
         ```
         sudo npm install -g snarkjs@0.6.11
   
   - Clone the circom repository:
      ```bash
      git clone https://github.com/iden3/circom.git
   
   - Enter the circom directory and use the cargo build to compile:
      ```bash
      cd circom
      cargo build --release
   - Install circom
      ```bash
      cargo install --path circom
   - Add circom directory to PATH:
      - Open bashrc:
         ```
         nano ~/.bashrc
      - Add to PATH, by adding to bashrc file with:
         ```
         export PATH="$PATH:/home/myusername/.local/bin"
   - Check if installation is proper by typing:
      ```bash
      circom --help  
3. Install all other needed dependencies:
   ```bash
   cd ..
   pip install -r requirements.txt
4. Configure .env file.
   - It's necessary to have a .env file with your wallet credentials inserted, so that you can run the project. The .env file looks like the following:

      ```
      export PRIVATE_KEY = 
      export WEB3_INFURA_PROJECT_ID = 
      export ETHERSCAN_TOKEN =
      ```

   - Be sure to start an infura project first at: https://www.infura.io/

5. Install circomlib
   ```
   npm install circomlib
   ```

6. Compile the circom circuit:
   
   To compile the circuits it's important to thouroughly follow these steps:
   
   - Go to the circuits directory:
      ```bash
      cd circuits
   - Run the circom_script.sh:
      ```bash
      ./circom_script.sh
   - The name of the circuit is InclusionProof
   - Choose option 1 that compiles the circuit
   - Open the file scripts/merkle_tree/SNMerkleTree.py and create a tree and add a leaf to that tree (by adding the following lines to the main):
      ```
      initialize_tree(3, "Operator")
      insert_leaf("operator_number", nonce , "Operator")
      ```
   - Run brownie on cmd line
      ```
      brownie run merkle_tree/SNMerkleTree.py --network sepolia
      ```
   Note that for this step to work, the contract MerkleTree.sol has to be already deployed.

   - Try to get the proof for the leaf you previously inserted by running:
      ```
      get_proof("operator_number", nonce , "Operator")
      ```
      This will give an error but it will create an input.json file under the InclusionProof_js folder. With this folder created it's now possible to run the rest of the circom_script.sh
   
   - Run circom_script.sh choosing the other options.


## Contracts Deployment
This is an essential step to be able to use DFly. Although some test contracts are already deployed in the Sepolia test net, you need to deploy your own contracts.
In order to do this a deploy.py script is available under the scripts folder.

1. Run brownie:
   ```
   brownie run deploy.py --network sepolia
   ```
The example is done for sepolia network, but you can change your network under brownie definitions. For more information go to [Brownie Documentation](https://eth-brownie.readthedocs.io/en/stable/toctree.html)
## Usage
<p align="center">
<img src="https://imgtr.ee/images/2024/05/04/419523a45ae2d3f8e4fe5dcf6d8b3d2a.png" alt="419523a45ae2d3f8e4fe5dcf6d8b3d2a.png" border="0" />
</p>
There's essentially, two phases of the usage of DFly, as it can be seen above. The first is the approval of the UAS and operator into the Merkle trees. The second is the actual usage of the smart contracts, that effectivelly allow the operator to request a flight authorisation.

### Approval in Merkle Trees

Using brownie it's possible to insert the UAS and UAS operator numbers into the merkle trees. For that, it is necessary to understand the structure of the merkle tree management. The following figure explains just that:

<p align="center">
<img src="https://imgtr.ee/images/2024/05/04/a59b498dfbf4d2bd7feecca7ad87e873.png" alt="a59b498dfbf4d2bd7feecca7ad87e873.png" border="0" />
</p>

To start properly the usage, you should initialize all the necessary trees with the required depth for the usage you want. In the following example, we choose all the merkle trees of depth 3. The following lines have to be included in SNMerkleTree.py:
   ```
   initialize_tree(3, "Operator")
   initialize_tree(3, "Open")
   initialize_tree(3, "Specific")
   initialize_tree(3, "Certified")
   initialize_tree(3, "SpecialOps")
   initialize_tree(3, "BVLOS")
   ```
To insert the operator and UAS number, following the logic of the previous figure, you can insert the UAS number and the operator number on the respective trees. In the following example, we choose a UAS legalized to fly on the following modes:

| Operation Mode | Flight Category | Flight Type  |
| -------------- | --------------- | ------------ | 
|    Specific    |      BVLOS      |  SpecialOps  |


To do this the following lines of code need to be included in SNMerkleTree.py, (change operator_number, nonce and uas_serial_number to your specific case). **The nonce has to be an integer** :

   ```
   insert_leaf("operator_number", nonce , "Operator")
   insert_leaf("uas_serial_number, nonce, "Specific")
   insert_leaf("uas_serial_number, nonce, "BVLOS")
   insert_leaf("uas_serial_number, nonce, "SpecialOps")
   ```

Once all this setup is done in the SNMerkleTree.py it's now possible to run SNMerkleTree, once again, using brownie:
```
brownie run merkle_tree/SNMerkleTree.py --network sepolia
```

### Flight Request

Once the necessary information from the UAS operator and UAS are added, it's now possible to request a flight. To do this, there's a small user interface that helps speed up the process of performing the request.

You just have to run this ui by running in you directory:
```
brownie run merkle_tree/user_interface/FLIGHTREQ_GUI.py --network sepolia
```

The UI will look like this:

<p align="left">
<img src="https://imgtr.ee/images/2024/05/04/f306813c00cb725949ee41f8861ff276.png" alt="f306813c00cb725949ee41f8861ff276.png" border="0" />
<p>

You just have to fill in all the data and click "Submit". 


## Contact

Please contact me at: fredbaptista8@gmail.com
