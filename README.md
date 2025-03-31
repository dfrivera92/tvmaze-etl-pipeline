# 🎬 TVMaze ETL Pipeline
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Workflow](https://img.shields.io/badge/Workflow-ETL_Pipeline-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
## Overview
An automated ETL pipeline that extracts TV show data from TVMaze API, processes it through multiple stages, and loads it into a SQLite database.

## 🏗️ Project structure
```plaintext
tvmaze-etl-pipeline/
├── data/                  # Processed Parquet files
│   └── tvmaze_data_YYYY-MM.parquet
├── model/                 # Image of the data model created to store the data
│   └── model_structure.png
├── db/                    # SQLite database storage
│   └── tvmaze.db
├── json/                  # Raw JSON data from TVMaze API
│   └── YYYY-MM-DD.json
├── profiling/            # Data quality reports
│   └── data_profile_report.html
├── src/                  # Source code
│   ├── data_ingestion.py
│   ├── data_processing.py
│   ├── data_profiling.py
│   ├── data_cleaning.py
│   ├── data_export.py
│   ├── data_normalization.py
│   ├── db_loader.py
│   └── main.py
└── tests/                  # Tests
    ├── test_data_cleaning
    ├── test_data_ingestion.py
    ├── test_data_processing.py
    └── test_db_loader.py
```

# Key features
- 📡 **API Integration**: Fetches TV show data from TVMaze API for any specified month
- 🧹 **Data Cleaning**: Handles missing values, duplicates, and inconsistencies
- 📊 **Data Profiling**: Generates comprehensive quality reports with `ydata-profiling`
- 🚀 **Efficient Storage**: Uses Parquet format for processed data
- 🗄️ **Relational Model**: Normalizes data into efficient SQL tables
- ⚙️ **Modular Design**: Each component follows single responsibility principle
- 🧪 **Comprehensive Testing**: Ensures reliability with unit tests for data cleaning, ingestion, processing, and database loading using `pytest`
  
## ⚙️ Requirements
Install required packages
```
pip install -r requirements.txt
```

## 🚀 Usage
Run the ETL pipeline using:
```
python src/main.py
```

### 🔄 Pipeline Workflow
The pipeline executes the following steps as shown in [`main.py`](/src/main.py):
1. Data Ingestion: [`TVMazeDataFetcher`](/src/data_ingestion.py) fetches show data from TVMaze API
2. Data Processing: [`TVMazeDataProcessor`](/src/data_processing.py) converts JSON files to DataFrame
3. Data Profiling: [`TVMazeDataProfiler`](/src/data_profiling.py) generates quality reports
4. Data Cleaning: [`TVMazeDataCleaner`](/src/data_cleaning.py) handles data quality issues
5. Data Export: [`ParquetExporter`](/src/data_export.py) saves processed data as Parquet
6. Data Normalization: [`TVMazeDataNormalizer`](/src/data_normalization.py) creates relational tables
7. Database Loading: [`SQLiteDB`](/src/db_loader.py) loads data into SQLite
8. 📊 **Data Analysis**: [`main.py`](/src/main.py#L51-L71) runs analytical queries on the dataset, including:  
   - ⏳ **Average Runtime of Shows**  
   - 🎭 **Genre Distribution**  
   - 🌐 **Unique Official Website Domains**  

## 📂 Sample data (January 2024)
The repository includes sample data from January 2024:
- 📄 **Raw API Data**:
  Raw API responses stored in [`/json/2024-01-*.json`](/json/)
- 🔄 **Processed Dataset**:
  Cleaned and transformed data in [`/data/tvmaze_data_2024-01.parquet`](/data/tvmaze_data_2024-01.parquet) (Parquet format)
- 📊 **Data Profile**
  HTML profile generated with Pandas Profiling available at [`/profiling/data_profile_report.html`](/profiling/data_profile_report.html)
- 📈 **Data Analysis**
  After processing and storing the TV show data, the pipeline performs a data analysis to extract key insights:

  ### ⏳ Average runtime of shows  
  The average runtime of TV shows in the dataset:  
  > **42.3 minutes**  

  ---

  ### 🎭 Genre distribution  
  The count of shows by genre:  

  ```plaintext
      Genre       Show Count
      ----------------------
      Undefined         261
      Drama            157
      Comedy           123
      Romance          73
      ...
  ```

  ---

  ### 🌐 Unique official website domains
  Some distinct official site URLs from the dataset:
  ```plaintext
    http://www.bbc.co.uk/programmes/p01djw5m
    http://www.bbc.co.uk/programmes/b006ml0g
    http://www.nbc.com/the-tonight-show
    http://www.bbc.co.uk/programmes/b006m8wd
    ...
  ```

## 🛠 Development
The ETL pipeline is modular, with each component handling a specific transformation:
- Each class in [`src`](/src/) follows single responsibility principle
- Data validation at each transformation step
- Comprehensive data profiling with `ydata_profiling`
- Efficient storage using Parquet format

## 🏛️ Data Model Structure  
The **TVMaze ETL pipeline** follows a **relational model** to efficiently store TV show data. The database schema is represented in:  
📌 [`model_structure.png`](/model/model_structure.png)  
<div align="center"><img src="https://github.com/user-attachments/assets/09d96c15-ffdd-44b6-a7aa-043ca2adf558" width=60% height=60%></div>

## 🧪 Tests
Unit tests ensure the correctness of each pipeline component. The test suite is located in the [`tests`](/tests/) directory and includes:
- ✅ **Data Cleaning**: Ensures handling of missing values, data type conversions, and renaming columns ([`test_data_cleaning.py`](/tests/test_data_cleaning.py/))
- ✅ **Data Ingestion**: Tests API fetching, invalid date handling, and data directory setup ([`test_data_ingestion.py`](/tests/test_data_ingestion.py))
- ✅ **Data Processing**: Verifies JSON to DataFrame transformation ([`test_data_processing.py`](/tests/test_data_processing.py))
- ✅ **Database Loading**: Ensures table creation and correct data insertion ([`test_db_loader.py`](/tests/test_db_loader.py))

### 🔍 Running Tests
Run the tests using:
```
pytest tests/ -v
```

## 📜 License
This project is licensed under the terms of the [LICENSE](LICENSE) file included in the repository.
