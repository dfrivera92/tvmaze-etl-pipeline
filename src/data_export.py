import pandas as pd
import os

class ParquetExporter:
    def __init__(self, project_root=None):
        """
        Initializes the ParquetExporter with the project root directory.

        Args:
            project_root (str, optional): Root directory of the project. Defaults to the parent of the script directory.
        """
        self.project_root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.project_root, "data")

        os.makedirs(self.data_dir, exist_ok=True)

    def export_to_parquet(self, df, filename="data.parquet"):
        """
        Exports a DataFrame to a Parquet file.

        Args:
            df (pd.DataFrame): The DataFrame to export.
            filename (str, optional): The name of the Parquet file. Defaults to "data.parquet".

        Returns:
            str: The full file path of the exported Parquet file.
        """
        file_path = os.path.join(self.data_dir, filename)

        df.to_parquet(file_path, engine="pyarrow", compression="snappy")

        print(f"Data exported to {file_path}")
        return file_path
