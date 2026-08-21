import streamlit as st
import pandas as pd
import database as db
import os 
import urllib.parse
from datetime import date

##"""" Authentication Gate (PIN  Protection) """
def  check_password():
    """" Return True if user enters the correct PIN """


    if not st.session_state.get("authenticated", False ):
        login_col1,login_col2,login_col3=st.columns([1,2,1])
        with login_col2:
            st.markdown(
              """
                <div style="text-align: center; margin-top: 50px; margin-bottom: 20px;">
                    <h2 style="color: #FF9933; margin-bottom: 5px;">🚩 श्री स्वामी समर्थ मित्र मंडळ</h2>
                    <p style="color: #CCCCCC; font-size: 15px;">सार्वजनिक गणेशोत्सव २०२६ | अधिकृत प्रवेश</p>
                </div>
                """, 
                unsafe_allow_html=True 
            )
            with st.form("login_form "):
                pin_input=st.text_input("🔑 सिक्रेट पिन / पासवर्ड टाका (Enter PIN)", placeholder= "Enter PIN ")
                login_btn=st.form_submit_button("लॉगिन (Unlock Dashboard)", use_container_width=True)

        if login_btn:
                    # Safely check Streamlit secrets, fall back to "1989" if secrets file doesn't exist
                    try:
                        correct_pin = st.secrets.get("APP_PASSWORD", "1989")
                    except Exception:
                        correct_pin = "1989"

                    if pin_input == correct_pin:
                        st.session_state["authenticated"] = True
                        st.rerun()
                    else:
                        st.error("❌ चुकीचा पासवर्ड! कृपया योग्य पिन टाका. (Incorrect PIN)")
        return False

    return True



##-------- Mandal Instagram Configaration (used for WA msg )-------------------------------
INSTAGRAM_HANDLE= "ss_group__1989"
INSTAGRAM_URL=f"https://instagram.com/{INSTAGRAM_HANDLE}"

##------------------ Whats app url helper  (Confrimed Donations)----------------------------
def create_whatsapp_url(phone, name, receipt_no, amount, mode):
    ## Generating whatsapp click-to-chat URL with pre-filled receipt msg
    clean_phone = "".join(filter(str.isdigit, str(phone)))
    if len(clean_phone) == 10:
        clean_phone = "91" + clean_phone 

    formatted_amount=f"₹{int(amount):,}" if float(amount).is_integer() else f"₹{amount:,.2f}"

    lines = [
        "🚩 *श्री स्वामी समर्थ मित्र मंडळ* 🚩",
        "*सार्वजनिक गणेशोत्सव २०२६*",
        "",
        f"📄 *पावती क्र.(Receipt no)* : #{receipt_no}",
        f"👤 *देणगीदार (Donor)* : *_{name}_*",
        f"💰 *वर्गणी रक्कम (Amount)* : *{formatted_amount}*",
        f"💳 *पद्धत (Payment mode)* : {mode}",
        "",
        "📸 *नवनवीन रील्स आणि उत्सवाचे सर्व अपडेट्स पाहण्यासाठी मंडळाच्या Instagram पेजला नक्की फॉलो करा:*",
        f"👉 {INSTAGRAM_URL}",
        "",
        "🙏 *_मंडळाच्या वतीने आपले मनापासून आभार!_*",
        "🌺 *_गणपती बाप्पा मोरया, मंगलमूर्ती मोरया!_* 🌺"
    ]
    message_text = '\n'.join(lines)
    encoded_text = urllib.parse.quote(message_text.encode('utf-8'))
    return f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_text}"

## Whatsapp url helper for (Pending Donations)  

def create_pending_whatsapp_url(phone,name,amount,promised_date,notes):
    ##Generates pending donations pledge link 
    clean_phone= "".join(filter(str.isdigit ,str(phone)))
    if len(clean_phone)==10:
        clean_phone="91"+ clean_phone

    formatted_amount=f"₹{int(amount):,}" if float(amount).is_integer() else f"₹{amount:,.2f}"

    lines = [
        "🚩 *श्री स्वामी समर्थ मित्र मंडळ* 🚩",
        "*सार्वजनिक गणेशोत्सव २०२६*",
        "",
        "📋 *अंदाजित / थकीत वर्गणी नोंद (Pending Donations)*",
        f"👤 *नाव / संस्था(Donor name)* : *_{name}_*",
        f"💰 *नोंदवलेली रक्कम(Amount)* : *{formatted_amount}*",
        f"🗓️ *अपेक्षित तारीख(Promised date)* : {promised_date}",
    ]

    if notes.strip():
        lines.append(f"📝 *तपशील* : {notes}")
        
    lines.extend([
        "",
        "",
        "📸 *नवनवीन रील्स आणि उत्सवाचे सर्व अपडेट्स पाहण्यासाठी मंडळाच्या Instagram पेजला नक्की फॉलो करा:*",
        f"👉 {INSTAGRAM_URL}",
        "",
        "🙏 आपल्या सहकार्याबद्दल मनःपूर्वक धन्यवाद!",
        "🌺 *गणपती बाप्पा मोरया, मंगलमूर्ती मोरया!* 🌺"
    ])
    message_text='\n'.join(lines)
    encoded_text=urllib.parse.quote(message_text.encode('utf-8'))
    return f"http://api.whatsapp.com/send?phone={clean_phone}&text={encoded_text}"




