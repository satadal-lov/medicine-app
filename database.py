import sqlite3
import os

DB_PATH = 'medicines.db'

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
    
    # Sample data
    sample_data = [
        ('Crocin', 'Paracetamol', 30, 5, 'জ্বর ও মাথাব্যথা', 'বমি বমি ভাব'),
        ('Dolo 650', 'Paracetamol', 35, 5, 'জ্বর ও মাথাব্যথা', 'বমি বমি ভাব'),
        ('Combiflam', 'Ibuprofen + Paracetamol', 55, 12, 'ব্যথা ও জ্বর', 'পেটব্যথা'),
        ('Azithral', 'Azithromycin', 180, 40, 'ব্যাকটেরিয়াল ইনফেকশন', 'ডায়রিয়া'),
        ('Augmentin', 'Amoxicillin', 220, 45, 'ব্যাকটেরিয়াল ইনফেকশন', 'বমি'),
        ('Pantop', 'Pantoprazole', 120, 20, 'অ্যাসিডিটি', 'মাথাব্যথা'),
        ('Omez', 'Omeprazole', 100, 15, 'অ্যাসিডিটি ও আলসার', 'ডায়রিয়া'),
        ('Allegra', 'Fexofenadine', 150, 25, 'অ্যালার্জি', 'ঘুম ঘুম ভাব'),
        ('Cetrizine', 'Cetirizine', 45, 8, 'অ্যালার্জি ও সর্দি', 'ঘুম ঘুম ভাব'),
        ('Metformin', 'Metformin', 80, 15, 'ডায়াবেটিস', 'বমি বমি ভাব'),
        ('Glycomet', 'Metformin', 90, 15, 'ডায়াবেটিস', 'পেটব্যথা'),
        ('Amlodipine', 'Amlodipine', 60, 10, 'উচ্চ রক্তচাপ', 'পা ফোলা'),
        ('Stamlo', 'Amlodipine', 75, 10, 'উচ্চ রক্তচাপ', 'মাথাব্যথা'),
        ('Atorva', 'Atorvastatin', 130, 25, 'কোলেস্টেরল', 'মাংসপেশিতে ব্যথা'),
        ('Lipitor', 'Atorvastatin', 200, 25, 'কোলেস্টেরল', 'মাংসপেশিতে ব্যথা'),
    ]
    
    c.execute('SELECT COUNT(*) FROM medicines')
    if c.fetchone()[0] == 0:
        c.executemany('''
            INSERT INTO medicines 
            (brand_name, generic_name, brand_price, generic_price, usage, side_effects)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_data)
    
    conn.commit()
    conn.close()

def search_medicine(name):
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

# Initialize database when imported
init_db()