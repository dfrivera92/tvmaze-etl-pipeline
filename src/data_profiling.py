import pandas as pd
import os
from ydata_profiling import ProfileReport

class TVMazeDataProfiler:
    """
    Class for generating data profiling reports for TV show data.

    This class creates and stores profiling reports for a given dataset,
    helping to analyze and understand the structure and quality of the data.

    Attributes:
        project_root (str): The root directory of the project.
        profiling_dir (str): The directory where profiling reports will be saved.
    """

    def __init__(self, profiling_dir=None):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.profiling_dir = profiling_dir or os.path.join(self.project_root, "profiling")
        os.makedirs(self.profiling_dir, exist_ok=True)

    def generate_profile_report(self, df_to_profile):
        """
        Generate a data profiling report for the given DataFrame.

        This method generates an HTML report summarizing the dataset's structure,
        missing values, statistics, and other key insights.

        Args:
            df_to_profile (pd.DataFrame): The pandas DataFrame to be profiled.

        Returns:
            str: The file path where the profiling report is saved.

        Saves:
            A file named 'data_profile_report.html' in the profiling directory.
        """
        profile = ProfileReport(df_to_profile, title="Data Profiling Report")
        output_path = os.path.join(self.profiling_dir, "data_profile_report.html")
        profile.to_file(output_path)
        print(f"\nReport saved to: {output_path}")
        return output_path


    