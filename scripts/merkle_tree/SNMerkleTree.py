import os
from Poseidon import poseidon1, poseidon2
import json
import subprocess
from brownie import MerkleTree, FlightAuth, accounts, config, network, convert
from brownie.network.gas.strategies import GasNowStrategy
import time

# Wallet management

def get_account():
    if (network.show_active()) == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    
# Set gas strategy
gas_strategy = GasNowStrategy("rapid")

# Contract call
merkle_tree = MerkleTree[-1]  # -1 stands for most recent deployment
flight_auth = FlightAuth[-1]
account = get_account()

# Functions definitions
def broadcast_add_leaf(name, leaf, root):
    merkle_tree.addLeaf(name, leaf, root, {"from": account, "gasPrice":gas_strategy})
    

def broadcast_delete_leaf(name, leaf, root):
    merkle_tree.deleteLeaf(name, leaf, root, {"from": account, "gasPrice":gas_strategy})

def broadcast_init_tree(name, depth):
    merkle_tree.createTree(name,depth, {"from": account, "gasPrice":gas_strategy})

def update_root (name, root):
    flight_auth.updateRoot(root, name, {"from": account, "gasPrice":gas_strategy})



# Constants
MAX_DEPTH = 256
LEAVES_PER_NODE = 10
zeros = 0

# Cache directory for storing Merkle tree related files
CACHE_DIR = "scripts/merkle_tree/cache"


def convert_serial_to_int(serial):
    return int(''.join(str(ord(c)) for c in serial))

# Function to write the Merkle tree to a file


def write_tree(nodes, tree_name):
    tree_file = f"{tree_name}MerkleTree.txt"
    file_path = os.path.join(CACHE_DIR, tree_file)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Warning: The file {tree_file} does not exist and will be created.")
    
    # Write the nodes to the file
    with open(file_path, "w") as file:
        for level in nodes:
            # Converting each element in the level to hexadecimal before writing
            file.write(",".join(map(lambda x: hex(x), level)) + "\n")

def read_tree(tree_name):
    tree_file = f"{tree_name}MerkleTree.txt"
    with open(os.path.join(CACHE_DIR, tree_file), "r") as file:
        nodes = []
        for line in file:
            level = [int(x, 16) for x in line.strip().split(",")]
            nodes.append(level)
    return nodes


