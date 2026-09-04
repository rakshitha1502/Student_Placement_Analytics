# Student Placement Analytics Platform

## Project Overview

The Student Placement Analytics Platform is a data engineering project designed to centralize, transform, validate, and analyze student placement data.

The platform processes data related to students, colleges, companies, and placement offers using PySpark and Snowflake. The transformed data is organized into a Star Schema for efficient analytical querying and is presented through an interactive Streamlit dashboard.

The project demonstrates data ingestion, ETL processing, data quality validation, dimensional modeling, SCD Type 2, incremental loading, analytical views, and dashboard development.

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

## Technology Stack

| Technology    | Purpose                                   |
| ------------- | ----------------------------------------- |
| Python        | ETL scripting and application development |
| PySpark       | Data processing and transformations       |
| Snowflake     | Cloud data warehouse and analytics        |
| Snowpipe      | Data ingestion                            |
| SQL           | Data modeling, validation, and analytics  |
| Streamlit     | Interactive dashboard                     |
| Pandas        | Dashboard data handling                   |
| Plotly        | Data visualization                        |
| python-dotenv | Environment variable management           |

## Project Architecture

```text
Source CSV Files
      |
      v
Snowflake RAW Layer
      |
      v
Snowflake STAGING Layer
      |
      v
PySpark ETL
  - Data Cleansing
  - Data Validation
  - Joins
  - Business Transformations
      |
      v
PySpark Staging
      |
      v
Snowflake Analytics Layer
      |
      +--> DIM_STUDENT (SCD Type 2)
      +--> DIM_COMPANY (SCD Type 2)
      +--> DIM_COLLEGE
      +--> DIM_DATE
      +--> FACT_PLACEMENT
      |
      v
Analytical Views
      |
      v
Streamlit Dashboard
```

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

## Data Engineering Process

### 1. Data Ingestion

Source CSV files are loaded into Snowflake RAW tables:

* `RAW_STUDENTS`
* `RAW_COLLEGES`
* `RAW_COMPANIES`
* `RAW_OFFERS`

Snowpipe is configured as part of the ingestion architecture.

### 2. Data Staging

The Snowflake STAGING layer prepares data for downstream processing.

Key staging objects include:

* `STG_STUDENTS`
* `STG_STUDENTS_FINAL`
* `STG_PLACEMENT`
* `STG_PLACEMENT_PYSPARK`

### 3. PySpark Processing

PySpark performs:

* Data cleansing
* Schema validation
* Data quality checks
* Dataset joins
* Business-rule transformations
* Derived column creation

### 4. Business Transformations

The pipeline creates the following derived attributes:

#### CGPA Band

* CGPA >= 8.5 → `Excellent`
* CGPA >= 7.0 → `Good`
* CGPA >= 5.0 → `Average`
* Otherwise → `Low`

#### Placement Segment

* CGPA >= 8.5 → `High Potential`
* CGPA >= 7.0 → `Moderate Potential`
* Otherwise → `Needs Improvement`

#### Offer Value Band

* CTC < 5 LPA → `Low`
* CTC <= 10 LPA → `Medium`
* CTC > 10 LPA → `High`

## Data Model

The analytical layer uses a **Star Schema**.

### Dimension Tables

#### DIM_STUDENT

Contains student information and supports **SCD Type 2** historical tracking.

Tracked attributes include:

* Program
* Branch
* Graduation year
* CGPA
* City
* State
* Segment

SCD Type 2 columns:

* `VALID_FROM`
* `VALID_TO`
* `IS_CURRENT`

#### DIM_COMPANY

Contains company and hiring information and supports historical tracking.

Important attributes include:

* Company name
* Industry
* Size band
* Hiring city
* Hiring state
* Status

#### DIM_COLLEGE

Contains college master information:

* College name
* City
* State
* Country
* Ownership
* Tier
* Category
* Status

#### DIM_DATE

Provides calendar attributes:

* Full date
* Day
* Month
* Quarter
* Year

### Fact Table

#### FACT_PLACEMENT

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

## Slowly Changing Dimension Type 2

SCD Type 2 is implemented for historical tracking of changing dimension attributes.

When a tracked attribute changes:

1. The existing record is expired.
2. `IS_CURRENT` is changed to `FALSE`.
3. `VALID_TO` is populated.
4. A new version of the record is inserted.
5. The new version has `IS_CURRENT = TRUE`.
6. The new record receives a new surrogate key.

This allows the system to preserve historical versions instead of overwriting existing information.

## Data Quality Framework

The project implements several data-quality controls.

### Row Count Reconciliation

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

