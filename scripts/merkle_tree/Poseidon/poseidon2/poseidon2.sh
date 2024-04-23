#!/bin/bash

# First argument is the directory path
DIR=$1

node $DIR/poseidon2/poseidon2_js/generate_witness.js $DIR/poseidon2/poseidon2_js/poseidon2.wasm $DIR/poseidon2/poseidon2_js/input.json $DIR/poseidon2/poseidon2_js/witness.wtns
snarkjs groth16 prove $DIR/poseidon2/poseidon2_0001.zkey $DIR/poseidon2/poseidon2_js/witness.wtns $DIR/poseidon2/proof.json $DIR/poseidon2/public.json
