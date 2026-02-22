import os
import json
import random
import pandas as pd
import string
import httplib2
import requests
import time
from oauth2client.service_account import ServiceAccountCredentials

# ... (Keep your existing keyword lists and generate_uid here) ...

def update_sitemap_xml(base_url):
    """Generates a clean, raw XML sitemap."""
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    xml_content.append(f'  <url><loc>{base_url}</loc></url>')
    
    if os.path.exists('services'):
        for file in os.listdir('services'):
            if file.endswith(".html"):
                xml_content.append(f'  <url><loc>{base_url}services/{file}</loc></url>')
    
    xml_content.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_content))
    # Crucial: Create .nojekyll so Google can read the XML
    with open(".nojekyll", "w") as f: f.write("")
    print("✅ Sitemap and .nojekyll updated.")

def notify_google(base_url):
    # ... (Insert your notify_google logic here) ...
    # IMPORTANT: Keep that 'requests.get' check you added! 
    # It prevents Google from seeing 404s if GitHub is slow.
    pass

if __name__ == "__main__":
    BASE_URL = "https://serviceshubnest.github.io/hubnest.github.io/"
    
    # STEP 1: Generate new content
    print("🚀 Generating Pages...")
    # build_and_index() logic here...

    # STEP 2: Update Sitemap
    update_sitemap_xml(BASE_URL)

    # STEP 3: Notify Google (Only for existing live pages)
    print("📢 Notifying Google of NEW live pages...")
    notify_google(BASE_URL)
