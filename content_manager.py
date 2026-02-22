import os
import json
import random
import pandas as pd
import shutil

# ==========================================
# 🔥 1. KEYWORD LISTS
# ==========================================
problem_intent = ["Fix", "Repair", "Emergency Repair", "24/7 Repair", "Immediate Fix", "Stop Leak Now", "Call Now for Repair"]
service_types = ["Plumber", "Drain Cleaning", "Burst Pipe Repair", "Water Heater Installation", "Sewer Line Replacement", "Slab Leak Repair", "Toilet Repair"]
location_modifiers = ["{city}", "{zip_code}", "Near Me", "Local", "Available Now"]

ULTRA_PLUMBING_KEYWORDS = [f"{i} {s} {l}" for i in problem_intent for s in service_types for l in location_modifiers]

problem_intent_book = ["Overcoming Self-Doubt", "Stop Overthinking", "Build Confidence", "Improve Social Skills"]
buyer_modifiers = ["Book", "Guide", "Blueprint", "Practical Guide"]
audience_modifiers = ["for Professionals", "for Introverts", "for Leaders", "for Career Growth"]

ALL_EXPANDED_BOOK_KEYWORDS = [f"{b} {p} {a}" for b in buyer_modifiers for p in problem_intent_book for a in audience_modifiers]

# ==========================================
# 🛠️ 2. PAGE BUILDER LOGIC
# ==========================================
def build_and_index():
    # 🧹 CLEANUP: Only notify Google about NEW pages
    if os.path.exists('services'):
        shutil.rmtree('services')
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

        if category == "plumbing":
            # --- 📞 PLUMBING DESIGN ---
            keyword = random.choice(ULTRA_PLUMBING_KEYWORDS).format(city=city, zip_code=zip_code)
            page_title = f"{company_name} Plumbing: Affordable Local Plumber in {city}"
            slug = f"plumber-{city.lower().replace(' ', '-')}-{zip_code}"
            
            main_content = f"""
            <span class="badge">📍 LOCAL SERVICE: {city}</span>
            <h1>{keyword}</h1>
            <p>Licensed plumbing experts providing fast, same-day, affordable services when you need them most. We specialize in everything from emergency repairs to routine maintenance.</p>
            
            <div class="cta-box">
                <p>LICENSED • BONDED • INSURED</p>
                <strong>FREE ESTIMATE & 24/7 DISPATCH</strong>
                <a href="tel:3085508314" class="phone-link">{phone}</a>
                <a href="tel:3085508314" class="btn btn-red">Call For Service</a>
            </div>

            <ul class="features">
                <li>✅ <b>Same Day:</b> Fast response in {city}.</li>
                <li>✅ <b>24/7:</b> Emergency repairs available now.</li>
                <li>✅ <b>Upfront:</b> Honest pricing, no hidden fees.</li>
            </ul>
            """
        else:
            # --- 📖 BOOK DATA (Ebook + Audiobook) ---
            keyword = random.choice(ALL_EXPANDED_BOOK_KEYWORDS)
            page_title = f"{keyword} | Official {company_name} Guide"
            slug = f"book-{keyword.lower().replace(' ', '-')}-{zip_code}"
            
            content_html = f"""
            <span class="location-badge" style="background:#e6f4ea; color:#1e8e3e;">📖 Official Publication</span>
            <h1>{keyword}</h1>
            <p>Master the blueprint for confidence and leadership. Curated by the <b>{company_name}</b> network for professionals in {city}.</p>
            
            <div class="book-card">
                <div class="book-flex">
                    <img src="https://m.media-amazon.com/images/I/41-A8mN-DmL._SY445_SX342_.jpg" class="book-img" alt="Book Cover">
                    
                    <div class="book-info">
                        <h3 style="margin:0 0 5px 0; font-size:18px;">{book_title}</h3>
                        <p style="margin:0; font-size:14px; color:#5f6368;">By <b>Asif Mehmood</b></p>
                        
                        <div style="margin-top:18px; border-top: 1px solid #eee; padding-top:10px;">
                            <span style="font-size:11px; font-weight:bold; color:#1e8e3e; display:block; margin-bottom:5px;">📄 DIGITAL E-BOOK</span>
                            <a href="https://play.google.com/store/books/details?id=9IG-EQAAQBAJ" target="_blank">
                                <img src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" style="width:140px;" alt="Get eBook on Google Play">
                            </a>
                        </div>

                        <div style="margin-top:12px; border-top: 1px solid #eee; padding-top:10px;">
                            <span style="font-size:11px; font-weight:bold; color:#1a73e8; display:block; margin-bottom:5px;">🎧 AUDIOBOOK VERSION</span>
                            <a href="https://play.google.com/store/audiobooks/details?id=AQAAAEAaNSp1IM" target="_blank">
                                <img src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" style="width:140px;" alt="Get Audiobook on Google Play">
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            """

        # --- UNIVERSAL TEMPLATE ---
        html = f"""<!DOCTYPE html>
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
        h1 {{ font-size: 22px; color: var(--blue); margin: 10px 0; }}
        .badge {{ background: #e8f0fe; color: var(--blue); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
        .badge-green {{ background: #e6f4ea; color: var(--green); }}
        
        /* Plumber CTA */
        .cta-box {{ border: 2px solid var(--red); background: #fff5f5; border-radius: 10px; padding: 20px; text-align: center; margin: 20px 0; }}
        .phone-link {{ display: block; font-size: 28px; color: var(--red); text-decoration: none; font-weight: 800; margin: 5px 0; }}
        
        /* Book Feature */
        .book-card {{ border: 1px solid #dadce0; border-radius: 10px; padding: 20px; background: #fcfcfc; }}
        .book-flex {{ display: flex; gap: 20px; align-items: flex-start; }}
        .book-img {{ width: 100px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
        .stars {{ color: #f4b400; margin-bottom: 10px; }}
        
        /* Buttons */
        .btn {{ display: inline-block; padding: 10px 18px; color: #fff; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 8px; font-size: 14px; text-align: center; }}
        .btn-red {{ background: var(--red); width: 80%; }}
        .btn-green {{ background: var(--green); }}
        .btn-blue {{ background: var(--blue); }}
        
        .features {{ list-style: none; padding: 0; }}
        .features li {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
        footer {{ text-align: center; padding: 30px; font-size: 12px; color: #70757a; }}
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin:0; color:var(--blue);">{company_name}</h2>
        <div style="font-size:12px; font-weight:bold; color:#5f6368;">{tagline}</div>
    </div>
    <div class="container">
        <div class="card">
            {main_content}
        </div>
    </div>
    <footer>
        © 2026 {company_name} Professional Services<br>
        Serving {city}, {zip_code} and Nationwide.
    </footer>
</body>
</html>"""

        with open(f"services/{slug}.html", "w", encoding="utf-8") as f:
            f.write(html)

if __name__ == "__main__":
    print("🎬 Starting Pro Build...")
    build_and_index()
    print("✅ Finished. Ready for Google.")
