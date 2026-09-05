# Student Placement Analytics Platform

## Project Overview

The **Student Placement Analytics Platform** is an end-to-end data engineering project designed to ingest, transform, validate, model, and analyze student placement data.

The platform processes data related to students, colleges, companies, and placement offers using **PySpark and Snowflake**. The data is organized into a **Star Schema** for analytical querying and presented through an interactive **Streamlit dashboard**.

**dbt** is used to implement automated **SCD Type 2 snapshots** for tracking historical changes in student and company dimensions.

The project demonstrates:

* Data ingestion
* ETL / ELT processing
* PySpark transformations
* Data quality validation
* Snowflake data warehousing
* Snowpipe ingestion
* Dimensional modeling
* Star Schema
* SCD Type 2
* dbt snapshots
* Incremental loading
* Analytical views
* Dashboard development

---

## Business Objective

The main objectives of the project are to:

* Analyze student placement performance.
* Track placement offers and joining status.
* Analyze college-wise placement performance.
* Analyze company hiring patterns.
* Monitor CTC and placement trends.
* Maintain historical changes in dimension data using SCD Type 2.
* Implement data quality and reconciliation checks.
* Provide an interactive dashboard for business users.

---

## Technology Stack

| Technology    | Purpose                                                |
| ------------- | ------------------------------------------------------ |
| Python        | ETL scripting and application development              |
| PySpark       | Distributed data processing and transformations        |
| Snowflake     | Cloud data warehouse and analytics                     |
| Snowpipe      | Data ingestion                                         |
| dbt           | Data transformation and automated SCD Type 2 snapshots |
| SQL           | Data modeling, validation, and analytics               |
| Streamlit     | Interactive dashboard                                  |
| Pandas        | Dashboard data handling                                |
| Plotly        | Data visualization                                     |
| python-dotenv | Environment variable management                        |

---

## Project Architecture

```text
                         Source CSV Files
                               |
                               v
                    +----------------------+
                    |   Snowflake RAW      |
                    |                      |
                    | RAW_STUDENTS         |
                    | RAW_COLLEGES         |
                    | RAW_COMPANIES        |
                    | RAW_OFFERS           |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   PySpark ETL        |
                    |                      |
                    | Data Cleansing       |
                    | Validation           |
                    | Joins                |
                    | Transformations      |
                    | Derived Columns      |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Snowflake STAGING    |
                    |                      |
                    | STG_PLACEMENT_PYSPARK|
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Snowflake ANALYTICS   |
                    |                      |
                    | DIM_STUDENT          |
                    | DIM_COMPANY          |
                    | DIM_COLLEGE          |
                    | DIM_DATE             |
                    | FACT_PLACEMENT       |
                    +----------+-----------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
        +------------------+        +------------------+
        | dbt Snapshots    |        | Analytical Views |
        |                  |        |                  |
        | STUDENT_SNAPSHOT |        | VW_*             |
        | COMPANY_SNAPSHOT |        +--------+---------+
        +------------------+                 |
                 |                           v
                 |                  Streamlit Dashboard
                 |                           |
                 v                           v
          SCD Type 2 History          Business Analytics
```

### SCD Type 2 Flow

```text
RAW Source Data
      |
      v
dbt Snapshot
      |
      v
Change Detection
      |
      +---- No Change ----> Keep Current Version
      |
      +---- Change -------> Expire Old Version
                              |
                              v
                       Insert New Version
                              |
                              v
                       Preserve History
```

---

## Data Sources

The project uses four CSV datasets:

* `placement_students.csv` — student academic and demographic information.
* `placement_colleges.csv` — college master data.
* `placement_companies.csv` — company and hiring information.
* `placement_offers.csv` — placement offer and joining information.

### Dataset Volume

| Dataset          | Records |
| ---------------- | ------: |
| Students         |      20 |
| Colleges         |      15 |
| Companies        |      15 |
| Placement Offers |      25 |

