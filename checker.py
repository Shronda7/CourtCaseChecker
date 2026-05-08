import os

# Define the target directory and filename
folder_path = r'D:\CourtCaseChecker'
file_name = 'checker.py'
full_path = os.path.join(folder_path, file_name)

# The code content for your case checker
code_content = """import os
import json
from court_scraper import Site
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# --- CONFIGURATION ---
CASE_NUMBER = '2023-CF-000123'
COURT_ID = 'wi_milwaukee' # Example: Milwaukee, WI
DB_FILE = os.path.join('data', 'case_history.json')
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    \"\"\"Authenticates and returns the Google Calendar service.\"\"\"
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('calendar', 'v3', credentials=creds)

def scrape_case_data():
    \"\"\"Extracts the latest status using court-scraper.\"\"\"
    site = Site(COURT_ID)
    results = site.search(case_number=CASE_NUMBER)
    return results[0]

def update_calendar(event_details):
    \"\"\"Creates a new event on Google Calendar.\"\"\"
    service = get_calendar_service()
    event = {
        'summary': f"Court Hearing: {CASE_NUMBER}",
        'description': f"Status: {event_details.get('status')}",
        'start': {'date': event_details.get('filing_date')},
        'end': {'date': event_details.get('filing_date')},
    }
    service.events().insert(calendarId='primary', body=event).execute()
    print("Calendar updated.")

def main():
    if not os.path.exists('data'):
        os.makedirs('data')
        
    current_data = scrape_case_data()
    
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            history = json.load(f)
    else:
        history = {}

    last_status = history.get(CASE_NUMBER, {}).get('status')
    if current_data['status'] != last_status:
        print(f"Update detected! New status: {current_data['status']}")
        update_calendar(current_data)
        
        history[CASE_NUMBER] = current_data
        with open(DB_FILE, 'w') as f:
            json.dump(history, f)
    else:
        print("No changes detected.")

if __name__ == "__main__":
    main()
"""

# Check if the folder exists, if not, create it
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Created directory: {folder_path}")

# Write the code to the file
with open(full_path, 'w') as f:
    f.write(code_content)

print(f"Successfully saved {file_name} to {full_path}")
