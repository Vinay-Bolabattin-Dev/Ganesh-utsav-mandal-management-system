import streamlit as st
import pandas as pd
import database as db



st.set_page_config(page_title= "श्री स्वामी समर्थ मित्र मंडळ", layout='wide')

st.title("श्री स्वामी समर्थ मित्र मंडळ ")
st.write("सार्वजनिक गणेश उत्सव मंडळ")

total_coll , total_exp , balance = db.get_financial_summary() ## calling function from database.py

col1,col2,col3=st.columns(3)
col1.metric(label="एकूण वर्गणी (Collection)", value =f"₹{total_coll:,.2f}")
col2.metric(label="एकूण खर्च (Expenses)", value=f"₹{total_exp:,.2f}")
col3.metric(label="शिल्लक रक्कम (Remaining Balance)", value=f"₹{balance:,.2f}")

st.write("----")

#navigation tables 
tab1, tab2, tab3=st.tabs(["वर्गणी पावती (Collect Vargani)", "📋 सर्व नोंदी (All Records)", "💸 खर्च नोंद (Expenses)"])

with tab1:
    st.subheader("नवीन वर्गणी पावती फाडा (New Donation Receipt)")

    with st.form("donation_form" ,clear_on_submit=True):
        donor_name=st.text_input("(भक्ताचे / देणगीदाराचे नाव (Donor Name) *")
        phone_number=st.text_input("मोबाईल नंबर (Phone Number)")
        amount=st.number_input("वर्गणी रक्कम (Amount in ₹) *", min_value=0.0,step=50.0)
        payment_mode=st.selectbox("पैसे देण्याची पद्धत (Payment Mode)",['Cash', 'UPI', 'Bank Transfer'])


        submitted= st.form_submit_button("पावती तयार करा (Generate Receipt)")


        if submitted:
            if donor_name.strip():
                # Call database function to save record
                receipt_id = db.add_donation(donor_name, phone_number, amount, payment_mode)
                st.balloons()
                st.success(f" वर्गणी यशस्वीरीत्या जमा झाली! पावती क्रमांक: #{receipt_id}")
                st.info(f"देणगीदार: {donor_name} | रक्कम: ₹{amount:,.2f} | पद्धत: {payment_mode}")
            else:
                st.error("कृपया देणगीदाराचे नाव टाका (Please enter donor name)!")


with tab2:
    st.subheader("📋 जमा वर्गणी यादी (All Donation Records)")
    
    records = db.get_all_donations()
    
    if records:
        columns = ["पावती क्र. (ID)", "भक्ताचे/देणगीदाराचे  नाव (Name)", "मोबाईल (Phone)", "रक्कम (₹)", "पद्धत (Mode)", "तारीख (Date & Time)"]
        df = pd.DataFrame(records, columns=columns)

        df.insert(0, "अनुक्रमांक (Sr. No.)", range(1, len(df) + 1))
        # Display table
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("अजून कोणतीही वर्गणी जमा झालेली नाही (No donations recorded yet).")


with tab3:
    st.subheader("💸 मंडळाचा खर्च नोंदवा (Record Mandal Expense)")
    
    with st.form("expense_form", clear_on_submit=True):
        category = st.selectbox(
            "खर्च प्रकार (Category) *",
            [
                "मंडप व सजावट (Decoration/Mandap)",
                "प्रसाद / महाप्रसाद (Prasad)",
                "ध्वनी व प्रकाश (Sound/Light)",
                "पूजा साहित्य (Pooja Items)",
                "इतर (Other)"
            ]
        )
        description = st.text_input("तपशील / वर्णन (Description)")
        
        # min_value=1.0 ensures the input box cannot accept 0 or negative numbers
        expense_amount = st.number_input("खर्च रक्कम (Amount in ₹) *", min_value=1.0, value=100.0, step=50.0)
        
        exp_submitted = st.form_submit_button("खर्च जतन करा (Save Expense)")
        
        if exp_submitted:
            if expense_amount > 0:
                db.add_expense(category, description, expense_amount)
                st.success(f"✅ खर्च यशस्वीरीत्या नोंदवला: ₹{expense_amount:,.2f} ({category})")
                st.rerun()
            else:
                st.error("⚠️ कृपया ₹० पेक्षा जास्त रक्कम टाका (Please enter an amount greater than 0)!")

    st.write("----")
    st.subheader("📋 सर्व खर्चांची यादी (All Expense Records)")

    expenses_data = db.get_all_expenses()
    if expenses_data:
        exp_columns = ["क्र. (ID)", "खर्च प्रकार (Category)", "तपशील (Description)", "रक्कम (₹)", "तारीख (Date & Time)"]
        exp_df = pd.DataFrame(expenses_data, columns=exp_columns)
        exp_df.insert(0, "अनुक्रमांक (Sr. No.)", range(1, len(exp_df) + 1))
        st.dataframe(exp_df, use_container_width=True, hide_index=True)
    else:
        st.info("अजून कोणताही खर्च नोंदवलेला नाही (No expenses recorded yet).")


with st.expander("🗑️ चुकीची नोंद हटवा (Delete Wrong Expense Entry)"):
    del_id = st.number_input("हटवण्यासाठी खर्च क्र. (ID) टाका", min_value=1, step=1)
    if st.button("नोंद हटवा (Delete)"):
        db.delete_expense(del_id)
        st.warning(f"खर्च क्र. #{del_id} हटवला गेला!")
        st.rerun()