'''
log 1 is the first attempt, it is a very basic form with hard coded locations for the log file path
and the extracted data path
'''

import re
import csv
from datetime import datetime

# File paths
log_file_path = 'C:/Users/alexa/OneDrive/Desktop/log/acc.txt'  # Adjust the path to your actual log file path
csv_file_path = 'C:/Users/alexa/OneDrive/Desktop/log/extracted_data.csv'

#pattern to extract date, IP address, host, method, and time zone (regex)
log_pattern = re.compile(
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) - (?P<host>\S+) \[(?P<date>[^\]:]+):(?P<time>[^\] ]+)(?P<timezone>[^\]]+)\] "(?P<method>\S+)'
)

def extract_log_data(log_file_path):
    extracted_data = []
    
    try:
        with open(log_file_path, 'r') as file:
            for line in file:
                match = log_pattern.search(line)
                if match:
                    log_entry = {
                        'date': match.group('date'),
                        'time': match.group('time'),
                        'timezone': match.group('timezone'),
                        'ip': match.group('ip'),
                        'host': match.group('host'),
                        'method': match.group('method')
                    }
                    extracted_data.append(log_entry)
    except PermissionError:
        print(f"Permission denied: '{log_file_path}'. Please check the file permissions.")
    except FileNotFoundError:
        print(f"File not found: '{log_file_path}'. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return extracted_data

def write_to_csv(data, csv_file_path):
    # Sort data by date and time
    sorted_data = sorted(data, key=lambda x: datetime.strptime(f"{x['date']} {x['time']} {x['timezone']}", '%d/%b/%Y %H:%M:%S %z'))
    
    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['date', 'time', 'timezone', 'ip', 'host', 'method']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for entry in sorted_data:
                writer.writerow(entry)
    except PermissionError:
        print(f"Permission denied: '{csv_file_path}'. Please check the file permissions.")
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

def main():
    log_data = extract_log_data(log_file_path)
    if log_data:
        write_to_csv(log_data, csv_file_path)
        print(f"Extracted data has been written to {csv_file_path}")

if __name__ == "__main__":
    main()