---

## Project Structure

```text
Student_Placement_Analytics/
│
├── README.md
├── .env
├── .gitignore
├── requirements.txt
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── quarantine/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── spark_session.py
│   ├── ingestion.py
│   ├── transformations.py
│   ├── snowflake_test.py
│   └── snowflake_load.py
│
├── sql/
│   ├── 01_database.sql
│   ├── 02_raw_tables.sql
│   ├── 03_dimensions.sql
│   ├── 04_fact.sql
│   └── 05_views.sql
│
├── dbt_project/
│   ├── dbt_project.yml
│   └── snapshots/
│       ├── student_snapshot.sql
│       └── company_snapshot.sql
│
├── dashboard/
│   ├── app.py
│   ├── executive_summary.py
│   ├── college_performance.py
│   ├── company_insights.py
│   ├── placement_explorer.py
│   └── data_quality.py
│
└── tests/
```

> **Note:** The current local dbt folder is named `jaffle_shop_1`. It can be renamed to `dbt_project` later without changing the dbt logic.

---

# Data Engineering Process

## 1. Data Ingestion

Source CSV files are loaded into Snowflake RAW tables:

* `RAW_STUDENTS`
* `RAW_COLLEGES`
* `RAW_COMPANIES`
* `RAW_OFFERS`

Snowpipe is configured as part of the ingestion architecture.

The RAW layer stores source-oriented data before downstream transformations.

---

## 2. Data Staging

The Snowflake STAGING layer prepares data for downstream processing.

Key staging objects include:

* `STG_STUDENTS`
* `STG_STUDENTS_FINAL`
* `STG_PLACEMENT`
* `STG_PLACEMENT_PYSPARK`

The PySpark pipeline loads the transformed placement dataset into:

```text
STUDENT_PLACEMENT_DB.STAGING.STG_PLACEMENT_PYSPARK
```

---

## 3. PySpark Processing

PySpark performs:

* Data cleansing
* Schema validation
* Data quality checks
* Dataset joins
* Business-rule transformations
* Derived column creation

The pipeline combines student, college, company, and offer information to create an analytical placement dataset.

---

## 4. Business Transformations

The pipeline creates the following derived attributes.

### CGPA Band

* CGPA >= 8.5 → `Excellent`
* CGPA >= 7.0 → `Good`
* CGPA >= 5.0 → `Average`
* Otherwise → `Low`

### Placement Segment

* CGPA >= 8.5 → `High Potential`
* CGPA >= 7.0 → `Moderate Potential`
* Otherwise → `Needs Improvement`

### Offer Value Band

* CTC < 5 LPA → `Low`
* CTC <= 10 LPA → `Medium`
* CTC > 10 LPA → `High`

---

# Data Model

The analytical layer uses a **Star Schema**.

## Dimension Tables

### DIM_STUDENT

Contains student information and supports historical tracking.

Important attributes include:

* Student information
* Program
* Branch
* Graduation year
* CGPA
* City
* State
* Segment
* College

The physical dimension design includes SCD Type 2 fields:

* `VALID_FROM`
* `VALID_TO`
* `IS_CURRENT`

dbt snapshots are additionally used to automatically detect and preserve changes from the source student data.

---

### DIM_COMPANY

Contains company and hiring information.

Important attributes include:

* Company name
* Industry
* Size band
* Hiring city
* Hiring state
* Country
* Status

Company changes are tracked historically using SCD Type 2.

---

### DIM_COLLEGE

Contains college master information:

* College name
* City
* State
* Country
* Ownership
* Tier
* Category
* Status

---

### DIM_DATE

Provides calendar attributes:

* Full date
* Day
* Month
* Quarter
* Year

---

## Fact Table

### FACT_PLACEMENT

Stores placement offer transactions.

The fact table grain is:

**One row per offer line (`OFFER_ID + OFFER_LINE_ID`).**

Important measures and attributes include:

