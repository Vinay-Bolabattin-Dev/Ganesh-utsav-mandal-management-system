import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Initialize connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def _read_sheet(worksheet_name):
    """Safely reads a worksheet, trims column whitespace, and handles empty rows."""
    try:
        df = conn.read(worksheet=worksheet_name, ttl=60)
        if df is not None and not df.empty:
            df = df.dropna(how="all")
            # Strip whitespace from all header names
            df.columns = [str(c).strip() for c in df.columns]
            return df
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def _update_sheet(worksheet_name, df):
    """Overwrites the worksheet with updated data and clears read cache."""
    conn.update(worksheet=worksheet_name, data=df)
    st.cache_data.clear()

def init_db():
    pass

def init_dono_master():
    pass

def _find_col(df, candidates):
    """Helper to find first matching column name regardless of minor typos."""
    col_lookup = {str(c).lower().strip(): c for c in df.columns}
    for cand in candidates:
        cand_lower = cand.lower().strip()
        if cand_lower in col_lookup:
            return col_lookup[cand_lower]
        # Partial match if column name was cut off (e.g. 'donor_na' for 'donor_name')
        for k in col_lookup:
            if k.startswith(cand_lower[:6]):
                return col_lookup[k]
    return None

# ==================== DONATIONS ====================
def add_donation(name, phone, amount, payment_mode):
    df = _read_sheet("donations")
    id_col = _find_col(df, ["id"])
    new_id = 1 if (df.empty or not id_col) else int(pd.to_numeric(df[id_col], errors="coerce").max() or 0) + 1
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
    
    id_col = _find_col(df, ["id"]) or "id"
    name_col = _find_col(df, ["donor_name", "name"]) or "donor_name"
    phone_col = _find_col(df, ["phone_number", "phone"]) or "phone_number"
    amt_col = _find_col(df, ["amount"]) or "amount"
    mode_col = _find_col(df, ["payment_mode", "mode"]) or "payment_mode"
    date_col = _find_col(df, ["date_added", "date"]) or "date_added"

    rows = []
    for _, r in df.iterrows():
        r_id = int(pd.to_numeric(r.get(id_col, 0), errors="coerce") or 0)
        r_name = str(r.get(name_col, "") or "")
        r_phone = str(r.get(phone_col, "") or "")
        r_amt = float(pd.to_numeric(r.get(amt_col, 0), errors="coerce") or 0.0)
        r_mode = str(r.get(mode_col, "Cash") or "Cash")
        r_date = str(r.get(date_col, "") or "")
        rows.append([r_id, r_name, r_phone, r_amt, r_mode, r_date])

    rows.sort(key=lambda x: x[0], reverse=True)
    return rows

def delete_donor_record(donation_id):
    df = _read_sheet("donations")
    id_col = _find_col(df, ["id"])
    if not df.empty and id_col:
        df = df[df[id_col].astype(str) != str(donation_id)]
        _update_sheet("donations", df)
    return True

# ==================== EXPENSES ====================
def add_expense(category, description, amount):
    df = _read_sheet("expenses")
    id_col = _find_col(df, ["id"])
    new_id = 1 if (df.empty or not id_col) else int(pd.to_numeric(df[id_col], errors="coerce").max() or 0) + 1
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
    
    id_col = _find_col(df, ["id"]) or "id"
    cat_col = _find_col(df, ["category"]) or "category"
    desc_col = _find_col(df, ["description", "expense_title"]) or "description"
    amt_col = _find_col(df, ["amount"]) or "amount"
    date_col = _find_col(df, ["date_added", "date"]) or "date_added"

    rows = []
    for _, r in df.iterrows():
        r_id = int(pd.to_numeric(r.get(id_col, 0), errors="coerce") or 0)
        r_cat = str(r.get(cat_col, "") or "")
        r_desc = str(r.get(desc_col, "") or "")
        r_amt = float(pd.to_numeric(r.get(amt_col, 0), errors="coerce") or 0.0)
        r_date = str(r.get(date_col, "") or "")
        rows.append([r_id, r_cat, r_desc, r_amt, r_date])

    rows.sort(key=lambda x: x[0], reverse=True)
    return rows

def delete_expense(expense_id):
    df = _read_sheet("expenses")
    id_col = _find_col(df, ["id"])
    if not df.empty and id_col:
        df = df[df[id_col].astype(str) != str(expense_id)]
        _update_sheet("expenses", df)
    return True

# ==================== FINANCIAL SUMMARY ====================
def get_financial_summary():
    donations_df = _read_sheet("donations")
    expenses_df = _read_sheet("expenses")

    d_col = _find_col(donations_df, ["amount"])
    e_col = _find_col(expenses_df, ["amount"])

    total_coll = pd.to_numeric(donations_df[d_col], errors="coerce").sum() if (not donations_df.empty and d_col) else 0.0
    total_exp = pd.to_numeric(expenses_df[e_col], errors="coerce").sum() if (not expenses_df.empty and e_col) else 0.0
    balance = total_coll - total_exp
    return float(total_coll), float(total_exp), float(balance)

