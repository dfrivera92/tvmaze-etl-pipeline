import pytest
import pandas as pd
import os
import sys

path_to_modules = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if path_to_modules not in sys.path:
    sys.path.insert(0,path_to_modules)
from src.db_loader import SQLiteDB

@pytest.fixture
def db():
    return SQLiteDB(db_name="test.db")

def test_table_creation(db):
    db._create_tables()
    tables = db.run_query("SELECT name FROM sqlite_master WHERE type='table'")
    assert 'shows' in tables['name'].values
    assert 'genres' in tables['name'].values

def test_insert_data(db):
    test_df = pd.DataFrame({'genre': ['Drama', 'Comedy']})
    db.insert_dataframe(test_df, 'genres')
    result = db.run_query("SELECT * FROM genres")
    assert len(result) == 2