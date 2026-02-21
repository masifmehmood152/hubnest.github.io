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

        # --- THE PROFESSIONAL TEMPLATE ---
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="Licensed plumber providing fast, same day, affordable plumbing services in {city}. Call {phone} for a FREE estimate.">
    <style>
        :root {{ --primary: #1a73e8; --secondary: #d93025; --text: #202124; --bg: #f8f9fa; }}
        body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: var(--bg); margin: 0; padding: 0; color: var(--text); line-height: 1.5; }}
        
        /* Header */
        .nav {{ background: #fff; padding: 15px 20px; border-bottom: 3px solid var(--primary); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .logo {{ font-weight: 800; font-size: 22px; color: var(--primary); text-decoration: none; letter-spacing: -1px; }}
        .tagline {{ font-size: 12px; color: #5f6368; text-transform: uppercase; font-weight: bold; }}

        /* Main Container */
        .container {{ max-width: 600px; margin: 20px auto; padding: 0 15px; }}
        .card {{ background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); padding: 30px; }}
        
        /* Headline Section */
        h1 {{ font-size: 24px; color: var(--primary); margin-top: 0; line-height: 1.2; }}
        .location-badge {{ background: #e8f0fe; color: var(--primary); padding: 5px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 15px; }}

        /* The "Canyon Hills" Style CTA Box */
        .cta-box {{ background: #fff5f5; border: 2px solid var(--secondary); border-radius: 12px; padding: 25px; text-align: center; margin: 25px 0; }}
        .cta-box p {{ margin: 0 0 10px 0; font-weight: bold; color: var(--secondary); letter-spacing: 1px; font-size: 14px; }}
        .phone-link {{ font-size: 32px; color: var(--secondary); text-decoration: none; font-weight: 900; display: block; margin: 5px 0; }}
        .btn {{ background: var(--secondary); color: #fff; padding: 12px 25px; border-radius: 5px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 15px; transition: transform 0.2s; }}
        .btn:hover {{ transform: scale(1.05); }}

        /* Details List */
        .features {{ list-style: none; padding: 0; margin: 25px 0; }}
        .features li {{ padding: 10px 0; border-bottom: 1px solid #eee; display: flex; align-items: center; font-size: 15px; }}
        .features li:last-child {{ border: none; }}
        .icon {{ margin-right: 15px; font-size: 18px; }}

        /* Recommendation Section (For Book Pages) */
        .rec-section {{ margin-top: 40px; border-top: 2px solid #eee; padding-top: 25px; }}
        .rec-card {{ display: flex; border: 1px solid #dadce0; border-radius: 10px; text-decoration: none; color: inherit; transition: background 0.2s; }}
        .rec-card:hover {{ background: #f8f9fa; }}
        .rec-img {{ width: 100px; height: 140px; object-fit: cover; border-right: 1px solid #dadce0; }}
        .rec-details {{ padding: 15px; }}

        footer {{ text-align: center; padding: 40px 20px; font-size: 13px; color: #70757a; }}
    </style>
</head>
<body>

    <div class="nav">
        <div>
            <a href="#" class="logo">{company_name}</a>
            <div class="tagline">{tagline}</div>
        </div>
        <a href="tel:3085508314" style="background:var(--primary); color:#fff; padding:8px 15px; border-radius:5px; text-decoration:none; font-weight:bold; font-size:14px;">CALL NOW</a>
    </div>

    <div class="container">
        <div class="card">
            <span class="location-badge">📍 {city}, {zip_code}</span>
            <h1>{keyword}</h1>
            
            <p>Reliable, local expertise you can count on. Whether it is an emergency fix or a planned installation, our team in <b>{city}</b> delivers high-quality results at a price you can afford.</p>

            <div class="cta-box">
                <p>LICENSED • BONDED • INSURED</p>
                <strong>FREE ESTIMATES & SAME DAY SERVICE</strong>
                <a href="tel:3085508314" class="phone-link">{phone}</a>
                <a href="tel:3085508314" class="btn">Emergency Dispatch</a>
            </div>

            <ul class="features">
                <li><span class="icon">🕒</span> <b>24/7 Availability:</b> We never close for emergencies.</li>
                <li><span class="icon">🛠️</span> <b>Full Service:</b> Drains, Pipes, Heaters & more.</li>
                <li><span class="icon">💰</span> <b>Fair Pricing:</b> Upfront quotes with no hidden fees.</li>
                <li><span class="icon">🏆</span> <b>Guaranteed Work:</b> Your satisfaction is our priority.</li>
            </ul>

            {recommendation_box}
        </div>
    </div>

    <footer>
        © 2026 {company_name} Plumbing & Professional Services<br>
        Serving {city}, {zip_code} and nearby areas.<br>
        <span style="display:block; margin-top:10px; color: var(--primary); font-weight:bold;">24/7 Dispatch: {phone}</span>
    </footer>

</body>
</html>"""

        if not os.path.exists('services'): os.makedirs('services')
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
 

# --- THE CODE BELOW MUST BE FLUSH TO THE LEFT (NO INDENTATION) ---

if __name__ == "__main__":
    import time # Make sure this is imported!
    print("🎬 Starting...")
    build_and_index()
    print("✅ Finished.")
