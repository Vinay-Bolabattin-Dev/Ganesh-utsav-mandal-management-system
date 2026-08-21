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

        # Pending table 
        cursor.execute("""
        CREATE  TABLE IF NOT EXISTS pending_donations(
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        donor_name TEXT NOT NULL,
        phone_number TEXT ,
        amount REAL NOT NULL ,
        promised_date TEXT,
        notes TEXT ,
        status TEXT DEFAULT 'Pending',
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP )
        """)
        conn.commit()
    init_dono_master()

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

def add_pending_donation(donor_name, phone_number, amount,promised_date , notes=""):
    ## Initalizes the pending donations table. 
    with sqlite3.connect(DB_NAME)as conn :
        cursor=conn.cursor()
        cursor.execute(""" 
        INSERT INTO pending_donations (donor_name , phone_number ,amount , promised_date , notes)
        VALUES (?,?,?,?,? ) 
        """, (donor_name, phone_number, amount,promised_date , notes))
        conn.commit()
        return cursor.lastrowid


def get_all_pending_donations():
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()
        cursor.execute("""
        SELECT id, donor_name,phone_number, amount, promised_date, notes, date_added
        FROM pending_donations
        WHERE status ='Pending'
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



def settle_pending_donation(pending_id, payment_mode):
    ## Moves a pending pledge to the confirmed donation table 
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()
        cursor.execute("SELECT donor_name ,phone_number,amount FROM pending_donations WHERE id=?", (pending_id,))
        records=cursor.fetchone()

        if records:
            donor_name ,phone ,amount = records
            cursor.execute("""
            INSERT INTO donations(donor_name, phone_number,amount,payment_mode)
            VALUES (?,?,?,?)
            """, (donor_name,phone ,amount,payment_mode)) 
            receipt_id=cursor.lastrowid
            cursor.execute("DELETE FROM pending_donations WHERE id =?" ,(pending_id,))
            conn.commit()
            return receipt_id, donor_name ,phone ,amount 
        return None,None,None, None

def delete_pending_donation(pending_id):
    ##Deletes a pending entry by ID.
    with sqlite3.connect(DB_NAME)as conn:
        cursor =conn.cursor()
        cursor.execute("DELETE FROM pending_donations WHERE id=?",(pending_id,))
        conn.commit()
        return True


##============ Previous year Donor List =======
def init_dono_master():
    ## initialises the previous year master donors table 
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS previous_donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_name TEXT NOT NULL,
        phone_number TEXT DEFAULT '' ,
        last_year_amount REAL  DEFAULT 0.0
        )
        """)
        conn.commit()


def add_master_donor_bulk(donor_tuples):
    with sqlite3.connect(DB_NAME) as conn:
        """ Inserts multiple master donor records at once.
        donor_tuples format [ ('Donor_name' , ' phone or blank ', amount), ....]"""

        cursor=conn.cursor()
        cursor.executemany(""" 
        INSERT INTO previous_donors(donor_name , phone_number , last_year_amount) VALUES(?,?,?)
        """, donor_tuples)
        conn.commit()
        return True 

def get_all_master_donor():
    ## Fetchas all previous year donor records alphabetically.
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()
        cursor.execute(""" 
        SELECT id , donor_name, phone_number , last_year_amount
        FROM  previous_donors
        ORDER BY donor_name ASC 
        """)
        return cursor.fetchall()


def search_master_donors(query_text):
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()
        cursor.execute(""" 
        SELECT id , donor_name ,phone_number, last_year_amount
        FROM previous_donors 
        WHERE donor_name LIKE ?
        ORDER BY donor_name ASC  
        """ , (f"%{query_text.strip()}%", ))
        return cursor.fetchall()

if __name__ == "__main__":
    init_db()
    print("Ganesh Mandal Database Initialized successfully!")


