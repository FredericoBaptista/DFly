pragma circom 2.0.0;

include "../../node_modules/circomlib/circuits/poseidon.circom";
include "../../node_modules/circomlib/circuits/bitify.circom";
include "../../node_modules/circomlib/circuits/comparators.circom";

// if s == 0 returns [in[1], in[0]]
// if s == 1 returns [in[0], in[1]]
template PositionSwitcher() {
    signal input in[2];
    signal input s;
    signal output out[2];

    s * (1 - s) === 0;
    out[0] <== (in[0] - in[1])*s + in[1];
    out[1] <== (in[1] - in[0])*s + in[0];
}


// Verifies that merkle path is correct for a given merkle root and leaf
// pathIndices input is an array of 0/1 selectors telling whether given 
// pathElement is on the left or right side of merkle path
template InclusionProof(levels) {
    signal input leaf;
    signal input nonce;
    signal input root;
    signal input pathElements[levels];
    signal input pathIndices[levels];
    signal output out;


    component selectors[levels];
    component hashers[levels];
    component hashleaf;

    signal computedPath[levels];
    signal hashedleaf;
    
    hashleaf = Poseidon(2);
    hashleaf.inputs[0] <== leaf; //user inputs serial number
    hashleaf.inputs[1] <== nonce;
    hashedleaf <== hashleaf.out;


    for (var i = 0; i < levels; i++) {
        selectors[i] = PositionSwitcher();
        selectors[i].in[0] <== i == 0 ? hashedleaf : computedPath[i - 1];
        selectors[i].in[1] <== pathElements[i];
        selectors[i].s <== pathIndices[i];

        hashers[i] = Poseidon(2);
        hashers[i].inputs[0] <== selectors[i].out[0];
        hashers[i].inputs[1] <== selectors[i].out[1];
        computedPath[i] <== hashers[i].out;
        
    }

    out <== computedPath[levels - 1];
    (root - computedPath[levels - 1]) === 0;
    //out <== root;

}

component main = InclusionProof(10);