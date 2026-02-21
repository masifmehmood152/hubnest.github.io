import os
import json
import random
import pandas as pd
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

# ==========================================
# 🔥 1. MASSIVE KEYWORD LISTS (12,500+ Combos)
# ==========================================
problem_intent = ["Fix", "Repair", "Emergency Repair", "24/7 Repair", "Immediate Fix", "Stop Leak Now", "Call Now for Repair"]
service_types = ["Plumber", "Drain Cleaning", "Burst Pipe Repair", "Water Heater Installation", "Sewer Line Replacement", "Slab Leak Repair", "Toilet Repair"]
location_modifiers = ["{city}", "{zip_code}", "Near Me", "Local", "Available Now"]

ULTRA_PLUMBING_KEYWORDS = [f"{i} {s} {l}" for i in problem_intent for s in service_types for l in location_modifiers]

book_title = "Becoming You: Confidence, Connection, and Growth"
problem_intent_book = ["Overcoming Self-Doubt", "Stop Overthinking", "Build Confidence", "Improve Social Skills"]
buyer_modifiers = ["Book", "Guide", "Blueprint", "Practical Guide"]
audience_modifiers = ["for Professionals", "for Introverts", "for Leaders", "for Career Growth"]

# Change 'for l in audience_modifiers' to 'for a in audience_modifiers'
ALL_EXPANDED_BOOK_KEYWORDS = [
    f"{b} {p} {a}" 
    for b in buyer_modifiers 
    for p in problem_intent_book 
    for a in audience_modifiers
]

# ==========================================
# 🚀 2. THE INDEXING API LOGIC
# ==========================================
def notify_google_indexing(url):
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    if not json_creds:
        print("❌ GOOGLE_CREDENTIALS Secret is missing!")
        return

    scopes = ["https://www.googleapis.com/auth/indexing"]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(json_creds), scopes)
        http = credentials.authorize(httplib2.Http())
        endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        
        content = json.dumps({"url": url, "type": "URL_UPDATED"})
        response, content_resp = http.request(endpoint, method="POST", body=content)
        
        if response.status == 200:
            print(f"✅ Google Notified: {url}")
        elif response.status == 429:
            print("🛑 Quota Limit (200) Reached. Stopping for today.")
            exit(0)
        else:
            print(f"⚠️ Status {response.status}: {content_resp}")
    except Exception as e:
        print(f"❌ Indexing Error: {e}")

# ==========================================
# 🚀 2. THE INDEXING API LOGIC
# ==========================================
def notify_google_indexing(url):
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    if not json_creds:
        print("❌ GOOGLE_CREDENTIALS Secret is missing!")
        return

    scopes = ["https://www.googleapis.com/auth/indexing"]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(json_creds), scopes)
        http = credentials.authorize(httplib2.Http())
        endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        
        content = json.dumps({"url": url, "type": "URL_UPDATED"})
        response, content_resp = http.request(endpoint, method="POST", body=content)
        
        if response.status == 200:
            print(f"✅ Google Notified: {url}")
        elif response.status == 429:
            print("🛑 Quota Limit (200) Reached. Stopping for today.")
            exit(0)
        else:
            print(f"⚠️ Status {response.status}: {content_resp}")
    except Exception as e:
        print(f"❌ Indexing Error: {e}")

