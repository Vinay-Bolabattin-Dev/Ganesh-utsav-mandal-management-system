import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Initialize connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def _read_sheet(worksheet_name):
    """Safely reads a worksheet with caching and strips column whitespace."""
    try:
        df = conn.read(worksheet=worksheet_name, ttl=60)
        if df is not None and not df.empty:
            df = df.dropna(how="all")
            # Strip accidental whitespace from all column names
            df.columns = [str(col).strip() for col in df.columns]
            return df
        return pd.DataFrame()
    except Exception as e:
        st.warning(f"Sheets sync in progress for '{worksheet_name}'. Please wait a moment...")
        return pd.DataFrame()

def _update_sheet(worksheet_name, df):
    """Overwrites the worksheet with updated data and clears read cache."""
    conn.update(worksheet=worksheet_name, data=df)
    st.cache_data.clear()

def init_db():
    pass

def init_dono_master():
    pass

# Helper to safely retrieve columns regardless of exact naming
def _get_col_value(df, candidate_names, default=""):
    for name in candidate_names:
        if name in df.columns:
            return df[name]
    return default

# ==================== DONATIONS ====================
def add_donation(name, phone, amount, payment_mode):
    df = _read_sheet("donations")
    new_id = 1 if df.empty or "id" not in df.columns else int(pd.to_numeric(df["id"], errors="coerce").max() or 0) + 1
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
    
    # Harmonize column names
    col_map = {
        "id": _get_col_value(df, ["id"], ""),
        "donor_name": _get_col_value(df, ["donor_name", "donor_na", "name"], ""),
        "phone_number": _get_col_value(df, ["phone_number", "phone_nu", "phone"], ""),
        "amount": _get_col_value(df, ["amount"], 0),
        "payment_mode": _get_col_value(df, ["payment_mode", "mode"], "Cash"),
        "date_added": _get_col_value(df, ["date_added", "date"], "")
    }
    clean_df = pd.DataFrame(col_map)
    clean_df = clean_df.sort_values(by="id", ascending=False)
    return clean_df[["id", "donor_name", "phone_number", "amount", "payment_mode", "date_added"]].values.tolist()

def delete_donor_record(donation_id):
    df = _read_sheet("donations")
    if not df.empty and "id" in df.columns:
        df = df[df["id"].astype(str) != str(donation_id)]
        _update_sheet("donations", df)
    return True

# ==================== EXPENSES ====================
def add_expense(category, description, amount):
    df = _read_sheet("expenses")
    new_id = 1 if df.empty or "id" not in df.columns else int(pd.to_numeric(df["id"], errors="coerce").max() or 0) + 1
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
    
    col_map = {
        "id": _get_col_value(df, ["id"], ""),
        "category": _get_col_value(df, ["category"], ""),
        "description": _get_col_value(df, ["description", "expense_title", "title"], ""),
        "amount": _get_col_value(df, ["amount"], 0),
        "date_added": _get_col_value(df, ["date_added", "date"], "")
    }
    clean_df = pd.DataFrame(col_map)
    clean_df = clean_df.sort_values(by="id", ascending=False)
    return clean_df[["id", "category", "description", "amount", "date_added"]].values.tolist()

def delete_expense(expense_id):
    df = _read_sheet("expenses")
    if not df.empty and "id" in df.columns:
        df = df[df["id"].astype(str) != str(expense_id)]
        _update_sheet("expenses", df)
    return True

# ==================== FINANCIAL SUMMARY ====================
def get_financial_summary():
    donations_df = _read_sheet("donations")
    expenses_df = _read_sheet("expenses")

    d_amt = _get_col_value(donations_df, ["amount"], 0) if not donations_df.empty else 0
    e_amt = _get_col_value(expenses_df, ["amount"], 0) if not expenses_df.empty else 0

    total_coll = pd.to_numeric(d_amt, errors="coerce").sum() if not donations_df.empty else 0.0
    total_exp = pd.to_numeric(e_amt, errors="coerce").sum() if not expenses_df.empty else 0.0
    balance = total_coll - total_exp
    return float(total_coll), float(total_exp), float(balance)

