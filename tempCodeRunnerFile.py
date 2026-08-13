import sqlite3

DB_NAME = "ganesh_mandal.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()

        #  Donation-table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Donations(
        ID_no INTEGER PRIMARY KEY AUTOINCREMENT,
        Donor_name TEXT NOT NULL ,
        phone_number TEXT,
        amount REAL NOT NULL ,
        payment_mode TEXT CHECK(payment_mode IN ('Cash' , 'Online/ Phone pay/ G-pay ', 'UPI' )), 
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP )
        """)

        ## Expenses Table 
        cursor.execute("""CREATE TABLE IF NOT EXISTS Expenses(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        Description TEXT,
        Amount REAL NOT NULL,
        Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP )
        """)

        conn.commit()

def Add_Donation(name ,phone,amount, payment_mode ):
    # Inserting new records into the table 
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()

        cursor.execute(""" INSERT INTO Donations(donar_name,phone_number, amount,payment_mode)
        VALUES (?,?,?,?) """,
        (name, phone, amount, payment_mode))
        return cursor.lastrowid ## addes at last 

def get_all_donations():
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()
        cursor.execute("SELECT ID_no , Donar_name, phone_number, amount, payment_mode,date_added FROM Donistions ORDER BY ID DESC ")
        return cursor.fetchall()


def add_expense(category, descirption ,amount):
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()
        cursor.execute(""" 
        INSERT INTO Expenses(category,description, amount )
        VALUES (?,?,?)""",
        (category,descirption,amount))
        return True

def get_financial_summary():
    ## Calculates total collections , total expenses ,and net balance.
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()

        cursor.execute("SELECT SUM(amount )FROM Donations ")
        total_collections= cursor.fetchone()[0] or 0.0 

        cursor.execute('SELECT SUM(amount )FROM Expemses')
        total_expenses=cursor.fetchone()[0] or 0.0 

        balance=total_collections-total_expenses 
        return total_collections, total_expenses, balance

if __name__== "__main__":
    init_db()
    print("Ganesh mandal Data base Initialized successfully")


