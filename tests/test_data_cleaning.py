import pytest
import os
import sys
import pandas as pd

path_to_modules = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if path_to_modules not in sys.path:
    sys.path.insert(0,path_to_modules)
from src.data_cleaning import TVMazeDataCleaner

@pytest.fixture
def sample_dataframe():
    """Creates a sample DataFrame mimicking raw TVMaze data."""
    data = {
        'id': [1],
        'url': ['http://example.com'],
        'name': ['Sample Show'],
        'language': [None],  # To test missing value handling
        'genres': [[]],  # Empty list to test genre handling
        'schedule.days': [[]],  # Empty list to test schedule handling
        'averageRuntime': ['30'],  # Should be converted to int
        'premiered': ['2023-01-01'],
        'ended': [None],  # Should be converted to NaT
        'last_updated_utc': [1672531200],  # Epoch time, should be converted to datetime
        'officialSite': [None],  # Should be filled with "Not Available"
        'image.medium': ['http://image.com/medium.jpg'],
        'image.original': ['http://image.com/original.jpg'],
        'runtime': [60],  # Should be dropped
        'network.name': ['ABC'],  # Should be dropped
    }
    return pd.DataFrame(data)

def test_clean_data(sample_dataframe):
    cleaner = TVMazeDataCleaner(sample_dataframe)
    cleaned_df = cleaner.clean_data()

    # Check dropped columns
    assert 'runtime' not in cleaned_df.columns
    assert 'network.name' not in cleaned_df.columns

    # Check column renaming
    assert 'tvmaze_id' in cleaned_df.columns
    assert 'tvmaze_url' in cleaned_df.columns
    assert 'show_name' in cleaned_df.columns
    assert 'show_language' in cleaned_df.columns

    # Check missing values handling
    assert cleaned_df.loc[0, 'show_language'] == "Other"
    assert cleaned_df.loc[0, 'official_site_url'] == "Not Available"

    # Check type conversions
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df['premiere_date'])
    assert pd.isna(cleaned_df.loc[0, 'end_date'])  # Check if None converted to NaT
    assert pd.api.types.is_integer_dtype(cleaned_df['average_runtime_minutes'])
    assert cleaned_df.loc[0, 'show_schedule_days'] == ['Unknown']
    assert cleaned_df.loc[0, 'show_genres'] == ['Undefined']

