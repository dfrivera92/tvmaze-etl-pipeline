import json
import pandas as pd
import os

class TVMazeDataProcessor:
    def __init__(self, json_dir=None):
        """
        Initializes the TVMazeDataProcessor class.
        
        Args:
            json_dir (str, optional): Directory where JSON files are stored. 
                                      Defaults to a 'json' folder in the project's root directory.
        """
        if json_dir is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_dir = os.path.join(project_root, "json")
        
        self.json_dir = json_dir

    def get_json_files(self, substring):
        """
        Retrieves JSON files containing TV show data that match a given substring.
        
        Args:
            substring (str): Substring to match in file names.
        
        Returns:
            list: List of matching JSON file paths.
        """
        return [
            os.path.join(self.json_dir, f) 
            for f in os.listdir(self.json_dir) 
            if f.endswith('.json') and substring in f
        ]

    def tv_shows_to_dataframe(self, json_files):
        """
        Processes multiple JSON files containing TV show data and extracts relevant information.
        
        Args:
            json_files (list): List of JSON file paths to process.
        
        Returns:
            pd.DataFrame: DataFrame containing the extracted TV show data.
        """
        all_series = []
        series_ids = set() 
        
        for file_path in json_files:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            for show in data:
                if '_embedded' in show and 'show' in show['_embedded']:
                    show_data = show['_embedded']['show']
                    if show_data.get('id') not in series_ids:
                        all_series.append(show_data)
                        series_ids.add(show_data['id'])
        
        return pd.json_normalize(all_series)

    def process_tv_shows(self, substring):
        """
        Main function to find and process JSON files containing TV show data.
        
        Args:
            substring (str): Substring to filter JSON files.
        
        Returns:
            pd.DataFrame: DataFrame containing TV show data.
        """
        json_files = self.get_json_files(substring)
        
        if not json_files:
            print(f"No JSON files found for date substring '{substring}'")
            return None

        return self.tv_shows_to_dataframe(json_files)
