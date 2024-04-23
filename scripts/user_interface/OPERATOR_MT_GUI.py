import tkinter as tk
from tkinter import ttk, messagebox
from .merkle_tree import SNMerkleTree

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input Operator")
        self.geometry("200x200")
        
        # Operator Number
        self.operator_label = ttk.Label(self, text="Input Operator Number")
        self.operator_label.pack(padx=10, pady=5)
        
        self.operator_entry = ttk.Entry(self)
        self.operator_entry.pack(padx=10, pady=5)

        # Submit button
        self.submit_button = ttk.Button(self, text="Submit", command=self.collect_data)
        self.submit_button.pack(pady=20)


    def collect_data(self):
        operator_num = self.operator_entry.get()


        SNMerkleTree.insert_leaf(operator_num,"Operator")

        messagebox.showinfo("Data Collected", "Data has been added to Merkle Tree successfully!")


def main():
    app = Application()
    app.mainloop()
