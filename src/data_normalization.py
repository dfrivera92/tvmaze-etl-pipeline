import pandas as pd

class TVMazeDataNormalizer:
    def __init__(self, parquet_file_path):
        """
        Initializes the transformer with the path to the Parquet file.
        
        Args:
            parquet_file_path (str): Path to the Parquet file to process.
        """
        self.parquet_file_path = parquet_file_path
        self.df = self._read_parquet_file()
        self.transformed_data = {}

    def _read_parquet_file(self, engine="pyarrow"):
        """Reads a Parquet file into a Pandas DataFrame."""
        try:
            df = pd.read_parquet(self.parquet_file_path, engine=engine)
            print(f"Successfully read file: {self.parquet_file_path}")
            return df
        except FileNotFoundError:
            print(f"Error: File not found at {self.parquet_file_path}")
        except ValueError as e:
            print(f"Error: {e} (Try using engine='fastparquet')")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None

    def _create_lookup_table(self, column_name, rename_map=None, sort_column=None):
        """Creates a lookup table with unique values from a DataFrame column."""
        df_lookup = self.df[[column_name]].drop_duplicates().dropna()
        if rename_map:
            df_lookup.rename(columns=rename_map, inplace=True)
        if column_name == 'show_genres':
            df_lookup = df_lookup.explode(rename_map[column_name]).dropna().drop_duplicates()
        if sort_column:
            df_lookup = df_lookup.sort_values(by=sort_column)

        df_lookup = df_lookup.reset_index(drop=True)
        df_lookup.insert(0, 'id', range(1, len(df_lookup) + 1))
        return df_lookup

    def _explode_and_map(self, column_name, lookup_df, lookup_key, new_column_name):
        """Explodes a list column and maps it to an ID from a lookup DataFrame."""
        lookup_map = lookup_df.set_index(lookup_key)["id"]
        exploded_df = self.df[['tvmaze_id', column_name]].explode(column_name).dropna()
        exploded_df.rename(columns={'tvmaze_id': 'show_id'}, inplace=True)
        exploded_df[new_column_name] = exploded_df[column_name].map(lookup_map)
        return exploded_df[['show_id', new_column_name]]

    def transform(self):
        """Performs data normalization and transformation."""
        if self.df is None:
            return None

        # Lookup tables
        self.transformed_data['show_types'] = self._create_lookup_table("show_type", sort_column="show_type")
        self.transformed_data['languages'] = self._create_lookup_table("show_language", {"show_language": "language"}, "language")
        self.transformed_data['genres'] = self._create_lookup_table("show_genres", {"show_genres": "genre"}, 'genre')
        self.transformed_data['statuses'] = self._create_lookup_table("show_status", {"show_status": "status"}, "status")

        # Schedule days lookup
        day_order = ['Unknown', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        schedule_days = self.df[["show_schedule_days"]].explode("show_schedule_days").dropna().drop_duplicates()
        schedule_days['show_schedule_days'] = pd.Categorical(schedule_days['show_schedule_days'], categories=day_order, ordered=True)
        schedule_days.rename(columns={"show_schedule_days": "day_name"}, inplace=True)
        self.transformed_data['schedule_days'] = schedule_days.reset_index(drop=True)
        self.transformed_data['schedule_days'].insert(0, 'id', range(1, len(self.transformed_data['schedule_days']) + 1))

        # Add ID mappings to main DataFrame
        self.df["language_id"] = self.df["show_language"].map(self.transformed_data['languages'].set_index("language")["id"])
        self.df["show_type_id"] = self.df["show_type"].map(self.transformed_data['show_types'].set_index("show_type")["id"])
        self.df["status_id"] = self.df["show_status"].map(self.transformed_data['statuses'].set_index("status")["id"])

        # Process main 'shows' DataFrame
        self.transformed_data['shows'] = self.df[[
            'tvmaze_id', 'show_name', 'tvmaze_url', 'average_runtime_minutes', 'premiere_date',
            'end_date', 'show_tvmaze_weight', 'show_summary', 'last_updated_utc',
            'imdb_id', 'image_medium_url', 'image_original_url', 'language_id',
            'show_type_id', 'status_id'
        ]].sort_values(by="tvmaze_id").reset_index(drop=True)

        # Junction tables
        self.transformed_data['show_genres'] = self._explode_and_map("show_genres", self.transformed_data['genres'], "genre", "genre_id")
        self.transformed_data['show_schedule_days'] = self._explode_and_map("show_schedule_days", self.transformed_data['schedule_days'], "day_name", "day_id")

        return self.transformed_data
