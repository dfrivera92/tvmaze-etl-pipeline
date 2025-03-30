#%%
from datetime import datetime
from data_ingestion import TVMazeDataFetcher
from data_processing import TVMazeDataProcessor
from data_profiling import TVMazeDataProfiler
from data_cleaning import TVMazeDataCleaner
from data_export import ParquetExporter
from data_normalization import TVMazeDataNormalizer
from db_loader import SQLiteDB

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
data_processor = TVMazeDataProcessor()
processed_df = data_processor.process_tv_shows(year_month)

# Data profiling
data_profiler = TVMazeDataProfiler()
profile_path = data_profiler.generate_profile_report(processed_df)

# Data cleaning
data_cleaner = TVMazeDataCleaner(processed_df)
cleaned_df = data_cleaner.clean_data()

# Data export
exporter = ParquetExporter()
parquet_file_path = exporter.export_to_parquet(cleaned_df, filename=f"tvmaze_data_{year_month}.parquet")

# Data normalization
data_normalizer = TVMazeDataNormalizer(parquet_file_path)
normalized_data = data_normalizer.transform()

# Upload data
db = SQLiteDB()
for table, df in normalized_data.items():
    db.insert_dataframe(df, table)
db.close_connection()
print(f"\n\nData uploaded to SQLite database successfully.")

# Data Analysis
df_avg_runtime = db.run_query("SELECT ROUND(AVG(average_runtime_minutes),2) AS avg_runtime FROM shows")
print(f"\n\nAverage runtime of shows: {df_avg_runtime['avg_runtime'][0]}min")

query_genre_count = """
SELECT 
    g.genre,
    COUNT(sg.show_id) AS show_count
FROM shows s
LEFT JOIN show_genres sg ON s.tvmaze_id = sg.show_id
LEFT JOIN genres g ON sg.genre_id = g.id
GROUP BY g.genre
ORDER BY show_count DESC
"""
df_genre_count = db.run_query(query_genre_count)
print("\n\nGenre count:")
print(df_genre_count.to_string(index=False))

df_unique_domains = db.run_query("SELECT DISTINCT(official_site_url) AS official_site_url FROM shows")
print(f"\n\nUnique official sites domains:")
print("\n".join(df_unique_domains["official_site_url"].astype(str)))