### Duplicate Check

The combination:

```text
OFFER_ID + OFFER_LINE_ID
```

is treated as the fact-table business grain.

Current result:

```text
Total records       = 25
Unique offer lines  = 25
```

### Referential Integrity

Fact records are validated against:

* `DIM_STUDENT`
* `DIM_COMPANY`
* `DIM_COLLEGE`
* `DIM_DATE`

No orphan records were identified.

### CTC Validation

The pipeline validates that:

```text
0 < CTC_LPA < 100
```

Current invalid CTC records:

```text
0
```

### Critical Field Validation

Critical fields such as offer, student, company, college, CTC, and status are checked for NULL values.

Current invalid critical records:

```text
0
```

## Analytical Views

The project contains business-oriented Snowflake views:

* `VW_PLACEMENT_ANALYTICS`
* `VW_EXECUTIVE_SUMMARY`
* `VW_COLLEGE_PERFORMANCE`
* `VW_COMPANY_INSIGHTS`
* `VW_PLACEMENT_EXPLORER`
* `VW_DATA_QUALITY_SUMMARY`

These views simplify analytical queries and provide curated datasets for the dashboard.

## Streamlit Dashboard

The Streamlit application provides five major pages.

### 1. Executive Summary

Displays:

* Total offers
* Students placed
* Companies hiring
* Colleges with placements
* Average CTC
* Highest CTC
* Join rate
* Placement status distribution

### 2. College Performance

Provides:

* Offers by college
* Average CTC by college
* College-level placement details

### 3. Company Insights

Provides:

* Offers by company
* Average CTC by company
* Company placement details

### 4. Placement Explorer

Provides interactive filters for:

* College
* Company
* Offer status
* CTC range

It also provides:

* Top job roles by offers
* Detailed placement records

### 5. Data Quality

Displays:

* Raw offer count
* Fact offer count
* Invalid CTC count
* Critical field errors
* Overall data quality status

## Current Project Results

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

## ETL Validation

The PySpark ETL pipeline successfully loads transformed data into:

```text
STUDENT_PLACEMENT_DB.STAGING.STG_PLACEMENT_PYSPARK
```

Current successful load:

```text
Records loaded = 25
```

The PySpark output was validated against the Snowflake fact data for key business fields, with:

```text
Mismatched records = 0
```

## How to Run the Project

### 1. Create and activate the virtual environment

```cmd
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```cmd
pip install -r requirements.txt
```

### 3. Configure Snowflake credentials

Create a `.env` file in the project root:

```text
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
```

Do not commit `.env` to GitHub.

### 4. Run PySpark ingestion

```cmd
python src\ingestion.py
```

### 5. Run PySpark transformations

```cmd
python src\transformations.py
```

### 6. Run the Streamlit dashboard

```cmd
python -m streamlit run dashboard\app.py
```

The application will open in the browser.

## Data Quality Summary

The current project successfully passes the implemented validation checks:

```text
Row count reconciliation       PASS
Duplicate offer-line check     PASS
Referential integrity          PASS
CTC validation                 PASS
Critical NULL validation       PASS
PySpark/Snowflake validation   PASS
```

## Key Data Engineering Concepts Demonstrated

This project demonstrates practical knowledge of:

* ETL / ELT
* PySpark DataFrames
* Data cleansing
* Data validation
* Joins
* Derived columns
* Snowflake architecture
* Snowpipe
* Staging and RAW layers
* Star Schema
* Fact and dimension tables
* Surrogate keys
* SCD Type 2
* Incremental loading
* MERGE
* Data quality checks
* Referential integrity
* Analytical views
* SQL
* Streamlit dashboards
* Environment variable management

## Future Enhancements

Potential future improvements include:

* Azure Data Lake Storage integration
* Automated Snowpipe event notifications
* Fully automated SCD Type 2 processing
* Snowflake Tasks and Streams
* Advanced dashboard visualizations
* Snowflake Cortex Search / RAG
* Cortex Analyst for natural-language analytics
* Role-based access control
* DEV / TEST / PROD deployment
* Automated unit and integration testing
* CI/CD pipeline

## Conclusion

The Student Placement Analytics Platform demonstrates how a modern data engineering solution can ingest, transform, validate, model, and analyze placement data using PySpark and Snowflake.

The solution combines scalable data processing, dimensional modeling, historical tracking, data-quality controls, incremental loading, and interactive visualization into a single end-to-end analytics platform.

```

Save it with **Ctrl + S**.

After this, your README will be substantially complete and suitable as a **GitHub portfolio project README**.
```
