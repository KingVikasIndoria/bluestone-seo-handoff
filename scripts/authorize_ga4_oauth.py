#!/usr/bin/env python3
"""
OAuth Authorization Helper for Google Analytics 4
=================================================
Allows authorizing GA4 access using your personal/company Google account.
Saves token to scripts/ga4_token.json.
"""

import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCRIPT_DIR = Path(__file__).parent
CLIENT_SECRET_FILE = SCRIPT_DIR / "client_secret.json"
GA4_TOKEN_FILE = SCRIPT_DIR / "ga4_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly"
]

def authorize():
    if not CLIENT_SECRET_FILE.exists():
        print(f"❌ client_secret.json not found at {CLIENT_SECRET_FILE}")
        return False
        
    print("🔐 Launching Google OAuth authorization in your browser...")
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
    creds = flow.run_local_server(port=8088)
    
    with open(GA4_TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(creds.to_json())
        
    print(f"✅ Successfully authorized GA4! Token saved to {GA4_TOKEN_FILE}")
    return True

if __name__ == "__main__":
    authorize()
