//SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.9;

import "./Approvable.sol";

contract MerkleTree is Approvable {

    constructor() Approvable(msg.sender, "Owner") {}

    event NewTree(string indexed _name_of_tree, uint depth);
    event NewLeaf(string indexed _name_of_tree, string leaf, string root);
    event DeleteLeaf(string indexed _name_of_tree, string leaf, string root);
    event UpdateTree(string indexed _name_of_tree, string indexed root);

    // Should I define the tree as a structure containing a list of leafs?
    // Asssuming there is a pre agreement on how to add leafs to the tree; just the root will be presented


    function createTree(string memory _name_of_tree, uint depth) public approversOnly {
        emit NewTree(_name_of_tree, depth);
    }

    function addLeaf(string memory name_of_tree, string memory leaf, string memory root) public approversOnly {
        emit NewLeaf(name_of_tree, leaf, root);
    }

    function deleteLeaf(string memory name_of_tree, string memory leaf, string memory root) public approversOnly {
        emit DeleteLeaf(name_of_tree, leaf,root);
    }

    function updateTree(string memory name_of_tree, string memory root) public approversOnly {
        emit UpdateTree(name_of_tree, root);
    }
}


