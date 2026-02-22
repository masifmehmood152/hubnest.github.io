import os
import json
import random
import pandas as pd
import string
import httplib2
import requests
import time
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build # You may need: pip install google-api-python-client

# --- CONFIGURATION ---
BASE_URL = "https://serviceshubnest.github.io/hubnest.github.io/"
SERVICES_DIR = 'services'
LOG_FILE = "indexed_urls.txt"

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
    
    with open(".nojekyll", "w") as f: f.write("")
    print("✅ Sitemap and .nojekyll updated.")

def submit_sitemap_to_gsc(base_url, credentials):
    """Officially notifies Google of a Sitemap update via Search Console API."""
    try:
        # Build the Search Console service
        service = build('webmasters', 'v3', credentials=credentials)
        sitemap_url = f"{base_url}sitemap.xml"
        
        # Google expects the 'siteUrl' to match exactly how it's defined in GSC 
        # (usually including the trailing slash)
        service.sitemaps().submit(siteUrl=base_url, feedpath=sitemap_url).execute()
        print(f"🚀 Google API: Sitemap submission successful for {sitemap_url}")
    except Exception as e:
        print(f"⚠️ Sitemap submission failed: {e}")

def notify_google(base_url):
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    if not json_creds:
        print("❌ GOOGLE_CREDENTIALS Secret is missing!")
        return

    # API Setup - Adding the webmasters scope for Sitemap submission
    scopes = [
        "https://www.googleapis.com/auth/indexing",
        "https://www.googleapis.com/auth/webmasters" # Required for Sitemap API
    ]
    creds_dict = json.loads(json_creds)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    
    # 1. First, submit the Sitemap (The broad update)
    submit_sitemap_to_gsc(base_url, credentials)

    # 2. Then, handle individual Page Indexing (The fast update)
    indexed_files = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            indexed_files = set(f.read().splitlines())

    all_files = [f for f in os.listdir(SERVICES_DIR) if f.endswith('.html')]
    new_files = [f for f in all_files if f not in indexed_files]

    if not new_files:
        print("⏭️ No new individual pages to index.")
        return

    http = credentials.authorize(httplib2.Http())
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"

    for file_name in new_files:
        full_url = f"{base_url}{SERVICES_DIR}/{file_name}"
        try:
            live_check = requests.get(full_url, timeout=10)
            if live_check.status_code != 200:
                print(f"⚠️ {file_name} not live. Skipping.")
                continue
        except: continue

        body = json.dumps({"url": full_url, "type": "URL_UPDATED"})
        response, content = http.request(endpoint, method="POST", body=body)
        
        if response.status == 200:
            print(f"✅ Google Notified: {full_url}")
            with open(LOG_FILE, "a") as f: f.write(file_name + "\n")
        elif response.status == 429:
            print("🛑 Quota Limit Reached.")
            break

if __name__ == "__main__":
    BASE_URL = "https://serviceshubnest.github.io/hubnest.github.io/"
    print("🚀 Generating Pages...")
    # build_and_index() 
    update_sitemap_xml(BASE_URL)
    print("📢 Notifying Google of updates...")
    notify_google(BASE_URL)