##Page configuration & financial metrics & Header banner 
st.set_page_config(page_title="श्री स्वामी समर्थ मित्र मंडळ", page_icon="🚩", layout='wide')
##============ CSS Styling =============================================================
st.markdown(
    """
    <style>
    /* Metric Cards - Glowing Festive Gradient */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255, 153, 51, 0.08) 0%, rgba(20, 20, 20, 0.6) 100%);
        border: 1px solid rgba(255, 153, 51, 0.35);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 15px rgba(255, 153, 51, 0.12);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: #FF9933;
        box-shadow: 0 6px 20px rgba(255, 153, 51, 0.25);
    }
    div[data-testid="stMetricLabel"] {
        color: #E0E0E0 !important;
        font-weight: 600;
        font-size: 14px;
    }
    div[data-testid="stMetricValue"] {
        color: #FFB347 !important;
        font-weight: bold;
    }

    /* Tab Headers - Saffron Accent */
    button[data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 8px 8px 0 0 !important;
        transition: all 0.2s ease-in-out;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FF9933 !important;
        border-bottom-color: #FF9933 !important;
    }

    /* Form Buttons - Rich Golden Saffron Gradient */
    div.stButton > button[kind="primary"], div.stButton > button {
        background: linear-gradient(45deg, #FF6600 0%, #FF9933 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 15px !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 12px rgba(255, 102, 0, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 18px rgba(255, 102, 0, 0.5) !important;
    }

    /* Form Containers */
    div[data-testid="stForm"] {
        border: 1px solid rgba(255, 153, 51, 0.2);
        border-radius: 12px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.02);
    }
    </style>
    """,
    unsafe_allow_html=True
)

if not check_password():
    st.stop()



##======================================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

## Automatically pick up any single image inside the assets directory 
found_image=None
if os.path.exists(ASSETS_DIR):
    for filename in os.listdir(ASSETS_DIR):
        if filename.lower().endswith(('.png','.jpg', '.jpeg', '.webp')):
            found_image=os.path.join(ASSETS_DIR , filename)
            break
## full width top banner & title 

if found_image and os.path.exists(found_image):
    st.image(found_image, use_container_width=True)

## Cretered Festival Header
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, rgba(255, 153, 51, 0.12) 0%, rgba(25, 25, 25, 0.7) 100%);
        border: 1px solid rgba(255, 153, 51, 0.4);
        border-radius: 14px;
        padding: 16px 20px;
        text-align: center;
        margin-top: 14px;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px rgba(255, 153, 51, 0.18);
    ">
        <p style="margin: 0; font-size: 15px; color: #FFD700; font-weight: 600; letter-spacing: 1px;">
            ॥ श्री गणेशाय नमः ॥
        </p>
        <h1 style="margin: 4px 0; font-size: 38px; font-weight: 800; color: #FF9933; text-shadow: 0 2px 10px rgba(255, 153, 51, 0.3);">
            🚩 श्री स्वामी समर्थ मित्र मंडळ 🚩
        </h1>
        <p style="margin: 0; font-size: 18px; color: #E0E0E0; font-weight: 500;">
            सार्वजनिक गणेशोत्सव २०२६ | सोलापूर
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

total_coll , total_exp , balance = db.get_financial_summary() ## calling function from database.py
total_pending=db.get_total_pending_amount()

col1,col2,col3,col4=st.columns(4)
col1.metric(label="एकूण वर्गणी (Collection)", value =f"₹{total_coll:,.2f}")
col2.metric(label="एकूण खर्च (Expenses)", value=f"₹{total_exp:,.2f}")
col3.metric(label="शिल्लक रक्कम (Remaining Balance)", value=f"₹{balance:,.2f}")
col4.metric(label="येणे बाकी (Total Pending)", value=f"₹{total_pending:,.2f}")
st.write("----")

