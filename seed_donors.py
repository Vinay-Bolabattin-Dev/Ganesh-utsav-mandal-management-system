from database import init_db, add_master_donor_bulk
import sqlite3

# Clear old entries to avoid duplicates
with sqlite3.connect("ganesh_utsav_mandal.db") as conn:
    conn.cursor().execute("DELETE FROM previous_donors")
    conn.commit()

donors_data = [
    # Format: (Marathi Name | English Name, phone, last_year_amount)
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

if __name__ == "__main__":
    init_db()
    add_master_donor_bulk(donors_data)
    print("Database updated with dual-language search support!")