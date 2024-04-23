#!/bin/bash

# First argument is the directory path
DIR=$1

start1=`date +%s%N`

node InclusionProof_js/generate_witness.js InclusionProof_js/InclusionProof.wasm InclusionProof_js/input.json InclusionProof_js/witness.wtns

end1=`date +%s%N`
echo Witness generation time was `expr $end1 - $start1` nanoseconds.

start2=`date +%s%N`

snarkjs groth16 prove InclusionProof_0001.zkey InclusionProof_js/witness.wtns proof.json public.json

end2=`date +%s%N`
echo Proof generation time was `expr $end2 - $start2` nanoseconds.

snarkjs generatecall