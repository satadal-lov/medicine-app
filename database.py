import requests
import json

GEMINI_API_KEY = 'AIzaSyB68L__n9XG4ynfZmrA7AQQzr_TtTVdH3A'

def init_db():
    pass

def search_medicine(name):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""আমি "{name}" ওষুধের তথ্য জানতে চাই।
    
শুধু এই JSON format এ উত্তর দিন, অন্য কিছু লিখবেন না:
{{
    "found": true,
    "medicines": [
        {{
            "brand_name": "ব্র্যান্ড নাম",
            "generic_name": "জেনেরিক নাম",
            "brand_price": 100,
            "generic_price": 20,
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
        response = requests.post(url, json=payload, timeout=15)
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
