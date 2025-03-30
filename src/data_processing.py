#%%
import json
import pandas as pd
import os

def get_json_files(json_dir, substring):
    return [
        os.path.join(json_dir, f) 
        for f in os.listdir(json_dir) 
        if f.endswith('.json') and substring in f
        ]

def tv_shows_to_dataframe(json_files):
    """
    Process multiple JSON files containing TV show data and extract relevant information.
    
    Args:
        json_files (list): List of JSON file paths to process
        
    Returns:
        tuple: (list of processed shows, list of unique show IDs)
    """
    all_series = []
    series_ids = []
    
    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            
        for show in data:
            if '_embedded' in show and 'show' in show.get('_embedded', {}):
                show_data = show['_embedded']['show']
                if not show_data.get('id') in series_ids:
                    all_series.append(show_data)
                    series_ids.append(show_data['id'])
    
    return pd.json_normalize(all_series)

def main(substring):

    project_root = project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    json_dir = os.path.join(project_root, "json")
    json_files = get_json_files(json_dir, substring)

    if not json_files:
        print(f"No JSON files found for date substring '{substring}'")
        return None

    df = tv_shows_to_dataframe(json_files)
    return df
