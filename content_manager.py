import os
import json
import random
import pandas as pd
import string

# ==========================================
# 🔥 1. SUPERCHARGED KEYWORD LISTS (10,000+ COMBOS)
# ==========================================
p_urgency = ["Emergency", "24-7", "Instant", "Same-Day", "Licensed", "Fast", "Reliable", "Expert", "Affordable", "Top-Rated"]
p_intent = ["Fix", "Repair", "Installation", "Replacement", "Service", "Unclogging", "Detection", "Maintenance", "Cleanup", "Inspection"]
p_service = ["Plumber", "Drain", "Pipe", "Water Heater", "Sewer Line", "Slab Leak", "Toilet", "Faucet", "Sump Pump", "Gas Line", "Main Line", "Boiler"]
p_local = ["{city}", "{zip_code}", "Near Me", "Local", "In my area", "Nearby", "Neighborhood", "Regional", "District", "Citywide"]

ULTRA_PLUMBING_KEYWORDS = [f"{u} {i} {s} {l}" for u in p_urgency for i in p_intent for s in p_service for l in p_local]

b_format = ["Digital", "Audiobook", "Print", "E-book", "Official"]
b_buyer = ["Book", "Guide", "Blueprint", "Manual", "Masterclass", "Handbook", "Strategy", "System"]
b_problem = ["Overcoming Self-Doubt", "Stop Overthinking", "Build Confidence", "Social Skills", "Public Speaking", "Anxiety", "Networking", "Leadership"]
b_audience = ["Professionals", "Introverts", "Leaders", "Career Starters", "Entrepreneurs", "Executives", "Graduates", "Managers"]
b_outcome = ["Success", "Growth", "Freedom", "Connection", "Impact"]

ALL_EXPANDED_BOOK_KEYWORDS = [f"{f} {bu} on {p} for {a} for {o}" for f in b_format for bu in b_buyer for p in b_problem for a in b_audience for o in b_outcome]

def generate_uid(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# ==========================================
# 🛠️ 3. PAGE BUILDER LOGIC
# ==========================================
def build_and_index():
    if not os.path.exists('services'):
        os.makedirs('services')

    try:
        df = pd.read_excel("locations.xlsx")
    except Exception as e:
        print(f"Excel Error: {e}")
        return

    company_name = "Hubnest"
    tagline = "Essential Services, Expert Solutions"
    phone = "(308) 550-8314"
    book_title = "Becoming You: Confidence, Connection, and Growth"

    for category in ["plumbing", "book"]:
        row = df.sample(n=1).iloc[0]
        city, zip_code = str(row['City']), str(row['ZipCode'])
        uid = generate_uid()
        city_slug = city.lower().replace(' ', '-')

        # 🚀 START: CATEGORY LOGIC
        if category == "plumbing":
            keyword = random.choice(ULTRA_PLUMBING_KEYWORDS).format(city=city, zip_code=zip_code)
            page_title = f"{keyword} | {company_name} Plumbing"
            slug = f"{keyword.lower().replace(' ', '-')}-{uid}"
            
            # --- 📞 PLUMBING HTML ---
            specific_content = f"""
            <span class="badge">📍 LOCAL SERVICE: {city}</span>
            <h1>{keyword}</h1>
            <p>Licensed plumbing experts providing fast, same-day service in <b>{city}</b>. We specialize in emergency repairs and 24/7 maintenance.</p>
            <div class="cta-box">
                <p>LICENSED • BONDED • INSURED</p>
                <strong>FREE ESTIMATE & 24/7 DISPATCH</strong>
                <a href="tel:3085508314" class="phone-link">{phone}</a>
                <a href="tel:3085508314" class="btn btn-red">CALL FOR SERVICE</a>
                <p style="margin: 10px 0 0; font-size: 12px; color: #1e8e3e; font-weight: bold;">✅ Tap to Call Now</p>
            </div>
            """
        else:
            keyword = random.choice(ALL_EXPANDED_BOOK_KEYWORDS)
            page_title = f"{keyword} | Official {company_name} Guide"
            slug = f"book-{keyword.lower().replace(' ', '-')}-{city_slug}-{uid}"
            
            # --- 📖 BOOK HTML ---
            # Stable Book Image Address (zoom=1 is reliable)
            book_img = "https://books.google.com/books/content?id=9IG-EQAAQBAJ&printsec=frontcover&img=1&zoom=1"
            
            specific_content = f"""
            <span class="badge badge-green">📖 Official Publication</span>
            <h1>{keyword}</h1>
            <p>Master the blueprint for confidence and leadership. This {keyword} is curated for professionals in {city}.</p>
            <div class="book-card">
                <div class="book-flex">
                    <img src="{book_img}" class="book-img" alt="Book Cover">
                    <div class="book-info">
                        <h3 style="margin:0 0 5px 0; font-size:18px;">{book_title}</h3>
                        <p style="margin:0; font-size:14px; color:#5f6368;">By <b>Asif Mehmood</b></p>
                        <div style="margin-top:15px; border-top: 1px solid #eee; padding-top:10px;">
                            <a href="https://play.google.com/store/books/details?id=9IG-EQAAQBAJ" target="_blank">
                                <img src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" style="width:130px;" alt="Get eBook">
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            """

        # --- UNIVERSAL TEMPLATE ---
        html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <style>
        :root {{ --blue: #1a73e8; --red: #d93025; --green: #1e8e3e; --text: #202124; }}
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #f8f9fa; margin: 0; color: var(--text); line-height: 1.6; }}
        .header {{ background: #fff; border-bottom: 3px solid var(--blue); padding: 20px; text-align: center; }}
        .container {{ max-width: 550px; margin: 25px auto; padding: 0 15px; }}
        .card {{ background: #fff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 30px; }}
        h1 {{ font-size: 22px; color: var(--blue); margin: 10px 0; text-transform: capitalize; }}
        .badge {{ background: #e8f0fe; color: var(--blue); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
        .badge-green {{ background: #e6f4ea; color: var(--green); }}
        .cta-box {{ border: 2px solid var(--red); background: #fff5f5; border-radius: 10px; padding: 20px; text-align: center; margin: 20px 0; }}
        .phone-link {{ display: block; font-size: 28px; color: var(--red); text-decoration: none; font-weight: 800; margin: 5px 0; }}
        .btn {{ display: inline-block; padding: 10px 18px; color: #fff; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 8px; font-size: 14px; text-align: center; }}
        .btn-red {{ background: var(--red); width: 80%; }}
        .book-card {{ border: 1px solid #dadce0; border-radius: 10px; padding: 20px; background: #fcfcfc; }}
        .book-flex {{ display: flex; gap: 20px; align-items: flex-start; }}
        .book-img {{ width: 80px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
        footer {{ text-align: center; padding: 30px; font-size: 12px; color: #70757a; }}
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin:0; color:var(--blue);">{company_name}</h2>
        <div style="font-size:12px; font-weight:bold; color:#5f6368;">{tagline}</div>
    </div>
    <div class="container">
        <div class="card">{specific_content}</div>
    </div>
    <footer>
        © 2026 {company_name} Professional Services<br>
        Serving {city}, {zip_code} and Nationwide.
    </footer>
</body>
</html>"""

        with open(f"services/{slug}.html", "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"✅ Created {category.upper()}: {slug}")

if __name__ == "__main__":
    print("🚀 Starting Daily Batch: Generating 190 pages...")
    
    # Each loop creates 2 pages (1 plumbing + 1 book)
    # 95 loops * 2 pages = 190 total URLs
    for i in range(95):
        build_and_index()
    
    print("🏁 190 pages created. Ready for GitHub push and Google notification.")
