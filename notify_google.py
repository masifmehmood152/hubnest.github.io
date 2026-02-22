import os
import json
import httplib2
import requests  # Added for the Live Page check
from oauth2client.service_account import ServiceAccountCredentials

def notify_google():
    # 1. Setup Google Credentials
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    if not json_creds:
        print("❌ GOOGLE_CREDENTIALS Secret is missing!")
        return
    # --- ADD THIS HERE ---
    log_file = "indexed_urls.txt"
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            pass # Creates an empty file so Git doesn't crash
        print(f"📄 Initialized {log_file}")
    # --------------------
    scopes = ["https://www.googleapis.com/auth/indexing"]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(json_creds), scopes)
        http = credentials.authorize(httplib2.Http())
        endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"

        # --- NEW: MEMORY LOGIC ---
        log_file = "indexed_urls.txt"
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                indexed_files = set(f.read().splitlines())
        else:
            indexed_files = set()

        # 2. Find the files
        if not os.path.exists('services'):
            print("❌ No services folder found.")
            return

        # NEW: Filter so we ONLY see files that haven't been indexed yet
        all_files = [f for f in os.listdir('services') if f.endswith('.html')]
        new_files = [f for f in all_files if f not in indexed_files]
        
        if not new_files:
            print("⏭️ No new HTML files to index. Skipping.")
            return

        print(f"🔍 Found {len(new_files)} NEW files to index. (Total files: {len(all_files)})")

        # 3. Notify Google for each NEW file
        for file_name in new_files:
            # Match your URL structure
            full_url = f"https://serviceshubnest.github.io/hubnest.github.io/services/{file_name}"
            
            # --- NEW: 120s SAFETY CHECK ---
            # Verify the page is actually LIVE on GitHub before telling Google
            try:
                live_check = requests.get(full_url, timeout=10)
                if live_check.status_code != 200:
                    print(f"⚠️ {file_name} not live yet (Status {live_check.status_code}). Skipping.")
                    continue
            except:
                continue

            # 4. SEND TO GOOGLE
            content = json.dumps({"url": full_url, "type": "URL_UPDATED"})
            response, content_resp = http.request(endpoint, method="POST", body=content)
            
            if response.status == 200:
                print(f"✅ Google Notified: {full_url}")
                # --- NEW: UPDATE LOG ---
                with open(log_file, "a") as f:
                    f.write(file_name + "\n")
            elif response.status == 429:
                print("🛑 Quota Limit Reached.")
                break
            else:
                print(f"⚠️ Status {response.status} for {file_name}")

    except Exception as e:
        print(f"❌ Indexing Error: {e}")

if __name__ == "__main__":
    notify_google()
