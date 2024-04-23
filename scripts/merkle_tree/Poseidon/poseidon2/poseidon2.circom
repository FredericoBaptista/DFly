pragma circom 2.0.0;

include "../node_modules/circomlib/circuits/poseidon.circom";
include "../node_modules/circomlib/circuits/bitify.circom";
include "../node_modules/circomlib/circuits/comparators.circom";

template poseidon2() {
    signal input left;
    signal input right;
    signal output out;

    component hasher;

        hasher = Poseidon(2);
        hasher.inputs[0] <== left;
        hasher.inputs[1] <== right;
        out <== hasher.out;

}

component main = poseidon2();