* CTC
* Monthly stipend
* Offer status
* Joining status
* Role
* Job city
* Hiring mode
* Student
* Company
* College
* Date

---

# Slowly Changing Dimension Type 2

SCD Type 2 is used to preserve historical versions of changing dimension data.

Instead of overwriting an existing record, the system maintains multiple versions of the record.

When a tracked attribute changes:

1. The existing version is identified.
2. The old version is expired.
3. Its end timestamp is populated.
4. A new version is created.
5. The new version becomes the current version.
6. Historical information remains available for analysis.

This allows the platform to answer questions such as:

> What was the student's CGPA or profile information at a particular point in time?

---

# dbt SCD Type 2 Snapshots

The project uses **dbt snapshots** to automate change detection for student and company source data.

Two snapshots are implemented:

```text
student_snapshot.sql
company_snapshot.sql
```

### Student Snapshot

Tracks changes in attributes such as:

* First name
* Last name
* Gender
* Program
* Branch
* Graduation year
* CGPA
* Segment
* College

### Company Snapshot

Tracks changes in attributes such as:

* Company name
* Industry
* HQ country
* Size band
* Hiring city
* Hiring state
* Status

The snapshots use the dbt `check` strategy.

Important dbt-managed historical columns include:

* `DBT_SCD_ID`
* `DBT_UPDATED_AT`
* `DBT_VALID_FROM`
* `DBT_VALID_TO`

### SCD Type 2 Validation

The implementation was tested by changing the CGPA of student `ST0001`:

```text
Original CGPA: 9.28
Test CGPA:     9.50
```

After executing the dbt snapshot, both versions were preserved:

```text
9.28 → Historical Version
9.50 → Current Version
```

The source data was subsequently restored to its original value.

This validates that the dbt snapshot correctly detects changes and maintains historical versions.

---

# Data Quality Framework

The project implements several data-quality controls.

## Row Count Reconciliation

The pipeline compares record counts between:

```text
RAW_OFFERS
     ↓
STG_PLACEMENT_PYSPARK
     ↓
FACT_PLACEMENT
```

Current validation:

```text
RAW_OFFERS          = 25
PYSPARK STAGING     = 25
FACT_PLACEMENT      = 25
```

---

## Duplicate Check

The combination:

```text
OFFER_ID + OFFER_LINE_ID
```

is treated as the fact-table business grain.

Current result:

```text
Total records        = 25
Unique offer lines   = 25
```

---

## Referential Integrity

Fact records are validated against:

* `DIM_STUDENT`
* `DIM_COMPANY`
* `DIM_COLLEGE`
* `DIM_DATE`

No orphan records were identified.

---

## CTC Validation

The pipeline validates that:

```text
0 < CTC_LPA < 100
```

Current invalid CTC records:

```text
0
```

---

## Critical Field Validation

Critical fields such as offer, student, company, college, CTC, and status are checked for NULL values.

Current invalid critical records:

```text
0
```

---

# Analytical Views

The project contains business-oriented Snowflake views:

* `VW_PLACEMENT_ANALYTICS`
* `VW_EXECUTIVE_SUMMARY`
* `VW_COLLEGE_PERFORMANCE`
* `VW_COMPANY_INSIGHTS`
* `VW_PLACEMENT_EXPLORER`
* `VW_DATA_QUALITY_SUMMARY`

These views provide curated datasets for analytical queries and the Streamlit dashboard.

---

# Streamlit Dashboard

The Streamlit application provides five major pages.

## 1. Executive Summary

Displays:

* Total offers
* Students placed
* Companies hiring
* Colleges with placements
* Average CTC
* Highest CTC
* Join rate
* Placement status distribution

## 2. College Performance

Provides:

* Offers by college
* Average CTC by college
* College-level placement details

## 3. Company Insights

Provides:

* Offers by company
* Average CTC by company
* Company placement details

## 4. Placement Explorer

Provides interactive filters for:

