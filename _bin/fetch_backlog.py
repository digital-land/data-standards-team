import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Load the credentials from the JSON file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

google_credentials = {
  "type": "service_account",
  "project_id": "data-standards-389209",
  "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
  "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
  "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
  "client_id": os.getenv("GOOGLE_CLIENT_ID"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/data-standards-team-bot%40data-standards-389209.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

gc = gspread.service_account_from_dict(google_credentials)

# Open the worksheet by its title
spreadsheet = gc.open('The grid')
worksheet = spreadsheet.worksheet('planning-concerns')

# Read all the data from the worksheet
data = worksheet.get_all_values()

# Create a pandas DataFrame from the data
df = pd.DataFrame(data)

# Remove the third row (index 2)
df = df.drop(0)
df = df.drop(2)

# Save the DataFrame as a CSV file
# index removes the row indices 
# header removes the column indices
df.to_csv('_data/planning-concerns-backlog.csv', index=False, header=False)
