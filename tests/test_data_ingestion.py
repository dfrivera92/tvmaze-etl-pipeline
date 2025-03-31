import pytest
import os
import sys
from datetime import datetime

path_to_modules = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if path_to_modules not in sys.path:
    sys.path.insert(0,path_to_modules)
from src.data_ingestion import TVMazeDataFetcher

def test_tvmaze_data_fetcher_init():
    fetcher = TVMazeDataFetcher()
    assert os.path.exists(fetcher.json_dir)

def test_invalid_date_format():
    fetcher = TVMazeDataFetcher()
    with pytest.raises(ValueError):
        fetcher.fetch_data("invalid-date")