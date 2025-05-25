import tkinter as tk
from tkinter import ttk
from database import db

class InventoryTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        # Title
        ttk.Label(self, text="Inventory Management", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        # Inventory Table
        columns = ("ID", "Name", "Quantity", "Price")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Load initial data
        self._load_inventory()
    
    def _load_inventory(self):
        """Fetch and display inventory from database"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get data from database
        inventory = db.execute_query("SELECT id, name, quantity, selling_price FROM products")
        
        # Insert into table
        for item in inventory:
            self.tree.insert("", tk.END, values=item)