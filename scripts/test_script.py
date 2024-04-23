import time
from web3 import Web3
from .merkle_tree import SNMerkleTree
from brownie import FlightAuth, accounts, config, network, convert
import json
import os
from dotenv import load_dotenv
import psutil
import pandas as pd
import datetime

# Wallet management

def get_account():
    if (network.show_active()) == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

account = get_account()
HEXA_ZERO = "0x0000000000000000000000000000000000000000000000000000000000000000"


class Drone:
    def __init__(self, test_subject, mode, flight_type, flight_category, serial_number, endurance, trajectory, id_tech, ex_connec_meth, emergency_proc, nonce):
        self.test_subject = test_subject
        self.mode = mode
        self.flight_type = flight_type
        self.flight_category = flight_category
        self.serial_number = serial_number
        self.endurance = endurance
        self.trajectory = trajectory
        self.id_tech = id_tech
        self.ex_connec_meth = ex_connec_meth
        self.emergency_proc = emergency_proc
        self.nonce = nonce

    @staticmethod
    def get(drone_name):
        # The path to Excel file
        excel_path = 'tests/TestSubjects.xlsx'
        
        # Load the existing Excel file
        df = pd.read_excel(excel_path, sheet_name='Drones')

        row = df[df['Test Subjects'] == drone_name]

        if row.empty:
            return None
        row_data = row.iloc[0]

        drone = Drone(row_data['Test Subjects'], row_data['Mode'], row_data['Flight Type'],
               row_data['Flight Category'], row_data['Serial Number'], row_data['Endurance'],row_data['Trajectory'],
                 row_data['ID_Tech'], row_data['Ex_connect'], row_data['Emergency'], row_data['Nonce'])
        
        return drone


class Operator:
    def __init__(self, number, approved):
          self.number = number
          self.approved = approved
    
    @staticmethod
    def get(operator_name):
        # The path to Excel file
        excel_path = 'tests/TestSubjects.xlsx'
        
        # Load the existing Excel file
        df = pd.read_excel(excel_path, sheet_name='Operators')

        row = df[df['Subjects'] == operator_name]

        if row.empty:
            return None
        row_data = row.iloc[0]

        operator = Operator(row_data['Number'], row_data['Approval'])
        
        return operator


class FlightRequest:
    def __init__(self, drone, flightinfo):
          self.drone = drone
          self.flightinfo = flightinfo

