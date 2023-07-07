import os
import csv
import datetime

# Define the path to the CSV file
backlog_file_path = '_data/planning-concerns-backlog.csv'
backup_file_path = '_data/planning-concerns-backlog.backup.csv'

# Define the path to the log.csv file
log_file_path = '_data/backlog-changelog.csv'

# Get today's date
today = datetime.date.today()


def delete_backup():
    try:
        os.remove(backup_file_path)
        print('Backup deleted successfully!')
    except OSError as e:
        print(f'Error deleting the backup file: {e}')

def get_log_rows(): 
    rows = []
    with open(log_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows

def write_log(fieldnames, rows):
    with open(log_file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def list_concerns(file_path):
    concerns = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            value = row['Concern']
            concerns.append(value)

    return concerns

def get_changes(current, original):
    added = set(current).difference(original)
    removed = set(original).difference(current)

    return added, removed

def log_changes():
    # Read concerns from latest and backup csv
    original_concerns = list_concerns(backup_file_path)
    current_concerns = list_concerns(backlog_file_path)
    current_count = len(current_concerns)

    # work out which concerns have been added and which have been removed
    added, removed = get_changes(current_concerns, original_concerns)

    # record any changes to log
    if len(added) or len(removed):
        fieldnames = ['date', 'count', 'added', 'removed']
        # get rows from log
        rows = get_log_rows()

        new_row = {
            'date': today.strftime('%Y-%m-%d'),
            'count': current_count,
            'added': ';'.join(added),
            'removed': ';'.join(removed)
        }

        rows.append(new_row)
        write_log(fieldnames, rows)

    # delete backup file
    delete_backup()

