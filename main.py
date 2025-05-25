"""
Entry point for Signature Lifestyle Business Suite
"""
import tkinter as tk
import ttkbootstrap as ttk
from ui.sales import SalesTab 
from ui.inventory import InventoryTab
from ui.dashboard import DashboardTab
from ui.reports import RevenueTrendTab
from auth import AuthManager

class SignatureLifestyleApp:
    def __init__(self):
        self.root = ttk.Window(
            title="Signature Lifestyle Business Suite",
            themename="litera",
            size=(1200, 800),
            resizable=(True, True)
        )
        self.auth = AuthManager()
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Initialize main application interface"""
        if not self.auth.current_user:
            self._show_login()
        else:
            self._show_main_interface()
    
    def _show_login(self) -> None:
        """Display authentication screen"""
        # Login form implementation
        pass
    
    def _show_main_interface(self) -> None:
        """Build the main application after successful login"""
        self.notebook = ttk.Notebook(self.root)
        
        # Add application tabs
        tabs = [
            ("Dashboard", DashboardTab),
            ("Sales", SalesTab),
            ("Inventory", InventoryTab),
            ("Reports", RevenueTrendTab)
        ]
        
        for name, tab_class in tabs:
            self.notebook.add(tab_class(self.notebook), text=name)
        
        self.notebook.pack(expand=True, fill='both')
        self.root.mainloop()

if __name__ == "__main__":
    app = SignatureLifestyleApp()