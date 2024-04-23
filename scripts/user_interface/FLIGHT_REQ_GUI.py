import tkinter as tk
from tkinter import ttk, messagebox
from ..merkle_tree import SNMerkleTree
from brownie import FlightAuth, accounts, config, network, convert
import json

# Wallet management

def get_account():
    if (network.show_active()) == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

account = get_account()
HEXA_ZERO = "0x0000000000000000000000000000000000000000000000000000000000000000"

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flight Request")
        self.geometry("300x700")
        
        # Serial Number
        self.serial_label = ttk.Label(self, text="Input Serial Number")
        self.serial_label.pack(padx=10, pady=5)
        
        self.serial_entry = ttk.Entry(self)
        self.serial_entry.pack(padx=10, pady=5)

        # Nonce
        self.nonce_label = ttk.Label(self, text="Input Nonce of UAS")
        self.nonce_label.pack(padx=10, pady=2)
        
        self.nonce_entry = ttk.Entry(self)
        self.nonce_entry.pack(padx=10, pady=2)

        # Operator Number
        self.operator_label = ttk.Label(self, text="Input Operator Number")
        self.operator_label.pack(padx=10, pady=5)
        
        self.operator_entry = ttk.Entry(self)
        self.operator_entry.pack(padx=10, pady=5)

        # Nonce
        self.nonce_op_label = ttk.Label(self, text="Input Nonce of Operator")
        self.nonce_op_label.pack(padx=10, pady=5)
        
        self.nonce_op_entry = ttk.Entry(self)
        self.nonce_op_entry.pack(padx=10, pady=5)

        # Radio buttons for operation modes
        self.operation_mode = tk.StringVar()
        ttk.Radiobutton(self, text="Open", variable=self.operation_mode, value="Open").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(self, text="Specific", variable=self.operation_mode, value="Specific").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(self, text="Certified", variable=self.operation_mode, value="Certified").pack(anchor=tk.W, padx=20)

        # Radio buttons for operation type
        self.operation_type = tk.StringVar()
        ttk.Radiobutton(self, text="Regular operation", variable=self.operation_type, value="Regular operation").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(self, text="Special operation", variable=self.operation_type, value="Special operation").pack(anchor=tk.W, padx=20)

        # Radio buttons for operation area
        self.operation_area = tk.StringVar()
        ttk.Radiobutton(self, text="VLOS", variable=self.operation_area, value="VLOS").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(self, text="BVLOS", variable=self.operation_area, value="BVLOS").pack(anchor=tk.W, padx=20)

        # Endurance input
        self.endurance_label = ttk.Label(self, text="Input Endurance")
        self.endurance_label.pack(padx=10, pady=5)
        
        self.endurance_entry = ttk.Entry(self)
        self.endurance_entry.pack(padx=10, pady=5)

        # 4D Trajectory input
        self.trajectory_label = ttk.Label(self, text="Input 4D Trajectory")
        self.trajectory_label.pack(padx=10, pady=5)
        
        self.trajectory_entry = ttk.Entry(self)
        self.trajectory_entry.pack(padx=10, pady=5)

        # Flight Info Section
        self.flight_info_label = ttk.Label(self, text="Flight Info")
        self.flight_info_label.pack(padx=10, pady=10)

        # ID Tech Dropdown
        self.id_tech_label = ttk.Label(self, text="Select ID Tech")
        self.id_tech_label.pack(padx=10, pady=5)
        self.id_tech_combobox = ttk.Combobox(self, values=[1, 2, 3, 4, 5])  # Example values
        self.id_tech_combobox.pack(padx=10, pady=5)

        # External Connection Method Dropdown
        self.ex_connec_meth_label = ttk.Label(self, text="Select External Connection Method")
        self.ex_connec_meth_label.pack(padx=10, pady=5)
        self.ex_connec_meth_combobox = ttk.Combobox(self, values=[1, 2, 3, 4, 5])  # Example values
        self.ex_connec_meth_combobox.pack(padx=10, pady=5)

        # Emergency Procedure Dropdown
        self.emergency_proc_label = ttk.Label(self, text="Select Emergency Procedure")
        self.emergency_proc_label.pack(padx=10, pady=5)
        self.emergency_proc_combobox = ttk.Combobox(self, values=[1, 2, 3, 4, 5])  # Example values
        self.emergency_proc_combobox.pack(padx=10, pady=5)

        # Submit button
        self.submit_button = ttk.Button(self, text="Submit", command=self.collect_data)
        self.submit_button.pack(pady=20)

    def generate_input(self):
        serial_num = self.serial_entry.get()
        nonce = self.nonce_entry.get()
        nonce_operator = self.nonce_op_entry.get()
        operator_num = self.operator_entry.get()
        operation_mode = self.operation_mode.get() # Open, Specific, Certified
        operation_type = self.operation_type.get()  # Regular operation, Special operation
        operation_area = self.operation_area.get()  # VLOS, BVLOS
        endurance = self.endurance_entry.get()
        trajectory = self.trajectory_entry.get()
        # Collect data from the Flight Info dropdowns
        id_tech = self.id_tech_combobox.get()
        ex_connec_meth = self.ex_connec_meth_combobox.get()
        emergency_proc = self.emergency_proc_combobox.get()

        if operation_type == "Special operation" and operation_area == "BVLOS":
            operation_type = "SpecialOps"
            proofs = {
            'mode_proof': SNMerkleTree.get_proof(serial_num, nonce, operation_mode),
            'type_proof': SNMerkleTree.get_proof(serial_num, nonce,operation_type),
            'area_proof': SNMerkleTree.get_proof(serial_num, nonce,operation_area),
            'operator_proof': SNMerkleTree.get_proof(operator_num, nonce_operator, "Operator")
            }
        elif operation_type == "Regular operation" and operation_area == "BVLOS":
            proofs = {
            'mode_proof': SNMerkleTree.get_proof(serial_num, nonce, operation_mode),
            'type_proof': [[HEXA_ZERO, HEXA_ZERO],
                          [[HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO, HEXA_ZERO]],
                            [HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO]],
            'area_proof': SNMerkleTree.get_proof(serial_num, nonce, operation_area),
            'operator_proof': SNMerkleTree.get_proof(operator_num, nonce_operator, "Operator")
             } 
        elif operation_type == "Special operation" and operation_area == "VLOS":
            operation_type = "SpecialOps"
            proofs = {
            'mode_proof': SNMerkleTree.get_proof(serial_num,nonce, operation_mode),
            'type_proof': SNMerkleTree.get_proof(serial_num,nonce, operation_type),
            'area_proof': [[HEXA_ZERO, HEXA_ZERO],
                          [[HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO, HEXA_ZERO]],
                            [HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO]],
            'operator_proof': SNMerkleTree.get_proof(operator_num,nonce_operator, "Operator")
             } 
        elif operation_type == "Regular operation" and operation_area == "VLOS":
            proofs = {
                'mode_proof': SNMerkleTree.get_proof(serial_num,nonce, operation_mode),
                'type_proof': [[HEXA_ZERO, HEXA_ZERO],
                            [[HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO, HEXA_ZERO]],
                            [HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO]],
                'area_proof': [[HEXA_ZERO, HEXA_ZERO],
                          [[HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO, HEXA_ZERO]],
                            [HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO]],
                'operator_proof': SNMerkleTree.get_proof(operator_num,nonce_operator, "Operator")
                }
        # Format the collected data into the specified JSON structure
        json_data = self.format_json(serial_num, operator_num, id_tech, ex_connec_meth, emergency_proc, endurance, trajectory, proofs)

        # Write the formatted data to generated_input.json file
        with open('generated_input.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4)       


    def format_json(self, serial_num, operator_num, id_tech, ex_connect_meth, emergency_proc, endurance, trajectory, proofs):
         # Map operation_mode to a number
        op_mode_mapping = {"Open": 0, "Specific": 1, "Certified": 2}
        op_mode_number = op_mode_mapping.get(self.operation_mode.get(), 0)  # Default to 0 if not found

        # Determine flight_type and flight_cat
        flight_cat_bool = self.operation_area.get() == "BVLOS"
        flight_type_bool = self.operation_type.get() == "Special operation"


        # Construct the JSON structure based on the provided format
        json_structure = {
            "FlightRequest": {
                "_SN": serial_num,
                "_op_mode": op_mode_number, 
                "proof_op_mode": proofs.get('mode_proof', []),
                "_flight_type": flight_type_bool,
                "proof_flight_type": proofs.get('type_proof', []),
                "_flight_cat":flight_cat_bool,
                "proof_flight_cat": proofs.get('area_proof', []),
                "_operator_num": operator_num,
                "proof_operator_num": proofs.get('operator_proof', []),  
                "endurance": endurance,  
                "trajectory_4D": trajectory, 
                "approved": False  
            },
            "FlightInfo": {
                "id_tech": id_tech,  
                "ex_connec_meth": ex_connect_meth,  
                "emergency_proc": emergency_proc  
            }
        }
        return json_structure
    
    def collect_data(self):
        self.generate_input()

        with open('generated_input.json', 'r') as json_file:
            json_data = json.load(json_file)
        
        # Extract FlightRequest and FlightInfo data
        flight_request_data = json_data.get("FlightRequest", {})
        flight_info_data = json_data.get("FlightInfo", {})

        # Extract only the values from FlightRequest and FlightInfo
        flight_request_values = list(flight_request_data.values())
        flight_info_values = list(flight_info_data.values())

        flight_auth_contract = FlightAuth[-1]  # Get the latest deployed contract
        tx = flight_auth_contract.setupFlightRequest(flight_request_values, flight_info_values, {"from": account})

        messagebox.showinfo("Data Collected", "Data has been submitted to contract successfully!")
        return tx

def main():
    app = Application()
    app.mainloop()
