"""
Interactive revenue trend visualization with time period selection
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from database import db

class RevenueTrendTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Initialize all UI components"""
        # Time period selection
        self.period_var = tk.StringVar(value="month")
        periods = ttk.Combobox(
            self,
            textvariable=self.period_var,
            values=["day", "week", "month", "year"],
            state="readonly"
        )
        periods.pack(pady=10)
        periods.bind("<<ComboboxSelected>>", lambda _: self._update_graph())
        
        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Summary panel
        self.summary_label = ttk.Label(self, wraplength=600)
        self.summary_label.pack(pady=10)
        
        self._update_graph()  # Initial render
    
    def _update_graph(self) -> None:
        """Refresh graph based on selected time period"""
        period = self.period_var.get()
        data = self._fetch_data(period)
        
        self.ax.clear()
        
        if period == "day":
            data.plot(x='date', y='revenue', ax=self.ax, style='o-', color='#2E86AB')
            self.ax.set_title("Daily Revenue Trend")
        elif period == "week":
            data.plot.bar(x='week', y='revenue', ax=self.ax, color='#4CAF50')
            self.ax.set_title("Weekly Revenue Comparison")
        elif period == "month":
            data.plot.area(x='month', y='revenue', ax=self.ax, color='#FF9800')
            self.ax.set_title("Monthly Revenue Analysis")
        else:  # year
            data.plot.line(x='year', y='revenue', ax=self.ax, marker='o', color='#9C27B0')
            self.ax.set_title("Annual Revenue Growth")
        
        self.ax.grid(True)
        self.canvas.draw()
        self._update_summary(data, period)
    
    def _fetch_data(self, period: str) -> pd.DataFrame:
        """Retrieve and aggregate revenue data from database"""
        queries = {
            "day": """
                SELECT date(sale_time) as date, 
                       SUM(quantity * sale_price) as revenue
                FROM sales
                GROUP BY date
                ORDER BY date
            """,
            "month": """
                SELECT strftime('%Y-%m', sale_time) as month,
                       SUM(quantity * sale_price) as revenue
                FROM sales
                GROUP BY month
                ORDER BY month
            """
            # Add week/year queries similarly
        }
        return pd.read_sql(queries[period], db.conn)
    
    def _update_summary(self, data: pd.DataFrame, period: str) -> None:
        """Generate performance insights"""
        if data.empty:
            self.summary_label.config(text="No data available")
            return
        
        latest = data.iloc[-1]
        avg = data['revenue'].mean()
        peak = data['revenue'].max()
        
        text = [
            f"Latest {period}: ${latest['revenue']:,.2f}",
            f"Average: ${avg:,.2f}",
            f"Peak: ${peak:,.2f}"
        ]
        
        if len(data) > 1:
            change = ((latest['revenue'] - data.iloc[-2]['revenue']) / 
                    data.iloc[-2]['revenue']) * 100
            text.append(f"Trend: {'↑' if change > 0 else '↓'} {abs(change):.1f}%")
        
        self.summary_label.config(text="\n".join(text))