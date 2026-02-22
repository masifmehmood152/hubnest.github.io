import os
import json
import random
import pandas as pd
import string
import httplib2
import requests
import time
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURATION ---
BASE_URL = "https://serviceshubnest.github.io/hubnest.github.io/"
SERVICES_DIR = 'services'
LOG_FILE = "indexed_urls.txt"

def generate_uid(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def update_sitemap_xml(base_url):
    """Generates a clean, raw XML sitemap and .nojekyll file."""
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    xml_content.append(f'  <url><loc>{base_url}</loc></url>')
    
    if os.path.exists(SERVICES_DIR):
        for file in os.listdir(SERVICES_DIR):
            if file.endswith(".html"):
                xml_content.append(f'  <url><loc>{base_url}{SERVICES_DIR}/{file}</loc></url>')
    
    xml_content.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_content))
    
    # Crucial for Google Search Console to read raw XML
    with open(".nojekyll", "w") as f: f.write("")
    print("✅ Sitemap and .nojekyll updated.")

def notify_google(base_url):
    """Notifies Google Indexing API only for pages that are verified LIVE."""
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    if not json_creds:
        print("❌ GOOGLE_CREDENTIALS Secret is missing!")
        return

    # Load previously indexed files
    indexed_files = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            indexed_files = set(f.read().splitlines())

    # Find new files
    all_files = [f for f in os.listdir(SERVICES_DIR) if f.endswith('.html')]
    new_files = [f for f in all_files if f not in indexed_files]

    if not new_files:
        print("⏭️ No new pages to index.")
        return

    # API Setup
    scopes = ["https://www.googleapis.com/auth/indexing"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(json_creds), scopes)
    http = credentials.authorize(httplib2.Http())
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"

    for file_name in new_files:
        full_url = f"{base_url}{SERVICES_DIR}/{file_name}"
        
        # --- THE LIVE CHECK ---
        # This ensures Google only visits if the file is actually on GitHub
        try:
            live_check = requests.get(full_url, timeout=10)
            if live_check.status_code != 200:
                print(f"⚠️ {file_name} not live on GitHub yet. Skipping notification.")
                continue
        except:
            continue

        # Send to Google
        body = json.dumps({"url": full_url, "type": "URL_UPDATED"})
        response, content = http.request(endpoint, method="POST", body=body)
        
        if response.status == 200:
            print(f"✅ Google Notified: {full_url}")
            with open(LOG_FILE, "a") as f:
                f.write(file_name + "\n")
        elif response.status == 429:
            print("🛑 Quota Limit Reached.")
            break

# ==========================================
# EXECUTION LOGIC
# ==========================================
if __name__ == "__main__":
    # 1. Generate new content (Your build_and_index logic)
    print("🚀 Generating Pages...")
    # build_and_index()  # <--- Call your generator here

    # 2. Update Sitemap (Always do this before notifying)
    update_sitemap_xml(BASE_URL)

    # 3. Notify Google
    # NOTE: On the very first run, this might skip because GitHub isn't updated.
    # The next 30-min run will pick them up and index them.
    print("📢 Running Google Indexing check...")
    notify_google(BASE_URL)
