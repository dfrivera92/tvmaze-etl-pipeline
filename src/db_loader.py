import sqlite3
import os
import pandas as pd

class SQLiteDB:
    def __init__(self, db_name="tvmaze.db"):
        """
        Initializes the SQLite database connection and ensures all required tables exist.
        """
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(project_root, "db", db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Creates necessary tables if they do not already exist."""
        tables = {
            "show_types": """
                CREATE TABLE IF NOT EXISTS show_types (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    show_type TEXT UNIQUE NOT NULL
                )
            """,
            "languages": """
                CREATE TABLE IF NOT EXISTS languages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    language TEXT UNIQUE NOT NULL
                )
            """,
            "genres": """
                CREATE TABLE IF NOT EXISTS genres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    genre TEXT UNIQUE NOT NULL
                )
            """,
            "statuses": """
                CREATE TABLE IF NOT EXISTS statuses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT UNIQUE NOT NULL
                )
            """,
            "schedule_days": """
                CREATE TABLE IF NOT EXISTS schedule_days (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    day_name TEXT UNIQUE NOT NULL
                )
            """,
            "shows": """
                CREATE TABLE IF NOT EXISTS shows (
                    tvmaze_id INTEGER PRIMARY KEY,
                    tvmaze_url TEXT,
                    official_site_url TEXT,
                    show_name TEXT NOT NULL,
                    show_type_id INTEGER,
                    language_id INTEGER,
                    status_id INTEGER,
                    average_runtime_minutes INTEGER,
                    premiere_date TEXT,
                    end_date TEXT,
                    show_tvmaze_weight INTEGER,
                    show_summary TEXT,
                    last_updated_utc TEXT,
                    imdb_id TEXT,
                    image_medium_url TEXT,
                    image_original_url TEXT,
                    FOREIGN KEY (show_type_id) REFERENCES show_types(id),
                    FOREIGN KEY (language_id) REFERENCES languages(id),
                    FOREIGN KEY (status_id) REFERENCES statuses(id)
                )
            """,
            "show_genres": """
                CREATE TABLE IF NOT EXISTS show_genres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    show_id INTEGER,
                    genre_id INTEGER,
                    FOREIGN KEY (show_id) REFERENCES shows(tvmaze_id),
                    FOREIGN KEY (genre_id) REFERENCES genres(id)
                )
            """,
            "show_schedule_days": """
                CREATE TABLE IF NOT EXISTS show_schedule_days (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    show_id INTEGER,
                    day_id INTEGER,
                    FOREIGN KEY (show_id) REFERENCES shows(tvmaze_id),
                    FOREIGN KEY (day_id) REFERENCES schedule_days(id)
                )
            """
        }

        for table_name, create_query in tables.items():
            self.cursor.execute(create_query)
            print(f"Table '{table_name}' checked/created successfully.")

        self.conn.commit()

    def insert_dataframe(self, df: pd.DataFrame, table_name: str):
        """
        Inserts a DataFrame into a given table.
        
        Args:
            df (pd.DataFrame): The DataFrame to insert.
            table_name (str): The name of the target SQLite table.
        """
        try:
            df.to_sql(table_name, self.conn, if_exists="append", index=False)
            print(f"Inserted {len(df)} records into {table_name}.")
        except Exception as e:
            print(f"Error inserting data into {table_name}: {e}")

    def run_query(self, query: str, params: tuple = ()):
        """
        Executes a given SQL query with optional parameters.
        
        Args:
            query (str): The SQL query to execute.
            params (tuple): A tuple of parameters to pass to the query.

        Returns:
            pd.DataFrame if the query is a SELECT statement, otherwise None.
        """
        try:
            if query.strip().upper().startswith("SELECT"):
                df = pd.read_sql(query, self.conn, params=params)
                return df
            else:
                self.cursor.execute(query, params)
                self.conn.commit()
                print("Query executed successfully.")
                return None
        except Exception as e:
            print(f"Error executing query: {e}")
            
    def close_connection(self):
        """Closes the database connection."""
        self.conn.close()
        print("Database connection closed.")
