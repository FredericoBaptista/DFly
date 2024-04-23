#!/bin/bash

set -e
trap 'echo "A command failed. Exiting..." >&2' ERR

read -p "Enter the name of the circuit: " circuit

echo "Choose an option:"
echo "0. Do all"
echo "1. Compile a circuit"
echo "2. Compute the witness"
echo "3. Powers of Tau phase 1"
echo "4. Powers of Tau phase 2"
echo "5. Generate Proof"
echo "6. Verify Proof"
echo "7. Generate Smart Contract Inputs"
echo "8. Generate Smart Contract"

read -p "Enter your choice (0-8): " option

if [[ $option -eq 0 ]]; then
    circom ${circuit}.circom --r1cs --wasm --sym --c
    wait
    read -p "Is the input.json already created? (Y/N): " isInputCreated
    if [[ $isInputCreated == "Y" || $isInputCreated == "y" ]]; then
        node ${circuit}_js/generate_witness.js ${circuit}_js/${circuit}.wasm ${circuit}_js/input.json ${circuit}_js/witness.wtns
        wait
        snarkjs powersoftau new bn128 12 pot12_0000.ptau -v
        snarkjs powersoftau contribute pot12_0000.ptau pot12_0001.ptau --name="First contribution" -v
        snarkjs powersoftau prepare phase2 pot12_0001.ptau pot12_final.ptau -v
        snarkjs groth16 setup ${circuit}.r1cs pot12_final.ptau ${circuit}_0000.zkey
        snarkjs zkey contribute ${circuit}_0000.zkey ${circuit}_0001.zkey --name="1st Contributor Name" -v
        snarkjs zkey export verificationkey ${circuit}_0001.zkey verification_key.json
        snarkjs groth16 prove ${circuit}_0001.zkey ${circuit}_js/witness.wtns proof.json public.json
        snarkjs groth16 verify verification_key.json public.json proof.json
        snarkjs generatecall
        snarkjs zkey export solidityverifier ${circuit}_0001.zkey verifier.sol
    else
        echo "Please create input.json first."
    fi

elif [[ $option -eq 1 ]]; then
    circom ${circuit}.circom --r1cs --wasm --sym --c

elif [[ $option -eq 2 ]]; then
    node ${circuit}_js/generate_witness.js ${circuit}_js/${circuit}.wasm ${circuit}_js/input.json ${circuit}_js/witness.wtns

elif [[ $option -eq 3 ]]; then
    snarkjs powersoftau new bn128 12 pot12_0000.ptau -v
    snarkjs powersoftau contribute pot12_0000.ptau pot12_0001.ptau --name="First contribution" -v

elif [[ $option -eq 4 ]]; then
    snarkjs powersoftau prepare phase2 pot12_0001.ptau pot12_final.ptau -v
    snarkjs groth16 setup ${circuit}.r1cs pot12_final.ptau ${circuit}_0000.zkey
    snarkjs zkey contribute ${circuit}_0000.zkey ${circuit}_0001.zkey --name="1st Contributor Name" -v
    snarkjs zkey export verificationkey ${circuit}_0001.zkey verification_key.json

elif [[ $option -eq 5 ]]; then
    snarkjs groth16 prove ${circuit}_0001.zkey ${circuit}_js/witness.wtns proof.json public.json

elif [[ $option -eq 6 ]]; then
    snarkjs groth16 verify verification_key.json public.json proof.json

elif [[ $option -eq 7 ]]; then
    snarkjs generatecall

elif [[ $option -eq 8 ]]; then
    snarkjs zkey export solidityverifier ${circuit}_0001.zkey verifier.sol

else
    echo "Invalid choice"
fi