# ==================== PENDING DONATIONS ====================
def add_pending_donation(donor_name, phone_number, amount, promised_date, notes=""):
    df = _read_sheet("pending_donations")
    id_col = _find_col(df, ["id"])
    new_id = 1 if (df.empty or not id_col) else int(pd.to_numeric(df[id_col], errors="coerce").max() or 0) + 1
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

    id_col = _find_col(df, ["id"]) or "id"
    name_col = _find_col(df, ["donor_name", "name"]) or "donor_name"
    phone_col = _find_col(df, ["phone_number", "phone"]) or "phone_number"
    amt_col = _find_col(df, ["amount", "expected_amount"]) or "amount"
    date_col = _find_col(df, ["promised_date", "date"]) or "promised_date"
    notes_col = _find_col(df, ["notes", "note"]) or "notes"
    created_col = _find_col(df, ["date_added", "created_at"]) or "date_added"
    status_col = _find_col(df, ["status"])

    rows = []
    for _, r in df.iterrows():
        # Only show pending items if a status column exists
        if status_col:
            st_val = str(r.get(status_col, "Pending")).strip().lower()
            if st_val not in ["pending", "", "nan"]:
                continue

        r_id = int(pd.to_numeric(r.get(id_col, 0), errors="coerce") or 0)
        r_name = str(r.get(name_col, "") or "")
        r_phone = str(r.get(phone_col, "") or "")
        r_amt = float(pd.to_numeric(r.get(amt_col, 0), errors="coerce") or 0.0)
        r_date = str(r.get(date_col, "") or "")
        r_notes = str(r.get(notes_col, "") or "")
        r_created = str(r.get(created_col, "") or "")

        # Exactly 7 items matching app.py p_columns
        rows.append([r_id, r_name, r_phone, r_amt, r_date, r_notes, r_created])

    rows.sort(key=lambda x: x[0], reverse=True)
    return rows

def get_total_pending_amount():
    df = _read_sheet("pending_donations")
    if df.empty:
        return 0.0
    status_col = _find_col(df, ["status"])
    amt_col = _find_col(df, ["amount", "expected_amount"])
    if not amt_col:
        return 0.0

    if status_col:
        mask = df[status_col].astype(str).str.strip().str.lower().isin(["pending", "", "nan"])
        pending_df = df[mask]
    else:
        pending_df = df

    total = pd.to_numeric(pending_df[amt_col], errors="coerce").sum()
    return float(total or 0.0)

def settle_pending_donation(pending_id, payment_mode):
    df_pending = _read_sheet("pending_donations")
    id_col = _find_col(df_pending, ["id"])
    if df_pending.empty or not id_col:
        return None, None, None, None

    match = df_pending[df_pending[id_col].astype(str) == str(pending_id)]
    if not match.empty:
        row = match.iloc[0]
        name_col = _find_col(df_pending, ["donor_name", "name"]) or "donor_name"
        phone_col = _find_col(df_pending, ["phone_number", "phone"]) or "phone_number"
        amt_col = _find_col(df_pending, ["amount", "expected_amount"]) or "amount"

        donor_name = str(row.get(name_col, ""))
        phone = str(row.get(phone_col, ""))
        amount = float(pd.to_numeric(row.get(amt_col, 0), errors="coerce") or 0.0)

        receipt_id = add_donation(donor_name, phone, amount, payment_mode)
        df_pending = df_pending[df_pending[id_col].astype(str) != str(pending_id)]
        _update_sheet("pending_donations", df_pending)
        return receipt_id, donor_name, phone, amount

    return None, None, None, None

def delete_pending_donation(pending_id):
    df = _read_sheet("pending_donations")
    id_col = _find_col(df, ["id"])
    if not df.empty and id_col:
        df = df[df[id_col].astype(str) != str(pending_id)]
        _update_sheet("pending_donations", df)
    return True

# ==================== MASTER DONORS ====================
def get_all_master_donor():
    df = _read_sheet("previous_donors")
    if df.empty:
        return []

    id_col = _find_col(df, ["id"]) or df.columns[0]
    name_col = _find_col(df, ["donor_name", "name"]) or (df.columns[1] if len(df.columns) > 1 else id_col)
    phone_col = _find_col(df, ["phone_number", "phone"]) or (df.columns[2] if len(df.columns) > 2 else name_col)
    amt_col = _find_col(df, ["last_year_amount", "amount"]) or (df.columns[3] if len(df.columns) > 3 else phone_col)

    rows = []
    for _, r in df.iterrows():
        r_id = int(pd.to_numeric(r.get(id_col, 0), errors="coerce") or 0)
        r_name = str(r.get(name_col, "") or "")
        r_phone = str(r.get(phone_col, "") or "")
        r_amt = float(pd.to_numeric(r.get(amt_col, 0), errors="coerce") or 0.0)
        # Exactly 4 elements matching Tab 5 columns in app.py
        rows.append([r_id, r_name, r_phone, r_amt])

    rows.sort(key=lambda x: str(x[1]).lower())
    return rows

def search_master_donors(query_text):
    all_donors = get_all_master_donor()
    if not query_text or not str(query_text).strip():
        return all_donors
    q = str(query_text).strip().lower()
    return [d for d in all_donors if q in str(d[1]).lower() or q in str(d[2])]