#%%
import requests
from datetime import datetime, timedelta
import time
import calendar
import json
import os
#%%
class TVMazeDataFetcher:
    """
    A class to fetch TV show data from the TVmaze API for a given month.
    """
    BASE_URL = "http://api.tvmaze.com/schedule/web"
    BATCH_SIZE = 20   # Max requests per rate limit window
    DELAY = 10        # Rate limit window in seconds

    def __init__(self, json_dir=None):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.json_dir = json_dir or os.path.join(self.project_root, "json")
        os.makedirs(self.json_dir, exist_ok=True)

    def fetch_data(self, year_month):
        """
        Fetches all unique TV shows aired in a specific month from TVmaze API.
        
        Args:
            year_month (str): Format "YYYY-MM" (e.g., "2024-12")
        """
        try:
            year, month = map(int, year_month.split('-'))
        except ValueError:
            raise ValueError("Invalid year-month format. Please use 'YYYY-MM'")

        _, num_days = calendar.monthrange(year, month)
        start_date = datetime(year, month, 1)
        request_count = 0

        print(f"\nFetching shows for {year_month} ({num_days} days)...")
        
        for day in range(num_days):
            current_date = start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            
            try:
                response = requests.get(f"{self.BASE_URL}?date={date_str}", timeout=10)
                response.raise_for_status()
                schedule_data = response.json()
                
                self._save_to_json(date_str, schedule_data)
                print(f"{date_str}", end=' ', flush=True)
                
                request_count += 1
                if request_count % self.BATCH_SIZE == 0:
                    print(f"\nMade {request_count} requests. Waiting {self.DELAY} seconds...")
                    time.sleep(self.DELAY)
            
            except requests.exceptions.RequestException as e:
                print(f"\nError fetching data for {date_str}: {e}")
                time.sleep(self.DELAY)
                continue
    
    def _save_to_json(self, date_str, data):
        """
        Save the fetched data to a JSON file.

        Args:
            date_str (str): The date string used as the filename.
            data (dict or list): The data to be saved in JSON format.

        Saves:
            A JSON file named '<date_str>.json' in the specified directory.
        """
        file_path = os.path.join(self.json_dir, f"{date_str}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
# %%
