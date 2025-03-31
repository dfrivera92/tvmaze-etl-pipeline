import pytest
import os
import sys
import pandas as pd

path_to_modules = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if path_to_modules not in sys.path:
    sys.path.insert(0,path_to_modules)
from src.data_processing import TVMazeDataProcessor

def test_process_tv_shows():
    processor = TVMazeDataProcessor()
    df = processor.process_tv_shows("2024-01")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty