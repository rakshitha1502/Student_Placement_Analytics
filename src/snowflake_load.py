import os
import snowflake.connector
from dotenv import load_dotenv

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
SELECT COUNT(*)
FROM STUDENT_PLACEMENT_DB.STAGING.STG_PLACEMENT
""")

result = cursor.fetchone()

print("Current STG_PLACEMENT records:", result[0])

cursor.close()
conn.close()

print("Snowflake ETL connection successful!")