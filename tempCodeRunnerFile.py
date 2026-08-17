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
"""-------- DONATIONS SESSION-------"""
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

def delete_donor_record(donation_id):
    ## delete Donation by ID
    with sqlite3.connect(DB_NAME)as conn:
        cursor=conn.cursor()
        cursor.execute("DELETE FROM donations WHERE id=?", (donation_id,))
        conn.commit()
        return True
""" ---------- EXPENSE SESSION --------"""
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

def delete_expense(expense_id):
    """Deletes an expense record by its ID."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        return True
    
"""------- FINANCIAL_SUMMARY SESSION-------"""
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
    


"""============= All Pending Donation / list ============ """

def add_pending_table(donor_name, phone_number, amount,promised_date , notes=""):
    ## Initalizes the pending donations table. 
    with sqlite3.connect(DB_NAME)as conn :
        cursor=conn.cursor()
        cursor.execute(""" 
        INSERT INTO pending_donations (donor_name , phone_nubmer ,amount , promised_date , notes)
        VALUES (?,?,?,?,? ) 
        """, (donor_name, phone_number, amount,promised_date , notes))
        conn.commit()
        return cursor.lastrowid


def get_all_pending_donations():
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()
        cursor.execute("""
        SELECT id, donor_name,phone_number, amount, promised_date, notes, data-added
        FROM pending_donations
        WHERE stastus ='Pending'
        ORDER BY id DESC
        """)
        return cursor.fetchall()

def get_total_pending_amount():
    ## calculates total pending pledged amount 
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()
        cursor.execute(" SELECT SUM(amount ) FROM pending_donations WHERE status  = 'Pending' ")
        total=cursor.fetchone()[0]
        return total or 0.0








if __name__ == "__main__":
    init_db()
    print("Ganesh Mandal Database Initialized successfully!")