* College
* Company
* Offer status
* CTC range

It also provides:

* Top job roles by offers
* Detailed placement records

## 5. Data Quality

Displays:

* Raw offer count
* Fact offer count
* Invalid CTC count
* Critical field errors
* Overall data quality status

---

# Current Project Results

Based on the current dataset:

| Metric                   |    Result |
| ------------------------ | --------: |
| Total offers             |        25 |
| Students with placements |        12 |
| Companies hiring         |        13 |
| Colleges with placements |         8 |
| Students joined          |         5 |
| Join rate                |       20% |
| Average CTC              | 26.19 LPA |
| Highest CTC              | 41.99 LPA |
| Invalid CTC records      |         0 |
| Critical field errors    |         0 |

---

# ETL Validation

The PySpark ETL pipeline successfully loads transformed data into:

```text
STUDENT_PLACEMENT_DB.STAGING.STG_PLACEMENT_PYSPARK
```

Current successful load:

```text
Records loaded = 25
```

The PySpark output was validated against Snowflake fact data for key business fields.

```text
Mismatched records = 0
```

---

# How to Run the Project

## 1. Create and activate the virtual environment

```cmd
python -m venv venv
venv\Scripts\activate
```

## 2. Install dependencies

```cmd
pip install -r requirements.txt
```

## 3. Configure Snowflake credentials

Create a `.env` file in the project root:

```text
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
```

Do not commit `.env` to GitHub.

---

## 4. Run PySpark ingestion

```cmd
python src\ingestion.py
```

---

## 5. Run PySpark transformations

```cmd
python src\transformations.py
```

---

## 6. Run dbt snapshots

Navigate to the dbt project:

```cmd
cd jaffle_shop_1
```

Run:

```cmd
dbt debug
```

Then:

```cmd
dbt snapshot
```

The snapshots create and maintain historical versions of student and company source data.

---

## 7. Run the Streamlit dashboard

From the project root:

```cmd
python -m streamlit run dashboard\app.py
```

The application will open in the browser.

---

# Data Quality Summary

The current project successfully passes the implemented validation checks:

```text
Row count reconciliation       PASS

Duplicate offer-line check    PASS

Referential integrity         PASS

CTC validation                PASS

Critical NULL validation      PASS

PySpark/Snowflake validation  PASS

dbt SCD Type 2 snapshots      PASS
```

---

# Key Data Engineering Concepts Demonstrated

This project demonstrates practical knowledge of:

* ETL / ELT
* PySpark DataFrames
* Data cleansing
* Data validation
* Joins
* Derived columns
* Snowflake architecture
* Snowpipe
* RAW and STAGING layers
* Star Schema
* Fact and dimension tables
* Surrogate keys
* SCD Type 2
* dbt snapshots
* Incremental loading
* MERGE
* Data quality checks
* Referential integrity
* Analytical views
* SQL
* Streamlit dashboards
* Environment variable management

---

# Future Enhancements

Potential future improvements include:

* Automated Snowpipe event notifications
* Snowflake Tasks and Streams
* Advanced dashboard visualizations
* Snowflake Cortex Search / RAG
* Cortex Analyst for natural-language analytics
* Role-based access control
* DEV / TEST / PROD deployment
* Automated unit and integration testing
* CI/CD pipeline
* Cloud object storage integration

---

# Conclusion

The **Student Placement Analytics Platform** demonstrates how a modern data engineering solution can ingest, transform, validate, model, and analyze placement data using **PySpark, Snowflake, dbt, and Streamlit**.

The solution combines:

* Scalable data processing
* Cloud data warehousing
* Dimensional modeling
* Historical SCD Type 2 tracking
* Automated dbt snapshots
* Data-quality controls
* Incremental processing
* Analytical views
* Interactive visualization

into a single end-to-end analytics platform.

The project provides practical exposure to the technologies and data engineering concepts commonly used in modern data platforms.
