import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Initialize connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def _read_sheet(worksheet_name):
    """Safely reads a worksheet, drops empty rows, and surfaces errors."""
    try:
        df = conn.read(worksheet=worksheet_name, ttl="1s")
        if df is not None and not df.empty:
            return df.dropna(how="all")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error reading tab '{worksheet_name}': {e}")
        return pd.DataFrame()

def _update_sheet(worksheet_name, df):
    """Overwrites the worksheet with updated data and clears read cache."""
    conn.update(worksheet=worksheet_name, data=df)
    st.cache_data.clear()

def init_db():
    """No-op for compatibility with app.py startup calls."""
    pass

def init_dono_master():
    """No-op for compatibility with app.py startup calls."""
    pass

# ==================== DONATIONS ====================
def add_donation(name, phone, amount, payment_mode):
    df = _read_sheet("donations")
    new_id = 1 if df.empty else int(pd.to_numeric(df["id"], errors="coerce").max() or 0) + 1
    new_row = pd.DataFrame([{
        "id": new_id,
        "donor_name": name,
        "phone_number": str(phone) if phone else "",
        "amount": float(amount),
        "payment_mode": payment_mode,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    updated_df = pd.concat([df, new_row], ignore_index=True)
    _update_sheet("donations", updated_df)
    return new_id

def get_all_donations():
    df = _read_sheet("donations")
    if df.empty:
        return []
    df = df.sort_values(by="id", ascending=False)
    return df[["id", "donor_name", "phone_number", "amount", "payment_mode", "date_added"]].values.tolist()

def delete_donor_record(donation_id):
    df = _read_sheet("donations")
    if not df.empty:
        df = df[df["id"].astype(str) != str(donation_id)]
        _update_sheet("donations", df)
    return True

# ==================== EXPENSES ====================
def add_expense(category, description, amount):
    df = _read_sheet("expenses")
    new_id = 1 if df.empty else int(pd.to_numeric(df["id"], errors="coerce").max() or 0) + 1
    new_row = pd.DataFrame([{
        "id": new_id,
        "category": category,
        "description": description,
        "amount": float(amount),
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    updated_df = pd.concat([df, new_row], ignore_index=True)
    _update_sheet("expenses", updated_df)
    return True

def get_all_expenses():
    df = _read_sheet("expenses")
    if df.empty:
        return []
    df = df.sort_values(by="id", ascending=False)
    return df[["id", "category", "description", "amount", "date_added"]].values.tolist()

def delete_expense(expense_id):
    df = _read_sheet("expenses")
    if not df.empty:
        df = df[df["id"].astype(str) != str(expense_id)]
        _update_sheet("expenses", df)
    return True

# ==================== FINANCIAL SUMMARY ====================
def get_financial_summary():
    donations_df = _read_sheet("donations")
    expenses_df = _read_sheet("expenses")

    total_coll = pd.to_numeric(donations_df["amount"], errors="coerce").sum() if not donations_df.empty else 0.0
    total_exp = pd.to_numeric(expenses_df["amount"], errors="coerce").sum() if not expenses_df.empty else 0.0
    balance = total_coll - total_exp
    return float(total_coll), float(total_exp), float(balance)

# ==================== PENDING DONATIONS ====================
def add_pending_donation(donor_name, phone_number, amount, promised_date, notes=""):
    df = _read_sheet("pending_donations")
    new_id = 1 if df.empty else int(pd.to_numeric(df["id"], errors="coerce").max() or 0) + 1
    new_row = pd.DataFrame([{
        "id": new_id,
        "donor_name": donor_name,
        "phone_number": str(phone_number) if phone_number else "",
        "amount": float(amount),
        "promised_date": str(promised_date),
        "notes": notes,
        "status": "Pending",
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    updated_df = pd.concat([df, new_row], ignore_index=True)
    _update_sheet("pending_donations", updated_df)
    return new_id

def get_all_pending_donations():
    df = _read_sheet("pending_donations")
    if df.empty:
        return []
    df = df[df["status"] == "Pending"].sort_values(by="id", ascending=False)
    return df[["id", "donor_name", "phone_number", "amount", "promised_date", "notes", "date_added"]].values.tolist()

def get_total_pending_amount():
    df = _read_sheet("pending_donations")
    if df.empty:
        return 0.0
    pending_df = df[df["status"] == "Pending"]
    total = pd.to_numeric(pending_df["amount"], errors="coerce").sum()
    return float(total or 0.0)

def settle_pending_donation(pending_id, payment_mode):
    df_pending = _read_sheet("pending_donations")
    if df_pending.empty:
        return None, None, None, None

    match = df_pending[df_pending["id"].astype(str) == str(pending_id)]
    if not match.empty:
        row = match.iloc[0]
        donor_name = row["donor_name"]
        phone = row["phone_number"]
        amount = float(row["amount"])

        # Add to donations sheet
        receipt_id = add_donation(donor_name, phone, amount, payment_mode)

        # Remove from pending donations sheet
        df_pending = df_pending[df_pending["id"].astype(str) != str(pending_id)]
        _update_sheet("pending_donations", df_pending)
        return receipt_id, donor_name, phone, amount

    return None, None, None, None

def delete_pending_donation(pending_id):
    df = _read_sheet("pending_donations")
    if not df.empty:
        df = df[df["id"].astype(str) != str(pending_id)]
        _update_sheet("pending_donations", df)
    return True

# ==================== MASTER DONORS ====================
def get_all_master_donor():
    df = _read_sheet("previous_donors")
    if df.empty:
        return []
    df = df.sort_values(by="donor_name", ascending=True)
    return df[["id", "donor_name", "phone_number", "last_year_amount"]].values.tolist()

def search_master_donors(query_text):
    df = _read_sheet("previous_donors")
    if df.empty or not query_text.strip():
        return []
    q = query_text.strip().lower()
    matched = df[df["donor_name"].str.lower().str.contains(q, na=False)]
    return matched[["id", "donor_name", "phone_number", "last_year_amount"]].values.tolist()