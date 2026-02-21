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
# 🛠️ 3. PAGE BUILDER LOGIC
# ==========================================
def build_and_index():
    try:
        df = pd.read_excel("locations.xlsx")
        row = df.sample(n=1).iloc[0]
        city, zip_code = str(row['City']), str(row['ZipCode'])
    except Exception as e:
        print(f"Excel Error: {e}")
        return

    # Pick keywords
    p_key = random.choice(ULTRA_PLUMBING_KEYWORDS).format(city=city, zip_code=zip_code)
    b_key = random.choice(ALL_EXPANDED_BOOK_KEYWORDS)

    slug = f"plumber-{city.lower().replace(' ', '-')}-{zip_code}"
    file_path = f"services/{slug}.html"
    full_url = f"https://serviceshubnest.github.io/{file_path}"

    # Simple HTML Template
    html = f"""<!DOCTYPE html><html><head><title>{p_key}</title></head>
    <body style='font-family:sans-serif; padding:20px;'>
    <h1>{p_key}</h1>
    <p>Providing expert plumbing in {city}, {zip_code}. Call (308) 550-8314.</p>
    <hr>
    <h3>Recommended Reading: {b_key}</h3>
    <p>Check out <b>{book_title}</b> by Asif Mehmood on Google Play.</p>
    </body></html>"""

    if not os.path.exists('services'): os.makedirs('services')
    with open(file_path, "w") as f:
        f.write(html)

    notify_google_indexing(full_url)

if __name__ == "__main__":
    build_and_index()
