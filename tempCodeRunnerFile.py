import sqlite3

DB_NAME = "ganesh_utsav_mandal.db"

def init_db():
    """Initializes the database tables."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Donations Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT NOT NULL,
            phone_number TEXT,
            amount REAL NOT NULL,
            payment_mode TEXT CHECK(payment_mode IN ('Cash', 'UPI', 'Bank Transfer')),
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Expenses Table 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()

def add_donation(name, phone, amount, payment_mode):
    """Inserts a new donation record and returns receipt ID."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO donations (donor_name, phone_number, amount, payment_mode)
        VALUES (?, ?, ?, ?)
        """, (name, phone, amount, payment_mode))
        conn.commit()
        return cursor.lastrowid

def get_all_donations():
    """Fetches all donation records ordered by newest first."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, donor_name, phone_number, amount, payment_mode, date_added 
        FROM donations 
        ORDER BY id DESC
        """)
        return cursor.fetchall()

def add_expense(category, description, amount):
    """Inserts a new Mandal expense record."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO expenses (category, description, amount)
        VALUES (?, ?, ?)
        """, (category, description, amount))
        conn.commit()
        return True

def get_financial_summary():
    """Calculates total collections, total expenses, and net balance."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(amount) FROM donations")
        total_collections = cursor.fetchone()[0] or 0.0

        cursor.execute("SELECT SUM(amount) FROM expenses")
        total_expenses = cursor.fetchone()[0] or 0.0

        balance = total_collections - total_expenses
        return total_collections, total_expenses, balance

def get_all_expenses():
    """Fetches all expense records ordered by newest first."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, category, description, amount, date_added 
        FROM expenses 
        ORDER BY id DESC
        """)
        return cursor.fetchall()

if __name__ == "__main__":
    init_db()
    print("Ganesh Mandal Database Initialized successfully!")

