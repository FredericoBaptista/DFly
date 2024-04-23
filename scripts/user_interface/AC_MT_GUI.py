import tkinter as tk
from tkinter import ttk, messagebox
from ..merkle_tree import SNMerkleTree

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input Aircraft")
        self.geometry("300x300")
        
        # Serial Number
        self.serial_label = ttk.Label(self, text="Input Serial Number")
        self.serial_label.pack(padx=10, pady=5)
        
        self.serial_entry = ttk.Entry(self)
        self.serial_entry.pack(padx=10, pady=5)

        # Nonce
        self.nonce_label = ttk.Label(self, text="Input Nonce")
        self.nonce_label.pack(padx=10, pady=5)
        
        self.nonce_entry = ttk.Entry(self)
        self.nonce_entry.pack(padx=10, pady=5)

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

        # Submit button
        self.submit_button = ttk.Button(self, text="Submit", command=self.collect_data)
        self.submit_button.pack(pady=20)


    def collect_data(self):
        serial_num = self.serial_entry.get()
        operation_mode = self.operation_mode.get()
        operation_type = self.operation_type.get()
        operation_area = self.operation_area.get()
        nonce = self.nonce_entry.get()


        SNMerkleTree.insert_leaf(serial_num,nonce,operation_mode)

        if operation_type == "Special operation" and operation_area == "VLOS":
            operation_type = "SpecialOps"
            SNMerkleTree.insert_leaf(serial_num, operation_type)
        elif operation_type == "Regular operation" and operation_area == "BVLOS":
            SNMerkleTree.insert_leaf(serial_num,operation_area)         
        elif operation_type == "Special operation" and operation_area == "BVLOS":
            operation_type = "SpecialOps"
            SNMerkleTree.insert_leaf(serial_num, operation_type)
            SNMerkleTree.insert_leaf(serial_num,operation_area)
        messagebox.showinfo("Data Collected", "Data has been added to Merkle Tree successfully!")


def main():
    app = Application()
    app.mainloop()
