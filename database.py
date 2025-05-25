"""
SQLite database operations for Signature Lifestyle
Handles all data persistence with proper error handling
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "data/signature.db"):
        """Initialize database connection and ensure tables exist"""
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self) -> None:
        """Create required tables if they don't exist"""
        tables = {
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT CHECK(role IN ('owner', 'manager', 'employee')) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "products": """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    quantity INTEGER DEFAULT 0,
                    purchase_price REAL,
                    selling_price REAL,
                    threshold INTEGER DEFAULT 5,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "sales": """
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER REFERENCES products(id),
                    quantity INTEGER NOT NULL,
                    sale_price REAL NOT NULL,
                    payment_mode TEXT CHECK(payment_mode IN ('cash', 'bkash', 'nagad', 'card')),
                    sale_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
        }
        
        with self.conn:
            cursor = self.conn.cursor()
            for table_name, schema in tables.items():
                cursor.execute(schema)
            
            # Insert default admin user if none exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE role='owner'")
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("admin", "admin123", "owner")
                )
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Generic query executor with error handling"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            
            if cursor.description:  # For SELECT queries
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            return []
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

# Initialize global DB instance
db = DatabaseManager()