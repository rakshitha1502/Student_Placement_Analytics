import streamlit as st
import snowflake.connector
import os
from dotenv import load_dotenv

from executive_summary import show_executive_summary
from college_performance import show_college_performance
from company_insights import show_company_insights
from placement_explorer import show_placement_explorer
from data_quality import show_data_quality


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Student Placement Analytics",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# Snowflake Connection
# --------------------------------------------------

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse="PLACEMENT_WH",
    database="STUDENT_PLACEMENT_DB",
    schema="ANALYTICS"
)


# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------

st.sidebar.title("🎓 Placement Analytics")

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Summary",
        "College Performance",
        "Company Insights",
        "Placement Explorer",
        "Data Quality"
    ]
)

# --------------------------------------------------
# Display Selected Page
# --------------------------------------------------

if page == "Executive Summary":

    show_executive_summary(conn)

elif page == "College Performance":

    show_college_performance(conn)

elif page == "Company Insights":

    show_company_insights(conn)

elif page == "Placement Explorer":

    show_placement_explorer(conn)

elif page == "Data Quality":
    show_data_quality(conn)

# --------------------------------------------------
# Close Connection
# --------------------------------------------------

conn.close()