#navigation tables 
tab1, tab2, tab3, tab4 = st.tabs([
    "वर्गणी पावती (Collect Vargani)",
    "सर्व नोंदी (All Records)",
    "खर्च नोंद (Expenses)",
    "थकीत / अंदाजित वर्गणी (Pending Donations)"
])

## tab1 : New Donations receipet

with tab1: ## receipt table 
    st.subheader("नवीन वर्गणी पावती फाडा (New Donation Receipt)")

    with st.form("donation_form" ,clear_on_submit=True):
        donor_name=st.text_input("भक्ताचे / देणगीदाराचे नाव (Donor Name) *")
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

                if phone_number.strip():
                    wa_url = create_whatsapp_url(phone_number, donor_name, receipt_id, amount, payment_mode)
                    
                    # Clean direct HTML button that prevents browser double-encoding
                    st.markdown(
                        f"""
                        <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                            <div style="
                                background-color: #25D366;
                                color: white;
                                padding: 10px 20px;
                                text-align: center;
                                border-radius: 8px;
                                font-weight: bold;
                                font-size: 16px;
                                margin-top: 10px;
                                display: inline-block;
                                width: 100%;
                            ">
                                WhatsApp वर पावती पाठवा (Send Receipt on WhatsApp)
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

            else:
                st.error("कृपया देणगीदाराचे नाव टाका (Please enter donor name)!")

## tab2 : Confrimed Donor Records 
with tab2: ## donors list table 
    st.subheader("जमा वर्गणी यादी (All Donation Records)")
    
    records = db.get_all_donations()
    
    if records:
        columns = ["पावती क्र. (ID)", "भक्ताचे/देणगीदाराचे  नाव (Name)", "मोबाईल (Phone)", "रक्कम (₹)", "पद्धत (Mode)", "तारीख (Date & Time)"]
        df = pd.DataFrame(records, columns=columns)

        df.insert(0, "अनुक्रमांक (Sr. No.)", range(1, len(df) + 1))
        # Display table
        st.dataframe(df, use_container_width=True, hide_index=True)

        with st.expander("चुकीची वर्गणी नोंद हटवा (Delete Donor Entry)"):
                donor_options={
                    f"पावती #{row[0]} - {row[1]} (₹{row[3]:,.2f})": row[0]
                    for row in records
                }
                selected_lable=st.selectbox(
                    "हटवण्यासाठी देणगीदाराची पावती निवडा:",
                    options=list(donor_options.keys())
                )
                if st.button("वर्गणी नोंद कायमची हटवा (Delete Record)", type="primary"):
                    selected_id=donor_options[selected_lable]
                    db.delete_donor_record(selected_id)
                    st.success(f"पावती क्र. #{selected_id} यशस्वीरीत्या हटवली गेली!")
                    st.rerun()
    else:
            st.info("अजून कोणतीही वर्गणी जमा झालेली नाही (No donations recorded yet).")


        


## tab3: Expenses Management 
with tab3: ## expenses list table   
    st.subheader("मंडळाचा खर्च नोंदवा (Record Mandal Expense)")
    
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
                st.success(f"खर्च यशस्वीरीत्या नोंदवला: ₹{expense_amount:,.2f} ({category})")
                st.rerun()
            else:
                st.error(" कृपया ₹० पेक्षा जास्त रक्कम टाका (Please enter an amount greater than 0)!")

    st.write("----")
    st.subheader(" सर्व खर्चांची यादी (All Expense Records)")

    expenses_data = db.get_all_expenses()
    if expenses_data:
        exp_columns = ["क्र. (ID)", "खर्च प्रकार (Category)", "तपशील (Description)", "रक्कम (₹)", "तारीख (Date & Time)"]
        exp_df = pd.DataFrame(expenses_data, columns=exp_columns)
        exp_df.insert(0, "अनुक्रमांक (Sr. No.)", range(1, len(exp_df) + 1))
        st.dataframe(exp_df, use_container_width=True, hide_index=True)

        with st.expander("चुकीची नोंद हटवा (Delete Wrong Expense Entry)"):
            del_id = st.number_input("हटवण्यासाठी खर्च क्र. (ID) टाका", min_value=1, step=1)
            if st.button("नोंद हटवा (Delete)"):
                db.delete_expense(del_id)
                st.warning(f"खर्च क्र. #{del_id} हटवला गेला!")
            st.rerun()
    else:
        st.info("अजून कोणताही खर्च नोंदवलेला नाही (No expenses recorded yet).")

## tab4 : pending / pledged Donations 

with tab4 :
    st.subheader("नवीन थकीत / अंदाजित वर्गणी नोंदवा (Record Pledged Donation)")

    with st.form("pending_form",clear_on_submit=True):
        p_name=st.text_input("नाव / दुकान / कारखाना / संस्था (Name / Entity) *")
        p_phone=st.text_input("मोबाईल नंबर (Phone Number)")
        p_amount=st.number_input("अंदाजित / ठरलेली रक्कम (Pledged Amount in ₹) *", min_value=1.0, value=500.0, step=100.0)
        p_date=st.date_input("अपेक्षित देय तारीख (Expected Date)", value=date.today())
        p_notes=st.text_input("तपशील / टीप (Notes e.g. पगार झाल्यावर देणार / चेक देणार)")

        p_submitted=st.form_submit_button("थकीत नोंद जतन करा (Save Pledge)")
        if p_submitted:
            if p_name.strip():
                p_id=db.add_pending_donation(p_name,p_phone,p_amount, str(p_date),p_notes)
                st.success(f"थकीत नोंद यशस्वीरीत्या जतन झाली! नोंद क्र. #{p_id}")
                st.info(f"{p_name} | अपेक्षित रक्कम: ₹{p_amount:,.2f} | तारीख: {p_date}")

                if p_phone.strip():
                    p_wa_url = create_pending_whatsapp_url(p_phone, p_name, p_amount, str(p_date), p_notes)
                    st.markdown(
                        f"""
                        <a href="{p_wa_url}" target="_blank" style="text-decoration:none;">
                            <div style="background-color: #25D366; color: white; padding: 12px 20px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 16px; margin-top: 10px; display: inline-block; width: 100%;">
                                 WhatsApp वर नोंद पावती / स्मरणपत्र पाठवा (Send Pledge Note)
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.error("कृपया नाव प्रविष्ट करा (Please enter name)!")

    st.write("-------")    
    st.subheader("सर्व येणे बाकी / थकीत वर्गणी यादी (Active Pending List)")


    pending_records = db.get_all_pending_donations()
    if pending_records:
        p_columns = ["नोंद क्र. (ID)", "नाव / संस्था (Name)", "मोबाईल (Phone)", "रक्कम (₹)", "अपेक्षित तारीख (Expected Date)", "तपशील (Notes)", "नोंद तारीख (Created At)"]
        p_df = pd.DataFrame(pending_records, columns=p_columns)
        p_df.insert(0, "अनुक्रमांक (Sr. No.)", range(1, len(p_df) + 1))
        st.dataframe(p_df, use_container_width=True, hide_index=True)

        st.write("---")

        ## Payment received section 
        st.subheader( " रक्कम जमा झाली? मुख्य यादीत जोडा (Mark as Received)")
        pending_dict={f"#{row[0]} - {row[1]} (₹{row[3]:,.2f})": row[0] for row in pending_records}

        col_s1, col_s2, col_s3 =st.columns([2,1,1])
        with col_s1:
            settle_selection = st.selectbox("जमा झालेली नोंद निवडा:", options=list(pending_dict.keys()))
        with col_s2:
            settle_mode = st.selectbox("जमा पद्धत (Mode):", ['Cash', 'UPI', 'Bank Transfer'], key="settle_mode")
        with col_s3:
            st.write("")
            st.write("")
            settle_btn = st.button("रक्कम जमा करा (Confirm)", type="primary")    

        if settle_btn:
            target_pending_id=pending_dict[settle_selection]
            r_id, d_name, d_phone, d_amt = db.settle_pending_donation(target_pending_id, settle_mode)
            if r_id:
                st.balloons()
                st.success(f"रक्कम यशस्वी जमा झाली! मुख्य पावती क्र. #{r_id} तयार झाली.")

                if d_phone and str(d_phone).strip():
                    final_wa_url =create_whatsapp_url(d_phone, d_name,  r_id ,d_amt ,settle_mode)
                    st.markdown(
                        f"""
                        <a href="{final_wa_url}" target="_blank" style="text-decoration:none;">
                            <div style="background-color: #25D366; color: white; padding: 12px 20px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 16px; margin-top: 10px; display: inline-block; width: 100%;">
                                 अधिकृत पावती WhatsApp वर पाठवा (Send Official Receipt)
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )


        with st.expander("थकीत नोंद रद्द करा (Delete Pending Entry)"):
            del_p_label = st.selectbox("रद्द करण्यासाठी नोंद निवडा:", options=list(pending_dict.keys()), key="del_pending")
            if st.button("नोंद रद्द करा (Delete)", type="secondary"):
                del_target_id = pending_dict[del_p_label]
                db.delete_pending_donation(del_target_id)
                st.warning(f"नोंद #{del_target_id} रद्द केली गेली!")
                st.rerun()
    else:
        st.info("सध्या कोणतीही थकीत वर्गणी नाही (No pending donations).")

