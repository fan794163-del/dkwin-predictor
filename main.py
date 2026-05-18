import threading
import time
from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
CORS(app)

# গ্লোবাল ভেরিয়েবল যেখানে আসল লাইভ ডাটা জমা থাকবে
live_data = {"last_crash": 1.00}

def start_dkwin_scraper():
    print("🚀 Dkwin আসল লাইভ স্ক্র্যাপার চালু হচ্ছে...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ব্যাকগ্রাউন্ডে চলবে
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    # ড্রাইভার সেটআপ
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Dkwin এর অ্যাভিয়েটর গেম পেজ (প্রয়োজনে সঠিক লাইভ গেম ইউআরএল দিন)
    driver.get("https://dkwin.com/game/aviator") 
    time.sleep(10) # পেজটি পুরোপুরি লোড হওয়ার জন্য সময় দেওয়া

    last_checked_multiplier = ""

    while True:
        try:
            # গেমের শেষ ক্র্যাশ নম্বরের ক্লাস নেম (Dkwin অনুযায়ী)
            crash_elements = driver.find_elements(By.CLASS_NAME, "stats-item")
            if crash_elements:
                latest_crash_text = crash_elements[0].text
                clean_number = latest_crash_text.replace('x', '').strip()
                
                if clean_number != last_checked_multiplier:
                    last_checked_multiplier = clean_number
                    live_data["last_crash"] = float(clean_number)
                    print(f"🎯 নতুন ক্র্যাশ ডাটা পাওয়া গেছে: {clean_number}x")
        except Exception as e:
            print("ডাটা রিড করতে সমস্যা হচ্ছে, পুনরায় চেষ্টা করা হচ্ছে...", e)
        time.sleep(2)

@app.route('/live-prediction', methods=['GET'])
def get_prediction():
