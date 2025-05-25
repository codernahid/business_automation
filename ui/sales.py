# ui/sales.py
import tkinter as tk
from tkinter import ttk
from database import db

class SalesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        ttk.Label(self, text="Sales Management").pack(pady=10)
        
        # Add your sales entry form here
        self.product_entry = ttk.Entry(self)
        self.product_entry.pack()
        
        ttk.Button(self, text="Record Sale", command=self._record_sale).pack()

    def _record_sale(self):
        print("Sale recorded!")  # Replace with actual logic