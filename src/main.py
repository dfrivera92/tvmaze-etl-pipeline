from datetime import datetime
from data_ingestion import TVMazeDataFetcher

# Data ingestion
year_month = input("Enter year and month (YYYY-MM): ").strip()

while True:
    try:
        datetime.strptime(year_month, "%Y-%m")
        break
    except ValueError:
        year_month = input("Invalid format. Please enter as YYYY-MM: ").strip()

fetcher = TVMazeDataFetcher()
fetcher.fetch_data(year_month)
print(f"\n\nFetched shows for {year_month}")

# Data processing
