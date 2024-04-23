//SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.9;

abstract contract Approvable {
    // Defines an approver
    struct Approver {
        string name;
        address id;
    }

    address public creator;
    mapping(address => bool) isapprover;
    Approver[] private listApprovers;
    mapping(address => Approver) approverMap;

    constructor(address owner, string memory name) {
        // Creates owner and assigns owner directly into the approver role
        creator = owner;
        createApprover(name, owner);
        isapprover[creator] = true;
    }

    modifier creatorOnly() {
        require(msg.sender == creator);
        _;
    }

    modifier approversOnly() {
        require(isapprover[msg.sender] == true);
        _;
    }

    function createApprover(
        string memory _name,
        address _address
    ) public creatorOnly {
        // Creates approver
        Approver storage approv = approverMap[_address];
        approv.name = _name; // The list of approvers is public
        approv.id = _address;
        isapprover[_address] = true;
        listApprovers.push(approv);
    }

    function deleteApprover(
        address _address,
        uint256 number
    ) public creatorOnly {
        isapprover[_address] = false;
        delete listApprovers[number];
    }
}