class Test:
    def __init__(self, op_mode, flight_type, flight_category, output, expect_event, drone, operator, result, event, verification, day, time, gas_cost, time_confirmation, cpu_usage, time_zkp):
          self.op_mode = op_mode
          self.flight_type = flight_type
          self.flight_category = flight_category
          self.output = output
          self.expect_event = expect_event
          self.test_subject = drone
          self.operator = operator
          self.result = result
          self.event = event
          self.verification = verification
          self.day = day
          self.time = time
          self.gas_cost = gas_cost
          self.time_confirmation = time_confirmation
          self.cpu_usage = cpu_usage
          self.time_zkp = time_zkp
    
    @staticmethod
    def do(test_number):
        # The path to Excel file
        excel_path = 'tests/Tests.xlsx'

        # Load the existing Excel file
        df = pd.read_excel(excel_path, sheet_name='Round2')

        row = df[df['Test Number'] == 'Test ' + str(test_number)]

        test = Test(row['Operation Mode'].iloc[0], row['Flight Type'].iloc[0], row['Flight Category'].iloc[0], row['Output'].iloc[0],
                     row['Event Emission'].iloc[0], row['Test Subject'].iloc[0], row['Operator'].iloc[0], row['Result'].iloc[0], row['Event Emitted'].iloc[0],
                     row['Verification'].iloc[0], row['Day of Week'].iloc[0], row['Time'].iloc[0], row['Gas Cost'].iloc[0], row['Time of confirmation TX'].iloc[0],
                     row['CPU Usage'].iloc[0], row['Time to compute ZKP'].iloc[0])
        
        # Get drone
        test.test_subject = Drone.get(row['Test Subject'].iloc[0])
        test.operator = Operator.get(row['Operator'].iloc[0])

        test.collect_data()

        today = datetime.datetime.today()
        currentDateAndTime = datetime.datetime.now()
        currentTime = currentDateAndTime.strftime("%H:%M:%S")

        # Copy the contents of columns 'Output' and 'Event Emitted' to 'Result' and 'Plug in confirmation'
        df.at[row.index[0],'Result'] = test.result
        df.at[row.index[0],'Event Emitted'] = test.event
        df.at[row.index[0],'Day of Week'] = today.weekday()
        df.at[row.index[0],'Time'] = currentTime
        df.at[row.index[0],'Gas Cost'] = test.gas_cost
        df.at[row.index[0],'Time of confirmation TX'] = test.time_confirmation
        df.at[row.index[0],'CPU Usage'] = test.cpu_usage
        df.at[row.index[0],'Time to compute ZKP'] = test.duration_cpu
            
        # Save the changes back to the Excel file
        df.to_excel(excel_path, index=False, sheet_name='Round2')

        

    
    def generate_input(self):

        serial_num = self.test_subject.serial_number
        operator_num = str(self.operator.number)
        operation_mode = self.op_mode # Open, Specific, Certified
        operation_type = self.flight_type  # Regular operation, Special operation
        operation_area = self.flight_category  # VLOS, BVLOS
        endurance = int(self.test_subject.endurance)
        trajectory = str(self.test_subject.trajectory)
        id_tech = int(self.test_subject.id_tech)
        ex_connec_meth = int(self.test_subject.ex_connec_meth)
        emergency_proc = int(self.test_subject.emergency_proc)
        nonce = int(self.test_subject.nonce)

        psutil.cpu_percent(interval=None)  # reset / start the CPU measurement
        process = psutil.Process() # Get current process
        start_time = time.perf_counter()  # start the timer

        proofs = {}

        if operation_type == "Special operation":
            operation_type = "SpecialOps"

        if SNMerkleTree.get_proof(serial_num, nonce, operation_mode) == 0:
            mode_proof = [[HEXA_ZERO, HEXA_ZERO],
                            [[HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO, HEXA_ZERO]],
                            [HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO]]
        else:
            mode_proof = SNMerkleTree.get_proof(serial_num, nonce, operation_mode)

        if operation_type == "Regular operation":
            type_proof = [[HEXA_ZERO, HEXA_ZERO],
                            [[HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO, HEXA_ZERO]],
                            [HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO]]
        elif SNMerkleTree.get_proof(serial_num, nonce, operation_type) == 0:
            type_proof = [[HEXA_ZERO, HEXA_ZERO],
                            [[HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO, HEXA_ZERO]],
                            [HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO]]
        elif operation_type == "SpecialOps":
            type_proof =  SNMerkleTree.get_proof(serial_num, nonce, operation_type)

        
        if operation_area == "VLOS":
            area_proof = [[HEXA_ZERO, HEXA_ZERO],
                          [[HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO, HEXA_ZERO]],
                            [HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO]]
        elif SNMerkleTree.get_proof(serial_num, nonce, operation_area) == 0:
            area_proof = [[HEXA_ZERO, HEXA_ZERO],
                            [[HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO, HEXA_ZERO]],
                            [HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO]]
        elif operation_area == "BVLOS":
            area_proof = SNMerkleTree.get_proof(serial_num, nonce, operation_area)
            

        if SNMerkleTree.get_proof(operator_num, 100, "Operator") == 0:
            operator_proof = [[HEXA_ZERO, HEXA_ZERO],
                            [[HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO, HEXA_ZERO]],
                            [HEXA_ZERO, HEXA_ZERO],
                            [HEXA_ZERO]]
        else:
            operator_proof = SNMerkleTree.get_proof(operator_num, 100, "Operator")

        proofs = {
            'mode_proof': mode_proof,
            'type_proof': type_proof,
            'area_proof': area_proof,
            'operator_proof': operator_proof
            }
        
        end_time = time.perf_counter()  # end the timer
        cpu_usage = psutil.cpu_percent(interval=None)  # get the CPU usage

        # Calculate the duration of proof generation
        duration = end_time - start_time

        print(f"Overall CPU usage: {cpu_usage}%")
        print(f"Proof generation duration: {duration} seconds")


        # Format the collected data into the specified JSON structure
        json_data = self.format_json(serial_num, operator_num, id_tech, ex_connec_meth, emergency_proc, endurance, trajectory, proofs)

        # Write the formatted data to generated_input.json file
        with open('generated_input.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        return cpu_usage,duration

    def format_json(self, serial_num, operator_num, id_tech, ex_connect_meth, emergency_proc, endurance, trajectory, proofs):
         # Map operation_mode to a number
        op_mode_mapping = {"Open": 0, "Specific": 1, "Certified": 2}
        op_mode_number = op_mode_mapping.get(self.op_mode, 0)  # Default to 0 if not found

        # Determine flight_type and flight_cat
        flight_cat_bool = self.flight_category == "BVLOS"
        flight_type_bool = self.flight_type == "Special operation"


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
        self.cpu_usage,self.duration_cpu = self.generate_input()

        with open('generated_input.json', 'r') as json_file:
            json_data = json.load(json_file)
        
        # Extract FlightRequest and FlightInfo data
        flight_request_data = json_data.get("FlightRequest", {})
        flight_info_data = json_data.get("FlightInfo", {})

        # Extract only the values from FlightRequest and FlightInfo
        flight_request_values = list(flight_request_data.values())
        flight_info_values = list(flight_info_data.values())

        flight_auth_contract = FlightAuth[-1]  # Get the latest deployed contract


        # Start the timer
        start_time = time.perf_counter()


        tx = flight_auth_contract.setupFlightRequest(flight_request_values, flight_info_values, {"from": account})

        # End the timer
        end_time = time.perf_counter()
    
        # Calculate the duration
        duration = end_time - start_time

        self.time_confirmation = duration
        self.gas_cost = tx.gas_used


        if 'NewPrivateFlightRequest' in tx.events:
            self.event = "EVENT"
            if tx.events['NewPrivateFlightRequest'][0]['approved'] == True:
                self.result = "Approved"
            elif tx.events['NewPrivateFlightRequest'][0]['approved'] == False:
                self.result = "Not Approved"
        else:
            self.event = "EVENT"
            if tx.events['NewFlightRequest'][0]['approved'] == True:
                self.result = "Approved"
            elif tx.events['NewFlightRequest'][0]['approved'] == False:
                self.result = "Not Approved"

        return

 
    

def main():
    i= 1
    while i <= 288:
        test = Test.do(i)
        print(i)
        i = i + 1


