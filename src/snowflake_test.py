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
    schema="ANALYTICS"
)

print("Snowflake connection successful!")

conn.close()