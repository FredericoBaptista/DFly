#!/bin/bash

# First argument is the directory path
DIR=$1

node InclusionProof_js/generate_witness.js InclusionProof_js/InclusionProof.wasm InclusionProof_js/input.json InclusionProof_js/witness.wtns
snarkjs groth16 prove InclusionProof_0001.zkey InclusionProof_js/witness.wtns proof.json public.json
snarkjs generatecall