# ==================== PENDING DONATIONS ====================
def add_pending_donation(donor_name, phone_number, amount, promised_date, notes=""):
    df = _read_sheet("pending_donations")
    new_id = 1 if df.empty or "id" not in df.columns else int(pd.to_numeric(df["id"], errors="coerce").max() or 0) + 1
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
    
    # Check if a status column exists; if it does, show Pending or blanks
    if "status" in df.columns:
        status_series = df["status"].astype(str).str.strip().str.lower()
        is_pending = status_series.isin(["pending", "", "nan", "none"])
        filtered_df = df[is_pending]
    else:
        filtered_df = df

    if filtered_df.empty:
        filtered_df = df  # fallback so records always show

    col_map = {
        "id": _get_col_value(filtered_df, ["id"], 1),
        "donor_name": _get_col_value(filtered_df, ["donor_name", "donor_na", "name"], ""),
        "phone_number": _get_col_value(filtered_df, ["phone_number", "phone_nu", "phone"], ""),
        "amount": _get_col_value(filtered_df, ["amount", "expected_amount"], 0),
        "promised_date": _get_col_value(filtered_df, ["promised_date", "date_promised", "date_added"], ""),
        "notes": _get_col_value(filtered_df, ["notes", "note"], ""),
        "date_added": _get_col_value(filtered_df, ["date_added", "date"], "")
    }
    clean_df = pd.DataFrame(col_map)
    clean_df["id"] = pd.to_numeric(clean_df["id"], errors="coerce").fillna(0)
    clean_df = clean_df.sort_values(by="id", ascending=False)
    return clean_df[["id", "donor_name", "phone_number", "amount", "promised_date", "notes", "date_added"]].fillna("").values.tolist()

def get_total_pending_amount():
    df = _read_sheet("pending_donations")
    if df.empty:
        return 0.0
    status_col = _get_col_value(df, ["status"], "Pending")
    is_pending = status_col.astype(str).str.strip().str.lower() == "pending"
    pending_df = df[is_pending]
    amt_col = _get_col_value(pending_df, ["amount", "expected_amount"], 0)
    total = pd.to_numeric(amt_col, errors="coerce").sum()
    return float(total or 0.0)

def settle_pending_donation(pending_id, payment_mode):
    df_pending = _read_sheet("pending_donations")
    if df_pending.empty or "id" not in df_pending.columns:
        return None, None, None, None

    match = df_pending[df_pending["id"].astype(str) == str(pending_id)]
    if not match.empty:
        row = match.iloc[0]
        donor_name = row.get("donor_name", row.get("donor_na", ""))
        phone = row.get("phone_number", row.get("phone_nu", ""))
        amt_val = row.get("amount", row.get("expected_amount", 0))
        amount = float(amt_val)

        # Add to donations sheet
        receipt_id = add_donation(donor_name, phone, amount, payment_mode)

        # Remove from pending donations sheet
        df_pending = df_pending[df_pending["id"].astype(str) != str(pending_id)]
        _update_sheet("pending_donations", df_pending)
        return receipt_id, donor_name, phone, amount

    return None, None, None, None

def delete_pending_donation(pending_id):
    df = _read_sheet("pending_donations")
    if not df.empty and "id" in df.columns:
        df = df[df["id"].astype(str) != str(pending_id)]
        _update_sheet("pending_donations", df)
    return True

# ==================== MASTER DONORS ====================
def get_all_master_donor():
    df = _read_sheet("previous_donors")
    if df.empty:
        return []
    
    col_map = {
        "id": _get_col_value(df, ["id"], ""),
        "donor_name": _get_col_value(df, ["donor_name", "donor_na", "name"], ""),
        "phone_number": _get_col_value(df, ["phone_number", "phone_nu", "phone"], ""),
        "last_year_amount": _get_col_value(df, ["last_year_amount", "amount", "last_year"], 0)
    }
    clean_df = pd.DataFrame(col_map)
    clean_df["donor_name"] = clean_df["donor_name"].astype(str)
    clean_df = clean_df.sort_values(by="donor_name", ascending=True)
    return clean_df[["id", "donor_name", "phone_number", "last_year_amount"]].fillna("").values.tolist()

def search_master_donors(query_text):
    df = _read_sheet("previous_donors")
    if df.empty or not query_text.strip():
        return []
    
    col_map = {
        "id": _get_col_value(df, ["id"], ""),
        "donor_name": _get_col_value(df, ["donor_name", "donor_na", "name"], ""),
        "phone_number": _get_col_value(df, ["phone_number", "phone_nu", "phone"], ""),
        "last_year_amount": _get_col_value(df, ["last_year_amount", "amount", "last_year"], 0)
    }
    clean_df = pd.DataFrame(col_map)
    q = query_text.strip().lower()
    matched = clean_df[clean_df["donor_name"].astype(str).str.lower().str.contains(q, na=False)]
    return matched[["id", "donor_name", "phone_number", "last_year_amount"]].fillna("").values.tolist()