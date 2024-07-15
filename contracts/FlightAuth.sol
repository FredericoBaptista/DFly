//SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.9;

import "./Approvable.sol";
import "./verifier.sol"; // update verifier after

contract FlightAuth is Approvable, Verifier {
    // Defines Aircraft data
    struct FlightRequest {
        string _SN; 
        // Operational Mode variables
        uint _op_mode;
        ZKProof proof_op_mode;
        // Flight Type variables
        bool _flight_type;
        ZKProof proof_flight_type;
        // Flight Category variables
        bool _flight_cat;
        ZKProof proof_flight_cat;
        // Operator Number variables
        uint256 _operator_num;
        ZKProof proof_operator_num;
        uint256 endurance;
        string trajectory_4D; //hash from ipfs
        bool approved;
    }

    struct ZKProof {
        uint256[2] _part1;
        uint256[2][2] _part2;
        uint256[2] _part3;
        uint256[2] _part4;
    }

    struct FlightInfo {
        uint id_tech;
        uint ex_connec_meth;
        uint emergency_proc;
    }


    // Defines the new user event
    // This event is "displayed" each time a new flight request is done
    event NewFlightRequest(
        uint createdAt,
        uint256 indexed serial_number,
        uint op_mode,
        bool flight_type,
        bool flight_cat,
        uint id_tech,
        uint ex_connect_meth,
        uint256 endurance,
        uint emergency_proc,
        uint256 indexed operator_num,
        bool indexed approved
    );

        event NewPrivateFlightRequest(
        uint createdAt,
        uint op_mode,
        bool flight_type,
        bool flight_cat,
        bool indexed approved
    );

    uint256[1] root_operator;
    uint256[1] root_open;
    uint256[1] root_specific;
    uint256[1] root_cerified;
    uint256[1] private root_specialops;
    uint256[1] root_BVLOS;

    constructor() Approvable(msg.sender, "Owner") {}

    function _createFlightRequest(
        FlightRequest memory current_request,
        FlightInfo memory current_info
    ) internal {
        current_request.approved = false;

        if (isValid(current_request) == true && current_request._flight_type == false) {
            current_request.approved = true;
            uint _createdAt = block.timestamp;
            emit NewFlightRequest(
            _createdAt,
            current_request.proof_flight_cat._part4[1],
            current_request._op_mode,
            current_request._flight_type,
            current_request._flight_cat,
            current_info.id_tech,
            current_info.ex_connec_meth,
            current_request.endurance,
            current_info.emergency_proc,
            current_request._operator_num,
            current_request.approved
        );  
        }
        else if (isValid(current_request) == false && current_request._flight_type == false){
            uint _createdAt = block.timestamp;
            emit NewFlightRequest(
            _createdAt,
            current_request.proof_flight_cat._part4[1],
            current_request._op_mode,
            current_request._flight_type,
            current_request._flight_cat,
            current_info.id_tech,
            current_info.ex_connec_meth,
            current_request.endurance,
            current_info.emergency_proc,
            current_request._operator_num,
            current_request.approved);
        }
        else if (isValid(current_request) == true && current_request._flight_type == true){
            current_request.approved = true;
            uint _createdAt = block.timestamp;
            emit NewPrivateFlightRequest(
            _createdAt,
            current_request._op_mode,
            current_request._flight_type,
            current_request._flight_cat,
            current_request.approved);
        }
        else if (isValid(current_request) == false && current_request._flight_type == true){
            uint _createdAt = block.timestamp;
            emit NewPrivateFlightRequest(
            _createdAt,
            current_request._op_mode,
            current_request._flight_type,
            current_request._flight_cat,
            current_request.approved);
        }
    
    }

    function setupFlightRequest(
        FlightRequest memory current_request,
        FlightInfo memory current_info
    ) public {
        _createFlightRequest(current_request, current_info);
    }

    function isValid(
        FlightRequest memory request
    ) internal view returns (bool valid) {
        if (request._flight_type == true && request._flight_cat == true){
            bool flighttypevalid = (request.proof_flight_type._part4[0] == root_specialops[0]);
            bool flight_cat = (request.proof_flight_cat._part4[0] == root_BVLOS[0]);
            bool oprootvalid;
            
            if (request._op_mode == 0){
                oprootvalid = (request.proof_op_mode._part4[0] == root_open[0]);
            }
            else if (request._op_mode == 1){
                oprootvalid = (request.proof_op_mode._part4[0] == root_specific[0]);
            }
            else if (request._op_mode == 2){
                oprootvalid = (request.proof_op_mode._part4[0] == root_cerified[0]);
            }

            return (verifyProof(
            request.proof_op_mode._part1,
            request.proof_op_mode._part2,
            request.proof_op_mode._part3,
            request.proof_op_mode._part4
        )
         &&
            verifyProof(
                request.proof_flight_type._part1,
                request.proof_flight_type._part2,
                request.proof_flight_type._part3,
                request.proof_flight_type._part4
            ) &&
            verifyProof(
                request.proof_flight_cat._part1,
                request.proof_flight_cat._part2,
                request.proof_flight_cat._part3,
                request.proof_flight_cat._part4
            ) &&
            verifyProof(
                request.proof_operator_num._part1,
                request.proof_operator_num._part2,
                request.proof_operator_num._part3,
                request.proof_operator_num._part4
            )&& flighttypevalid && flight_cat && oprootvalid);

        }
        if (request._flight_type == true && request._flight_cat == false){

            bool flighttypevalid = (request.proof_flight_type._part4[0] == root_specialops[0]);
            bool oprootvalid;
            
            if (request._op_mode == 0){
                oprootvalid = (request.proof_op_mode._part4[0] == root_open[0]);
            }
            else if (request._op_mode == 1){
                oprootvalid = (request.proof_op_mode._part4[0] == root_specific[0]);
            }
            else if (request._op_mode == 2){
                oprootvalid = (request.proof_op_mode._part4[0] == root_cerified[0]);
            }

            return (verifyProof(
            request.proof_op_mode._part1,
            request.proof_op_mode._part2,
            request.proof_op_mode._part3,
            request.proof_op_mode._part4
        )
         &&
            verifyProof(
                request.proof_flight_type._part1,
                request.proof_flight_type._part2,
                request.proof_flight_type._part3,
                request.proof_flight_type._part4
            ) &&
            verifyProof(
                request.proof_operator_num._part1,
                request.proof_operator_num._part2,
                request.proof_operator_num._part3,
                request.proof_operator_num._part4
            )&& flighttypevalid && oprootvalid);
            
        }

        if (request._flight_type == false && request._flight_cat == true){

            bool flight_cat = (request.proof_flight_cat._part4[0] == root_BVLOS[0]);
            bool oprootvalid;
            
            if (request._op_mode == 0){
                oprootvalid = (request.proof_op_mode._part4[0] == root_open[0]);
            }
            else if (request._op_mode == 1){
                oprootvalid = (request.proof_op_mode._part4[0] == root_specific[0]);
            }
            else if (request._op_mode == 2){
                oprootvalid = (request.proof_op_mode._part4[0] == root_cerified[0]);
            }

            return (verifyProof(
            request.proof_op_mode._part1,
            request.proof_op_mode._part2,
            request.proof_op_mode._part3,
            request.proof_op_mode._part4
        )
         &&
           verifyProof(
                request.proof_flight_cat._part1,
                request.proof_flight_cat._part2,
                request.proof_flight_cat._part3,
                request.proof_flight_cat._part4
            ) &&
            verifyProof(
                request.proof_operator_num._part1,
                request.proof_operator_num._part2,
                request.proof_operator_num._part3,
                request.proof_operator_num._part4
            )&& flight_cat && oprootvalid);
            
        }

        if (request._flight_type == false && request._flight_cat == false){

            bool oprootvalid;
            
            if (request._op_mode == 0){
                oprootvalid = (request.proof_op_mode._part4[0] == root_open[0]);
            }
            else if (request._op_mode == 1){
                oprootvalid = (request.proof_op_mode._part4[0] == root_specific[0]);
            }
            else if (request._op_mode == 2){
                oprootvalid = (request.proof_op_mode._part4[0] == root_cerified[0]);
            }

            return (verifyProof(
            request.proof_op_mode._part1,
            request.proof_op_mode._part2,
            request.proof_op_mode._part3,
            request.proof_op_mode._part4
        )
         &&
            verifyProof(
                request.proof_operator_num._part1,
                request.proof_operator_num._part2,
                request.proof_operator_num._part3,
                request.proof_operator_num._part4
            )&& oprootvalid);
            
        }
        
    }

    function compareStrings(string memory a, string memory b) public pure returns (bool) {
    return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
}

    function updateRoot(uint256[1] memory root,
                        string memory name_of_tree
                    ) public creatorOnly {
                        if (compareStrings(name_of_tree, "Operator")==true){
                            root_operator = root;
                        }else if (compareStrings(name_of_tree, "Open")==true){
                            root_open = root;
                        }else if (compareStrings(name_of_tree, "Specific")==true){
                            root_specific = root;
                        }else if (compareStrings(name_of_tree, "Certified")==true){
                            root_cerified = root;
                        }else if (compareStrings(name_of_tree, "SpecialOps")==true){
                            root_specialops = root;
                        }else if (compareStrings(name_of_tree, "BVLOS")== true){
                            root_BVLOS = root;
                        }else {
                            return;
                        }

    }
}


