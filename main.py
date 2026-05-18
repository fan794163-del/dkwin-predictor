import time
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/live-prediction', methods=['GET'])
def get_prediction():
    # একটি ডেমো লাইভ ক্র্যাশ ডাটা জেনারেট করা (যা রিয়েল-টাইমে ওঠানামা করবে)
    # সময়ভিত্তিক বীজ (Seed) ব্যবহার করায় প্রতি সেকেন্ডে নম্বর পরিবর্তন হবে
    current_time = int(time.time())
    
    # গাণিতিক লজিক: ৬০% চান্স ছোট ক্র্যাশ, ৪০% চান্স বড় ক্র্যাশ
    if current_time % 3 == 0:
        # বড় মাল্টিপ্লায়ার (২.৫০ থেকে ৫.৫০)
        predicted_multiplier = 2.50 + (current_time % 31) / 10
        last_crash = 1.20 + (current_time % 5) / 10
    else:
        # ছোট মাল্টিপ্লায়ার (১.০৫ থেকে ২.২০)
        predicted_multiplier = 1.05 + (current_time % 12) / 10
        last_crash = 2.50 + (current_time % 15) / 10
        
    return jsonify({
        "status": "success",
        "last_crash": round(last_crash, 2),
        "prediction": round(predicted_multiplier, 2)
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
