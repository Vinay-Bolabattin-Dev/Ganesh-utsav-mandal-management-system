import pandas as pd

# Master donors from last year
master_donors_data = [
    (1, "अशोक बोद्धूल | Ashok Boddhul", "", 751.0),
    (2, "पद्मावती हॉटेल | Padmavati Hotel", "", 201.0),
    (3, "अनिल कस्तुरी | Anil Kasturi", "", 601.0),
    (4, "कुमार हेअर स्टाईल | Kumar Hair Style", "", 501.0),
    (5, "यल्लप्पा बोल्ली | Yallappa Bolli", "", 2100.0),
    (6, "महेश माशेट्टी | Mahesh Mashetti", "", 251.0),
    (7, "राकेश नोरा | Rakesh Nora", "", 501.0),
    (8, "गणेश श्रीगिरी | Ganesh Shrigiri", "", 501.0),
    (9, "झोड्डू | Zoddu", "", 501.0),
    (10, "नरेश केंडीकटला | Naresh Kendikatla", "", 1100.0),
    (11, "सुरज ईराबत्ती | Suraj Irabatti", "", 1001.0),
    (12, "बोल्ली | Bolli", "", 2001.0),
    (13, "गणेश मेकॅनिकल | Ganesh Mechanical", "", 1200.0),
    (14, "राम गुंडेली (सभासद) | Ram Gundeli", "", 1001.0),
    (15, "संतोष दासरी (सभासद) | Santosh Dasari", "", 1001.0),
    (16, "अंबादास अलवाल (सभासद) | Ambadas Alwal", "", 1001.0),
    (17, "रोहित दासरी (सभासद) | Rohit Dasari", "", 1001.0),
    (18, "प्रसाद मोदास (सभासद) | Prasad Modas", "", 1001.0),
    (19, "गोपी गाजूल (सभासद) | Gopi Gajul", "", 500.0),
    (20, "राम दासरी (सभासद) | Ram Dasari", "", 1001.0),
    (21, "अभय हिबारे (सभासद) | Abhay Hibare", "", 1001.0),
    (22, "श्रीकांत गेट्याल | Shrikant Getyal", "", 2501.0),
    (23, "साई कलेक्शन | Sai Collection", "", 151.0),
    (24, "ओम कोल्ड्रिंक्स | Om Coldrinks", "", 101.0),
    (25, "जय भवानी स्वीट्स | Jay Bhavani Sweets", "", 851.0),
    (26, "मुलचंद मिठाई | Mulchand Mithai", "", 301.0),
    (27, "सत्तरया ईराबत्ती | Sattaraya Irabatti", "", 1001.0),
    (28, "श्रीनिवास आडम | Shrinivas Adam", "", 701.0),
    (29, "सुर्का कृष्णा | Surka Krishna", "", 301.0),
    (30, "अभय टेक्स | Abhay Tex", "", 1001.0),
    (31, "नरसय्या बोलाबत्तीन | Narsayya Bolabattin", "", 501.0),
    (32, "चक दे दाल | Chak De Dal", "", 501.0),
    (33, "लंगर बिडी कंपनी | Langar Bidi Company", "", 1501.0),
    (34, "पुष्पा टेक्स्टाईल | Pushpa Textile", "", 701.0),
    (35, "व्ही. के. जी वाईन्स | VKG Wines", "", 1501.0),
    (36, "नरसय्या अचली | Narsayya Achali", "", 1101.0),
    (37, "वैभव क्रिएशन | Vaibhav Creation", "", 1001.0),
    (38, "शरद दुडम | Sharad Dudam", "", 1101.0),
    (39, "अंकिता टेक्स (कंदोब्बे) | Ankita Tex Kandobbe", "", 1101.0),
    (40, "शिवकुमार यम्ला | Shivkumar Yamla", "", 501.0),
    (41, "बिर्रु मालक | Birru Malak", "", 1501.0),
    (42, "आदित्य टेक्स स्टोअर्स (संगीता) | Aditya Tex Stores Sangita", "", 5001.0),
    (43, "माशेट्टी | Mashetti", "", 50001.0),
    (44, "सत्यनारायण गुंडेली | Satyanarayan Gundeli", "", 1501.0),
    (45, "रवी दुडम | Ravi Dudam", "", 501.0),
    (46, "विश्वनाथ तुम्मा | Vishwanath Tumma", "", 2011.0),
    (47, "बालाजी धोता | Balaji Dhota", "", 2011.0),
    (48, "दिनेश येलगेटी | Dinesh Yelgeti", "", 3011.0),
    (49, "आनंद टेलर | Anand Tailor", "", 651.0),
    (50, "रोहित फ्लॉवर | Rohit Flower", "", 1001.0),
    (51, "पद्मावती टी हाऊस | Padmavati Tea House", "", 601.0)
   

]

df_donations = pd.DataFrame(columns=["id", "donor_name", "phone_number", "amount", "payment_mode", "date_added"])
df_expenses = pd.DataFrame(columns=["id", "category", "description", "amount", "date_added"])
df_pending_donations = pd.DataFrame(columns=["id", "donor_name", "phone_number", "amount", "promised_date", "notes", "status", "date_added"])
df_previous_donors = pd.DataFrame(master_donors_data, columns=["id", "donor_name", "phone_number", "last_year_amount"])

# Save directly as Excel workbook with 4 tabs
with pd.ExcelWriter("Ganesh_Mandal_2026.xlsx", engine="openpyxl") as writer:
    df_donations.to_excel(writer, sheet_name="donations", index=False)
    df_expenses.to_excel(writer, sheet_name="expenses", index=False)
    df_pending_donations.to_excel(writer, sheet_name="pending_donations", index=False)
    df_previous_donors.to_excel(writer, sheet_name="previous_donors", index=False)

print("SUCCESS: File Ganesh_Mandal_2026.xlsx generated!")