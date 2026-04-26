import sqlite3
import os
import requests
import json

DB_PATH = '/tmp/medicines.db'
GEMINI_API_KEY = 'AIzaSyB68L__n9XG4ynfZmrA7AQQzr_TtTVdH3A'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name TEXT NOT NULL,
            generic_name TEXT NOT NULL,
            brand_price REAL NOT NULL,
            generic_price REAL NOT NULL,
            usage TEXT NOT NULL,
            side_effects TEXT
        )
    ''')
    conn.commit()
    conn.close()

def search_medicine_db(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT brand_name, generic_name, brand_price, generic_price, usage, side_effects
        FROM medicines
        WHERE brand_name LIKE ? OR generic_name LIKE ?
    ''', (f'%{name}%', f'%{name}%'))
    results = c.fetchall()
    conn.close()
    return results

def search_with_ai(medicine_name):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""আমি "{medicine_name}" ওষুধের তথ্য জানতে চাই।
    
    নিচের JSON format এ উত্তর দিন, অন্য কিছু লিখবেন না:
    {{
        "found": true/false,
        "medicines": [
            {{
                "brand_name": "ব্র্যান্ড নাম",
                "generic_name": "জেনেরিক নাম",
                "brand_price": দাম সংখ্যায়,
                "generic_price": জেনেরিক দাম সংখ্যায়,
                "usage": "ব্যবহার বাংলায়",
                "side_effects": "পার্শ্বপ্রতিক্রিয়া বাংলায়"
            }}
        ]
    }}
    
    ভারতের বাজারের দাম দিন। সর্বোচ্চ ৩টা বিকল্প দিন।"""
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        text = data['candidates'][0]['content']['parts'][0]['text']
        text = text.replace('```json', '').replace('```', '').strip()
        result = json.loads(text)
        
        if result.get('found') and result.get('medicines'):
            medicines = []
            for m in result['medicines']:
                medicines.append((
                    m['brand_name'],
                    m['generic_name'],
                    float(m['brand_price']),
                    float(m['generic_price']),
                    m['usage'],
                    m['side_effects']
                ))
            return medicines
    except:
        pass
    return []

def search_medicine(name):
    results = search_with_ai(name)
    return results

init_db()