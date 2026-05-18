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

live_data = {"last_crash": 1.50}

def start_dkwin_scraper():
    print("🚀 Dkwin লাইভ স্ক্র্যাপার সার্ভারে চালু হচ্ছে...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    # সার্ভারের জন্য ক্রোম ড্রাইভার সেটআপ
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://dkwin.com/game/aviator") 
    time.sleep(5)

    last_checked_multiplier = ""

    while True:
        try:
            crash_elements = driver.find_elements(By.CLASS_NAME, "stats-item")
            if crash_elements:
                latest_crash_text = crash_elements[0].text
                clean_number = latest_crash_text.replace('x', '').strip()
                
                if clean_number != last_checked_multiplier:
                    last_checked_multiplier = clean_number
                    live_data["last_crash"] = float(clean_number)
        except:
            pass
        time.sleep(2)

@app.route('/live-prediction', methods=['GET'])
def get_prediction():
    last_crash = live_data["last_crash"]
    if last_crash < 1.50:
        predicted_multiplier = (1.50 + (time.time() % 3.5)) 
    else:
        predicted_multiplier = (1.01 + (time.time() % 1.2))
        
    return jsonify({
        "status": "success",
        "last_crash": last_crash,
        "prediction": round(predicted_multiplier, 2)
    })

if __name__ == "__main__":
    scraper_thread = threading.Thread(target=start_dkwin_scraper, daemon=True)
    scraper_thread.start()
    # Render সার্ভার স্বয়ংক্রিয়ভাবে PORT অ্যাসাইন করে
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
