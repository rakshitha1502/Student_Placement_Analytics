from pyspark.sql import SparkSession

# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = SparkSession.builder \
    .appName("StudentPlacementIngestion") \
    .getOrCreate()


# --------------------------------------------------
# 2. Load Datasets
# --------------------------------------------------

students_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/raw/placement_students.csv")

colleges_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/raw/placement_colleges.csv")

companies_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/raw/placement_companies.csv")

offers_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("data/raw/placement_offers.csv")


# --------------------------------------------------
# 3. Confirm Data Loaded
# --------------------------------------------------

print("All datasets loaded successfully")

print("Students:", students_df.count())
print("Colleges:", colleges_df.count())
print("Companies:", companies_df.count())
print("Offers:", offers_df.count())


# --------------------------------------------------
# 4. Students - Data Quality
# --------------------------------------------------

print("\nStudents - Null Values")

students_df.select([
    students_df[col].isNull().cast("int").alias(col)
    for col in students_df.columns
]).show()

print("\nStudents - Duplicate Rows")

print(
    students_df.count()
    - students_df.dropDuplicates().count()
)


# --------------------------------------------------
# 5. Colleges - Data Quality
# --------------------------------------------------

print("\nColleges - Null Values")

colleges_df.select([
    colleges_df[col].isNull().cast("int").alias(col)
    for col in colleges_df.columns
]).show()

print("\nColleges - Duplicate Rows")

print(
    colleges_df.count()
    - colleges_df.dropDuplicates().count()
)


# --------------------------------------------------
# 6. Companies - Data Quality
# --------------------------------------------------

print("\nCompanies - Null Values")

companies_df.select([
    companies_df[col].isNull().cast("int").alias(col)
    for col in companies_df.columns
]).show()

print("\nCompanies - Duplicate Rows")

print(
    companies_df.count()
    - companies_df.dropDuplicates().count()
)


# --------------------------------------------------
# 7. Offers - Data Quality
# --------------------------------------------------

print("\nOffers - Null Values")

offers_df.select([
    offers_df[col].isNull().cast("int").alias(col)
    for col in offers_df.columns
]).show()

print("\nOffers - Duplicate Rows")

print(
    offers_df.count()
    - offers_df.dropDuplicates().count()
)


# --------------------------------------------------
# 8. Display Schemas
# --------------------------------------------------

print("\nStudents Schema")
students_df.printSchema()

print("\nColleges Schema")
colleges_df.printSchema()

print("\nCompanies Schema")
companies_df.printSchema()

print("\nOffers Schema")
offers_df.printSchema()


# --------------------------------------------------
# 9. Stop Spark
# --------------------------------------------------
# --------------------------------------------------
# 10. Business Rule Validation
# --------------------------------------------------

print("\nOffers - Invalid CTC Values")

invalid_ctc_df = offers_df.filter(
    (offers_df["CTC_LPA"] <= 0) |
    (offers_df["CTC_LPA"] >= 100)
)

print("Invalid CTC Records:", invalid_ctc_df.count())

invalid_ctc_df.show()

# --------------------------------------------------
# 11. Referential Integrity Validation
# --------------------------------------------------

print("\nOffers - Invalid Student IDs")

invalid_student_ids = offers_df.join(
    students_df,
    offers_df["STUDENT_ID"] == students_df["STUDENT_ID"],
    "left_anti"
)

print("Invalid Student IDs:", invalid_student_ids.count())


print("\nOffers - Invalid Company IDs")

invalid_company_ids = offers_df.join(
    companies_df,
    offers_df["COMPANY_ID"] == companies_df["COMPANY_ID"],
    "left_anti"
)

print("Invalid Company IDs:", invalid_company_ids.count())


print("\nOffers - Invalid College IDs")

invalid_college_ids = offers_df.join(
    colleges_df,
    offers_df["COLLEGE_ID"] == colleges_df["COLLEGE_ID"],
    "left_anti"
)

print("Invalid College IDs:", invalid_college_ids.count())
spark.stop()