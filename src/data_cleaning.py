import pandas as pd

class TVMazeDataCleaner:
    def __init__(self, df):
        """
        Initializes the TVMazeDataCleaner with a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing raw TV show data.
        """
        self.df = df

    def clean_data(self):
        """
        Cleans the TV show data by:
        - Dropping unnecessary columns
        - Renaming columns for better readability
        - Handling missing values
        - Converting data types

        Returns:
            pd.DataFrame: The cleaned DataFrame
        """
        columns_to_drop = [
            'runtime', 'officialSite', 'dvdCountry', 'schedule.time', 'rating.average',
            'externals.tvrage', 'externals.thetvdb', '_links.self.href', '_links.previousepisode.href',
            '_links.previousepisode.name', '_links.nextepisode.href', '_links.nextepisode.name',
            'network', 'network.country.code', 'network.country.name', 'network.country.timezone',
            'network.id', 'network.name', 'network.officialSite', 'webChannel', 'webChannel.country',
            'webChannel.country.code', 'webChannel.country.name', 'webChannel.country.timezone',
            'webChannel.id', 'webChannel.name', 'webChannel.officialSite', 'dvdCountry',
            'dvdCountry.code', 'dvdCountry.name', 'dvdCountry.timezone', 'image'
        ]

        self.df.drop(columns=columns_to_drop, errors='ignore', inplace=True)

        self.df.rename(columns={
            'id': 'tvmaze_id',
            'url': 'tvmaze_url',
            'name': 'show_name',
            'type': 'show_type',
            'language': 'show_language',
            'genres': 'show_genres',
            'status': 'show_status',
            'averageRuntime': 'average_runtime_minutes',
            'premiered': 'premiere_date',
            'ended': 'end_date',
            'weight': 'show_tvmaze_weight',
            'summary': 'show_summary',
            'updated': 'last_updated_utc',
            'schedule.days': 'show_schedule_days',
            'externals.imdb': 'imdb_id',
            'image.medium': 'image_medium_url',
            'image.original': 'image_original_url',
        }, inplace=True)

        # Handle missing values and type conversions
        self.df["show_language"] = self.df["show_language"].fillna("Other")
        self.df["last_updated_utc"] = pd.to_datetime(self.df["last_updated_utc"], unit='s', utc=True).dt.tz_localize(None)
        self.df["premiere_date"] = pd.to_datetime(self.df["premiere_date"], errors='coerce')
        self.df["end_date"] = pd.to_datetime(self.df["end_date"], errors='coerce')
        self.df["average_runtime_minutes"] = pd.to_numeric(self.df["average_runtime_minutes"], errors='coerce')
        self.df['show_schedule_days'] = self.df['show_schedule_days'].apply(lambda x: ['Unknown'] if not x else x)
        self.df['show_genres'] = self.df['show_genres'].apply(lambda x: ['Undefined'] if not x else x)

        return self.df
