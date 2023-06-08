import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Load the credentials from the JSON file
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# credentials = ServiceAccountCredentials.from_json_keyfile_name('data-standards-389209-6bf7855d074f.json', scope)

# Authorize the client
# client = gspread.authorize(credentials)

gc = gspread.service_account()

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
