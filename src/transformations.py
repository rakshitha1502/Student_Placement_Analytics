from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
import os
import snowflake.connector
from dotenv import load_dotenv

# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = SparkSession.builder \
    .appName("StudentPlacementTransformations") \
    .getOrCreate()



# --------------------------------------------------
# 2. Load Datasets
# --------------------------------------------------

students_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/raw/placement_students.csv")

offers_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/raw/placement_offers.csv")

companies_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/raw/placement_companies.csv")

colleges_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/raw/placement_colleges.csv")


# --------------------------------------------------
# 3. Join Students and Offers
# --------------------------------------------------

student_offers_df = students_df.alias("s").join(
    offers_df.alias("o"),
    col("s.STUDENT_ID") == col("o.STUDENT_ID"),
    "inner"
).select(
    col("s.STUDENT_ID"),
    col("s.FIRST_NAME"),
    col("s.LAST_NAME"),
    col("s.PROGRAM"),
    col("s.BRANCH"),
    col("s.CGPA"),
    col("s.COLLEGE_ID"),

    col("o.OFFER_ID"),
    col("o.OFFER_LINE_ID"),
    col("o.COMPANY_ID"),
    col("o.ROLE_TITLE"),
    col("o.CTC_LPA"),
    col("o.OFFER_STATUS"),
    col("o.IS_JOINED")
)


# --------------------------------------------------
# 4. Join with Companies
# --------------------------------------------------

student_offers_companies_df = student_offers_df.alias("so").join(
    companies_df.alias("c"),
    col("so.COMPANY_ID") == col("c.COMPANY_ID"),
    "inner"
).select(
    col("so.*"),
    col("c.COMPANY_NAME"),
    col("c.INDUSTRY"),
    col("c.SIZE_BAND"),
    col("c.HIRING_CITY")
)


# --------------------------------------------------
# 5. Join with Colleges
# --------------------------------------------------

final_df = student_offers_companies_df.alias("soc").join(
    colleges_df.alias("cl"),
    col("soc.COLLEGE_ID") == col("cl.COLLEGE_ID"),
    "inner"
).select(
    col("soc.*"),
    col("cl.COLLEGE_NAME"),
    col("cl.TIER"),
    col("cl.CATEGORY")
)


# --------------------------------------------------
# 6. Add CGPA Band
# --------------------------------------------------

final_df = final_df.withColumn(
    "CGPA_BAND",
    when(col("CGPA") >= 8.5, "Excellent")
    .when(col("CGPA") >= 7.0, "Good")
    .when(col("CGPA") >= 5.0, "Average")
    .otherwise("Low")
)


# --------------------------------------------------
# 7. Add Placement Segment
# --------------------------------------------------

final_df = final_df.withColumn(
    "PLACEMENT_SEGMENT",
    when(col("CGPA") >= 8.5, "High Potential")
    .when(col("CGPA") >= 7.0, "Moderate Potential")
    .otherwise("Needs Improvement")
)


# --------------------------------------------------
# 8. Add Offer Value Band
# --------------------------------------------------

final_df = final_df.withColumn(
    "OFFER_VALUE_BAND",
    when(col("CTC_LPA") < 5, "Low")
    .when(col("CTC_LPA") <= 10, "Medium")
    .otherwise("High")
)


# --------------------------------------------------
# 9. Display Final Analytical Dataset
# --------------------------------------------------

print("\nFinal Analytical Placement Dataset")

final_df.select(
    "STUDENT_ID",
    "CGPA",
    "CGPA_BAND",
    "PLACEMENT_SEGMENT",
    "COMPANY_NAME",
    "CTC_LPA",
    "OFFER_VALUE_BAND",
    "COLLEGE_NAME"
).show(truncate=False)


# --------------------------------------------------
# 10. Record Count
# --------------------------------------------------

print("Final Analytical Records:", final_df.count())


# --------------------------------------------------
# 11. Stop Spark
# --------------------------------------------------
print("\nFinal Dataset Count:", final_df.count())

load_dotenv()

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse="PLACEMENT_WH",
    database="STUDENT_PLACEMENT_DB",
    schema="STAGING"
)

cursor = conn.cursor()

cursor.execute("""
TRUNCATE TABLE STUDENT_PLACEMENT_DB.STAGING.STG_PLACEMENT_PYSPARK
""")

insert_sql = """
INSERT INTO STUDENT_PLACEMENT_DB.STAGING.STG_PLACEMENT_PYSPARK (
    STUDENT_ID,
    FIRST_NAME,
    LAST_NAME,
    PROGRAM,
    BRANCH,
    CGPA,
    COLLEGE_ID,
    OFFER_ID,
    OFFER_LINE_ID,
    COMPANY_ID,
    ROLE_TITLE,
    CTC_LPA,
    OFFER_STATUS,
    IS_JOINED,
    COMPANY_NAME,
    INDUSTRY,
    SIZE_BAND,
    HIRING_CITY,
    COLLEGE_NAME,
    TIER,
    CATEGORY,
    CGPA_BAND,
    PLACEMENT_SEGMENT,
    OFFER_VALUE_BAND
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""

rows = [
    (
        row.STUDENT_ID,
        row.FIRST_NAME,
        row.LAST_NAME,
        row.PROGRAM,
        row.BRANCH,
        row.CGPA,
        row.COLLEGE_ID,
        row.OFFER_ID,
        row.OFFER_LINE_ID,
        row.COMPANY_ID,
        row.ROLE_TITLE,
        row.CTC_LPA,
        row.OFFER_STATUS,
        row.IS_JOINED,
        row.COMPANY_NAME,
        row.INDUSTRY,
        row.SIZE_BAND,
        row.HIRING_CITY,
        row.COLLEGE_NAME,
        row.TIER,
        row.CATEGORY,
        row.CGPA_BAND,
        row.PLACEMENT_SEGMENT,
        row.OFFER_VALUE_BAND
    )
    for row in final_df.collect()
]

cursor.executemany(insert_sql, rows)

conn.commit()

print("PySpark data loaded into Snowflake successfully!")
print("Records loaded:", len(rows))

cursor.close()
conn.close()
spark.stop()