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
    except Exception as e:
        print(f"Excel Error: {e}")
        return

    # 🔥 We run this TWICE per execution to get 1 Plumbing + 1 Book page
    for category in ["plumbing", "book"]:
        row = df.sample(n=1).iloc[0]
        city, zip_code = str(row['City']), str(row['ZipCode'])

        if category == "plumbing":
            keyword = random.choice(ULTRA_PLUMBING_KEYWORDS).format(city=city, zip_code=zip_code)
            slug = f"plumber-{city.lower().replace(' ', '-')}-{zip_code}"
        else:
            keyword = random.choice(ALL_EXPANDED_BOOK_KEYWORDS)
            # Create a unique slug for the book pages too
            slug = f"book-{keyword.lower().replace(' ', '-')}-{zip_code}"

        file_path = f"services/{slug}.html"
        full_url = f"https://serviceshubnest.github.io/hubnest.github.io/{file_path}"

        # Professional Book Promotion Section
    html = f"""<!DOCTYPE html><html><head><title>{keyword}</title></head>
    <body style='font-family:sans-serif; padding:20px; line-height:1.6;'>
    <h1>{keyword}</h1>
    <p>Providing expert service in {city}, {zip_code}. Contact us for immediate support.</p>
    
    <div style='background:#f4f4f4; padding:20px; border-radius:10px; margin-top:30px; border:1px solid #ddd;'>
        <h3 style='margin-top:0;'>Special Recommendation: {book_title}</h3>
        <p>By Author <b>Asif Mehmood</b></p>
        <p>Master the art of confidence and connection with this practical guide.</p>
        
        <div style='margin-top:15px;'>
            <a href="https://play.google.com/store/books/details?id=9IG-EQAAQBAJ" 
               style="background:#007bff; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; margin-right:10px; display:inline-block;">
               📖 Get the E-Book
            </a>
            <a href="https://play.google.com/store/audiobooks/details?id=AQAAAEAaNSp1IM" 
               style="background:#28a745; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; display:inline-block;">
               🎧 Get the Audiobook
            </a>
        </div>
    </div>
    </body></html>"""

        if not os.path.exists('services'): os.makedirs('services')
        with open(file_path, "w") as f:
            f.write(html)

        # This calls the indexing function
        notify_google_indexing(full_url)

if __name__ == "__main__":
    build_and_index()