#"""============ PREVIOUS YEAR DONOR MASTER ============"""
def init_dono_master():
    """Initializes and auto-seeds the previous year master donors table if empty."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS previous_donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT NOT NULL,
            phone_number TEXT DEFAULT '',
            last_year_amount REAL DEFAULT 0.0
        )
        """)
        conn.commit()

        # Check if table is empty, auto-seed if needed
        cursor.execute("SELECT COUNT(*) FROM previous_donors")
        count = cursor.fetchone()[0]
        
        if count == 0:
            default_donors = [
                ("अशोक बोद्धूल | Ashok Boddhul", "", 751.0),
                ("पद्मावती हॉटेल | Padmavati Hotel", "", 201.0),
                ("अनिल कस्तुरी | Anil Kasturi", "", 601.0),
                ("कुमार हेअर स्टाईल | Kumar Hair Style", "", 501.0),
                ("यल्लप्पा बोल्ली | Yallappa Bolli", "", 2100.0),
                ("महेश माशेट्टी | Mahesh Mashetti", "", 251.0),
                ("राकेश नोरा | Rakesh Nora", "", 501.0),
                ("गणेश श्रीगिरी | Ganesh Shrigiri", "", 501.0),
                ("झोड्डू | Zoddu", "", 501.0),
                ("नरेश केंडीकटला | Naresh Kendikatla", "", 1100.0),
                ("सुरज ईराबत्ती | Suraj Irabatti", "", 1001.0),
                ("बोल्ली | Bolli", "", 2001.0),
                ("गणेश मेकॅनिकल | Ganesh Mechanical", "", 1200.0),
                ("राम गुंडेली (सभासद) | Ram Gundeli", "", 1001.0),
                ("संतोष दासरी (सभासद) | Santosh Dasari", "", 1001.0),
                ("अंबादास अलवाल (सभासद) | Ambadas Alwal", "", 1001.0),
                ("रोहित दासरी (सभासद) | Rohit Dasari", "", 1001.0),
                ("प्रसाद मोदास (सभासद) | Prasad Modas", "", 1001.0),
                ("गोपी गाजूल (सभासद) | Gopi Gajul", "", 500.0),
                ("राम दासरी (सभासद) | Ram Dasari", "", 1001.0),
                ("अभय हिबारे (सभासद) | Abhay Hibare", "", 1001.0),
                ("श्रीकांत गेट्याल | Shrikant Getyal", "", 2501.0),
                ("साई कलेक्शन | Sai Collection", "", 151.0),
                ("ओम कोल्ड्रिंक्स | Om Coldrinks", "", 101.0),
                ("जय भवानी स्वीट्स | Jay Bhavani Sweets", "", 851.0),
                ("मुलचंद मिठाई | Mulchand Mithai", "", 301.0),
                ("सत्तरया ईराबत्ती | Sattaraya Irabatti", "", 1001.0),
                ("श्रीनिवास आडम | Shrinivas Adam", "", 701.0),
                ("सुर्का कृष्णा | Surka Krishna", "", 301.0),
                ("अभय टेक्स | Abhay Tex", "", 1001.0),
                ("नरसय्या बोलाबत्तीन | Narsayya Bolabattin", "", 501.0),
                ("चक दे दाल | Chak De Dal", "", 501.0),
                ("लंगर बिडी कंपनी | Langar Bidi Company", "", 1501.0),
                ("पुष्पा टेक्स्टाईल | Pushpa Textile", "", 701.0),
                ("व्ही. के. जी वाईन्स | VKG Wines", "", 1501.0),
                ("नरसय्या अचली | Narsayya Achali", "", 1101.0),
                ("वैभव क्रिएशन | Vaibhav Creation", "", 1001.0),
                ("शरद दुडम | Sharad Dudam", "", 1101.0),
                ("अंकिता टेक्स (कंदोब्बे) | Ankita Tex Kandobbe", "", 1101.0),
                ("शिवकुमार यम्ला | Shivkumar Yamla", "", 501.0),
                ("बिर्रु मालक | Birru Malak", "", 1501.0),
                ("आदित्य टेक्स स्टोअर्स (संगीता) | Aditya Tex Stores Sangita", "", 5001.0),
                ("माशेट्टी | Mashetti", "", 50001.0),
                ("सत्यनारायण गुंडेली | Satyanarayan Gundeli", "", 1501.0),
                ("रवी दुडम | Ravi Dudam", "", 501.0),
                ("विश्वनाथ तुम्मा | Vishwanath Tumma", "", 2011.0),
                ("बालाजी धोता | Balaji Dhota", "", 2011.0),
                ("दिनेश येलगेटी | Dinesh Yelgeti", "", 3011.0),
                ("आनंद टेलर | Anand Tailor", "", 651.0),
                ("रोहित फ्लॉवर | Rohit Flower", "", 1001.0),
                ("पद्मावती टी हाऊस | Padmavati Tea House", "", 601.0)
            ]
            cursor.executemany(""" 
            INSERT INTO previous_donors(donor_name, phone_number, last_year_amount) 
            VALUES (?, ?, ?)
            """, default_donors)
            conn.commit()
