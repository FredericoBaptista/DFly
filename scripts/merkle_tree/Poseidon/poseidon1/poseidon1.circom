pragma circom 2.0.0;

include "../node_modules/circomlib/circuits/poseidon.circom";
include "../node_modules/circomlib/circuits/bitify.circom";
include "../node_modules/circomlib/circuits/comparators.circom";

template poseidon1() {
    signal input in;
    signal output out;

    component hasher;

        hasher = Poseidon(1);
        hasher.inputs[0] <== in;
        out <== hasher.out;

}

component main = poseidon1();