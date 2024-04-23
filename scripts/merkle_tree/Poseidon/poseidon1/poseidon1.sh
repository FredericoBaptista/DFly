#!/bin/bash

# First argument is the directory path
DIR=$1

node $DIR/scripts/merkle_tree/Poseidon/poseidon1/poseidon1_js/generate_witness.js $DIR/scripts/merkle_tree/Poseidon/poseidon1/poseidon1_js/poseidon1.wasm $DIR/scripts/merkle_tree/Poseidon/poseidon1/poseidon1_js/input.json $DIR/scripts/merkle_tree/Poseidon/poseidon1/poseidon1_js/witness.wtns
snarkjs groth16 prove $DIR/scripts/merkle_tree/Poseidon/poseidon1/poseidon1_0001.zkey $DIR/scripts/merkle_tree/Poseidon/poseidon1/poseidon1_js/witness.wtns $DIR/scripts/merkle_tree/Poseidon/poseidon1/proof.json $DIR/scripts/merkle_tree/Poseidon/poseidon1/public.json