# ==========================================
# 🛠️ 3. PAGE BUILDER LOGIC
# ==========================================
def build_and_index():
    try:
        df = pd.read_excel("locations.xlsx")
    except Exception as e:
        print(f"Excel Error: {e}")
        return

    company_name = "Hubnest"
    tagline = "Essential Services, Expert Solutions"
    book_title = "Becoming You: Confidence, Connection, and Growth"
    book_cover_url = "https://play-lh.googleusercontent.com/nIKYSu9wpS89zWGbVtI5fiNjokKbZK_ZZB0rAog7NlHXb9NZtWr05QgI-8HPNSCYy_vO7nUwE9ED9g=w480-h690-rw"

    for category in ["plumbing", "book"]:
        row = df.sample(n=1).iloc[0]
        city, zip_code = str(row['City']), str(row['ZipCode'])

        if category == "plumbing":
            keyword = random.choice(ULTRA_PLUMBING_KEYWORDS).format(city=city, zip_code=zip_code)
            slug = f"plumber-{city.lower().replace(' ', '-')}-{zip_code}"
            
            # 📞 Plumbing specific content
            action_section = f"""
            <div class="call-box">
                <strong>📞 Need Assistance?</strong><br>
                <a href="tel:3085508314" style="font-size: 20px; color: #1a73e8; text-decoration: none; font-weight: bold;">(308) 550-8314</a>
            </div>"""
        else:
            keyword = random.choice(ALL_EXPANDED_BOOK_KEYWORDS)
            slug = f"book-{keyword.lower().replace(' ', '-')}-{zip_code}"
            
            # 📖 Book specific content (No phone number)
            action_section = f"""
            <div style="margin: 20px 0; border-left: 4px solid #1a73e8; padding-left: 15px;">
                <p style="font-style: italic; color: #5f6368;">"Unlock your potential with expert insights on leadership and self-growth, curated by the Hubnest professional network."</p>
            </div>"""

        file_path = f"services/{slug}.html"
        full_url = f"https://serviceshubnest.github.io/hubnest.github.io/{file_path}"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{keyword} | {company_name}</title>
    <style>
        body {{ font-family: -apple-system, system-ui, sans-serif; background: #f8f9fa; margin: 0; padding: 0; color: #202124; }}
        .header {{ background: #fff; border-bottom: 2px solid #1a73e8; padding: 20px; text-align: center; }}
        .content {{ max-width: 600px; margin: 20px auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .preview-card {{ 
            display: flex; border: 1px solid #dadce0; border-radius: 8px; overflow: hidden; 
            text-decoration: none; color: inherit; margin-top: 25px; transition: background 0.2s;
        }}
        .preview-card:hover {{ background: #f1f3f4; }}
        .cover-img {{ width: 120px; height: 160px; object-fit: cover; border-right: 1px solid #dadce0; }}
        .details {{ padding: 15px; display: flex; flex-direction: column; justify-content: center; }}
        .badge {{ width: 140px; margin-top: 10px; }}
        .call-box {{ background: #e8f0fe; padding: 15px; border-radius: 8px; margin: 20px 0; text-align: center; }}
        .audio-link {{ color: #1e8e3e; font-weight: bold; text-decoration: none; font-size: 14px; margin-top: 8px; display: block; }}
    </style>
</head>
<body>

    <div class="header">
        <h1 style="margin:0; font-size: 24px;">{company_name}</h1>
        <p style="margin:5px 0 0; color: #1a73e8; font-weight: bold; font-size: 14px; text-transform: uppercase;">{tagline}</p>
    </div>

    <div class="content">
        <h2 style="font-size: 20px; color: #1a73e8;">{keyword}</h2>
        <p>Expert solutions for <b>{city}</b>. At {company_name}, we are dedicated to providing high-quality results and professional excellence.</p>

        {action_section}

        <hr style="border:0; border-top: 1px solid #eee; margin: 30px 0;">

        <p style="font-size: 12px; color: #70757a; text-transform: uppercase; font-weight: bold; letter-spacing: 0.5px;">Official Recommendation</p>
        
        <a href="https://play.google.com/store/books/details?id=9IG-EQAAQBAJ" class="preview-card" target="_blank">
            <img src="{book_cover_url}" alt="Book Cover" class="cover-img">
            <div class="details">
                <div style="font-weight: bold; font-size: 16px;">{book_title}</div>
                <div style="font-size: 13px; color: #5f6368; margin-top: 4px;">By Asif Mehmood</div>
                <div style="color: #f4b400; font-size: 14px; margin-top: 5px;">★★★★★ <span style="color:#70757a; font-size:12px;">(Official)</span></div>
                <img src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" class="badge" alt="Get it on Google Play">
            </div>
        </a>

        <div style="text-align: center; margin-top: 15px;">
            <a href="https://play.google.com/store/audiobooks/details?id=AQAAAEAaNSp1IM" target="_blank" class="audio-link">
                🎧 Get the Audiobook Version
            </a>
        </div>
    </div>

    <footer style="text-align: center; padding: 20px; font-size: 12px; color: #70757a;">
        © 2026 {company_name} | {tagline}<br>
        Serving {city}, {zip_code}
    </footer>

</body>
</html>"""

        if not os.path.exists('services'): os.makedirs('services')
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        notify_google_indexing(full_url)
# --- THE CODE BELOW MUST BE FLUSH TO THE LEFT (NO INDENTATION) ---

if __name__ == "__main__":
    print("🎬 Starting...")
    build_and_index()
    print("✅ Finished.")
