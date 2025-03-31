# TVMaze Dataset Profiling Analysis

## Overview
The dataset contains information about TV shows from TVMaze with:

- **48 variables (columns)**
- **725 observations (rows)**
- **46.3% missing cells** (16,110 total missing values)
- **No duplicate rows**
- **Total memory size of 272.0 KiB**

## Key Data Quality Issues

### 1. Missing Data Problems
#### Severely incomplete columns:
- `network` and `dvdCountry`: **100% missing** (725/725)
- `runtime`: **80.3% missing** (582/725)
- `rating.average`: **82.3% missing** (597/725)
- `ended`: **74.8% missing** (542/725)

#### Moderately incomplete columns:
- `language`: **6.5% missing** (47/725)
- `officialSite`: **11.3% missing** (82/725)
- `summary`: **13.4% missing** (97/725)

### 2. Variable Type Issues
- **7 unsupported columns**, including `genres` (which is a list), `network`, `dvdCountry`, and nested objects like `image` and `webChannel`, which may contain complex data structures that weren't properly parsed.

### 3. Data Distribution Observations
#### ID field:
- Unique values for all **725 records**
- Range from **274 to 83,688**

#### Show names:
- **723 distinct names** (**99.7% unique**) indicating nearly all shows have unique names

#### Show types:
- Mostly **"Scripted"** (235), followed by **"Animation"** (117), **"Documentary"** (95), and **"Reality"** (91)

#### Languages:
- Primarily **English (280)**, **Chinese (117)**, **Russian (66)**, **Norwegian (31)**, and **Korean (23)**

#### Status:
- Mostly **"Running" (446)**, with **"Ended" (183)** and **"To Be Determined" (96)**

## Notable Columns

### Temporal Data
#### `premiered`:
- Dates range from **1944 to 2024**
- No missing or invalid dates

#### `ended`:
- Only available for **183 shows (25.2%)**
- Dates range from **2024 to 2025**

### Ratings
#### `rating.average`:
- When present (**128 records**), ranges from **1 to 8.3**
- Mean rating of **6.51**

### Runtime
- `runtime` and `averageRuntime` show similar distributions when present
- Typical runtime around **42-47 minutes**
- Range from **1 to 300 minutes**

### Web Channel Information
#### `webChannel.country` data shows:
- **China (107)**, **United States (97)**, **Russia (53)**, **United Kingdom (45)**, **Norway (25)** as top countries

#### `webChannel.name` has **151 distinct values**

## Recommendations

### Missing Data Handling:
- Consider **dropping columns with >80% missing data** unless critical
- For **moderately missing columns**, implement **imputation strategies** or flag as missing

### Data Structure Improvement:
- Parse **nested objects** (like `image`, `network`, `webChannel`) into proper **relational structures**
- Convert **categorical variables** to proper categorical **dtype**
- Flatten **list-based fields** like `genres` into separate rows or categories

The dataset provides a good foundation for **TV show analysis**, but requires significant **cleaning and restructuring** to be fully usable for most analytical purposes.