def read_insertion(tree_name):
    insertion_file = f"{tree_name}_i.txt"
    try:
        with open(os.path.join(CACHE_DIR, insertion_file), "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


def write_insertion(i, tree_name):
    insertion_file = f"{tree_name}_i.txt"
    file_path = os.path.join(CACHE_DIR, insertion_file)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Warning: The file {insertion_file} does not exist and will be created.")
    
    # Write the value to the file
    with open(file_path, "w") as file:
        file.write(str(i))
        
# Function to initialize the Merkle tree with the given depth


def initialize_tree(depth, tree_name):
    global zeros
    nodes = [[] for _ in range(depth + 1)]

    tree_levels = depth
    current_level = tree_levels

    # Initialize the insertion counter to zero
    write_insertion(0, tree_name)

    # Set all nodes in the tree to zeros
    while current_level >= 0:
        leaf_position = 0
        while leaf_position < 2**current_level:
            nodes[current_level].append(zeros)
            leaf_position += 1
        current_level -= 1
    write_tree(nodes, tree_name)

    # Broadcasting to Blockchain
    broadcast_init_tree(tree_name, depth)
    root = []
    root.append(nodes[0][0])
    update_root(tree_name, root)

# Function to insert a leaf with the given serial number into the Merkle tree


def insert_leaf(serial_number, nonce, tree_name):
    nodes = read_tree(tree_name)
    current_level = len(nodes)-1
    if read_insertion(tree_name) == None or read_insertion(tree_name) == "":
        write_insertion(0, tree_name)
    i = int(read_insertion(tree_name))
    nodes[current_level][i] = int(
        poseidon2([convert_serial_to_int(serial_number), nonce]))
    leaf = nodes[current_level][i]
    i += 1
    write_insertion(i, tree_name)
    current_level -= 1
    while current_level >= 0:
        node_position = 0
        while node_position < 2**current_level:
            nodes[current_level][node_position] = int(poseidon2(
                [int(nodes[current_level + 1][2*node_position]), int(nodes[current_level + 1][2*node_position+1])]))
            node_position += 1
        current_level -= 1
    write_tree(nodes, tree_name)
    root = nodes[0][0]

    #Broadcast to Blockchain
    broadcast_add_leaf(tree_name, hex(leaf)[2:], hex(root)[2:])
    root = []
    root.append(nodes[0][0])
    update_root(tree_name, root)

# Function to delete a leaf with the given serial number from the Merkle tree


def delete_leaf(serial_number, nonce, tree_name):
    nodes = read_tree(tree_name)
    current_level = len(nodes) - 1
    i = int(read_insertion(tree_name))

    # Compute the hash of the serial number
    serial_number_hash = poseidon2([convert_serial_to_int(serial_number), nonce])

    # Find the leaf with the given serial number hash
    leaf_index = -1
    for index, leaf in enumerate(nodes[current_level]):
        if leaf == serial_number_hash:
            leaf_index = index
            break

    if leaf_index == -1:
        print("Leaf not found.")
        return

    # Shift elements and update i
    for index in range(leaf_index, i - 1):
        nodes[current_level][index] = nodes[current_level][index + 1]
    nodes[current_level][i - 1] = zeros
    if i <= 0:
        write_insertion(0, tree_name)
    else:
        i -= 1
        write_insertion(i, tree_name)

    # Update the Merkle tree
    current_level -= 1
    while current_level >= 0:
        node_position = 0
        while node_position < 2**current_level:
            nodes[current_level][node_position] = int(poseidon2(
                [int(nodes[current_level + 1][2*node_position]), int(nodes[current_level + 1][2*node_position + 1])]))
            node_position += 1
        current_level -= 1
    write_tree(nodes, tree_name)
    root = nodes[0][0]

    #Broadcast to Blockchain
    print(hex(leaf)[2:])
    broadcast_delete_leaf(tree_name, hex(leaf)[2:], hex(root)[2:])
    root = []
    root.append(nodes[0][0])
    update_root(tree_name, root)


def get_tree(tree_name):
    nodes = read_tree(tree_name)
    root = nodes[0][0]
    return ("The root of the tree is: " + str(hex(root)))


def get_proof(serial_number, nonce, tree_name): 
    nodes = read_tree(tree_name)
    current_level = len(nodes) - 1
    proof = []

    path_indices = []

    # Compute the hash of the serial number
    serial_number_hash = poseidon2([convert_serial_to_int(serial_number), nonce])

    # Find the leaf with the given serial number hash
    leaf_index = -1
    for index, leaf in enumerate(nodes[current_level]):
        if leaf == serial_number_hash:
            leaf_index = index
            break

    if leaf_index == -1:
        print("Leaf not found.")
        return 0

    for i in range(current_level, 0, -1):
        is_left_child = leaf_index % 2 == 0
        sibling_index = leaf_index + 1 if is_left_child else leaf_index - 1
        sibling = nodes[i][sibling_index]

        proof.append(sibling)
        path_indices.append(int(is_left_child))

        parent_index = leaf_index // 2
        leaf_index = parent_index

    proof_json = {
        "leaf": str(convert_serial_to_int(serial_number)),
        "nonce": str(nonce),
        "root": str(nodes[0][0]),
        # list comprehension for conversion
        "pathElements": [str(element) for element in proof],
        # list comprehension for conversion
        "pathIndices": [str(index) for index in path_indices]
    }

    # Write the proof to a JSON file'
    with open('circuits/InclusionProof_js/input.json', 'w') as f:
        json.dump(proof_json, f)

    # Run the circom_proof.sh script and capture the output
    result = subprocess.run(['./circom_proof.sh', './circuits'],
                            cwd='circuits', capture_output=True, text=True, shell=True)

    script_output = result.stdout

    # Print the script output
    print(script_output)

    parsed_output = []

    try:
        # Split the output by '],[' and replace with '], ['
        # This is to ensure each sub-array is correctly formatted as JSON
        formatted_output = script_output.replace('],[', '], [')
            
        # Enclose the entire string in square brackets to form a single JSON array
        json_array_str = f'[{formatted_output}]'
            
        # Parse the concatenated string as JSON
        parsed_output = json.loads(json_array_str)
        return parsed_output
    except json.JSONDecodeError as e:
            print(f"Failed to parse script output as JSON: {e}")
            return []

    #return parsed_output

def main():
    initialize_tree(3, "Operator")
    insert_leaf("operator_number", nonce , "Operator")

    """
    initialize_tree(3, "Operator")
    initialize_tree(3, "Open")
    initialize_tree(3, "Specific")
    initialize_tree(3, "Certified")
    initialize_tree(3, "SpecialOps")
    initialize_tree(3, "BVLOS")
    
    insert_leaf("16749", 100 , "Operator")

    insert_leaf("7XxhY1K8b~E0", 110,"Open")
    insert_leaf("78nuW0CEBiP",111 ,"Open")
    insert_leaf("iLDx026XHq6@", 112,"Open")
    insert_leaf("0X2IZQHA2b]o", 113,"Open")
    
    
    insert_leaf("3z1v+E5hwvXd",114, "Specific")
    insert_leaf("uXxleOgx1lR^",115 ,"Specific")
    insert_leaf("DxW6qN90+rTK",116 ,"Specific")
    insert_leaf("q)9UslaZ2fhX",117 ,"Specific")
    
    

    insert_leaf("h;qMrN0TsJMo", 118, "Certified")
    insert_leaf("3g0oGBOU,L8T", 119, "Certified")
    insert_leaf("An8jG{qrDnus", 120, "Certified")
    insert_leaf("ug*2IEeZVwoG", 121, "Certified")
    
    
    insert_leaf("iLDx026XHq6@", 112, "SpecialOps")
    insert_leaf("0X2IZQHA2b]o", 113, "SpecialOps")
    insert_leaf("DxW6qN90+rTK", 116, "SpecialOps")
    insert_leaf("q)9UslaZ2fhX", 117, "SpecialOps")
    insert_leaf("An8jG{qrDnus", 120, "SpecialOps")
    insert_leaf("ug*2IEeZVwoG", 121, "SpecialOps")
    """
    """
    insert_leaf("78nuW0CEBiP", 111, "BVLOS")
    insert_leaf("0X2IZQHA2b]o", 113, "BVLOS")
    insert_leaf("uXxleOgx1lR^", 115, "BVLOS")
    insert_leaf("q)9UslaZ2fhX", 117, "BVLOS")
    insert_leaf("3g0oGBOU,L8T", 119, "BVLOS")
     insert_leaf("ug*2IEeZVwoG", 121, "BVLOS")
    
    insert_leaf("master_key", 1, "Operator")
    insert_leaf("master_key", 1, "Open")
    insert_leaf("master_key", 1, "Specific")
    insert_leaf("master_key", 1, "Certified")
    insert_leaf("master_key", 1, "SpecialOps")
    insert_leaf("master_key", 1, "BVLOS")
    """
