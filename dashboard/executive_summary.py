import streamlit as st
import pandas as pd


def show_executive_summary(conn):

    st.header("🎓 Executive Summary")

    query = """
    SELECT *
    FROM STUDENT_PLACEMENT_DB.ANALYTICS.VW_EXECUTIVE_SUMMARY
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No placement data available.")
        return

    data = df.iloc[0]

    # KPI Section
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Offers",
        data["TOTAL_OFFERS"]
    )

    col2.metric(
        "Students Placed",
        data["STUDENTS_PLACED"]
    )

    col3.metric(
        "Companies Hiring",
        data["COMPANIES_HIRING"]
    )

    col4.metric(
        "Colleges",
        data["COLLEGES_WITH_PLACEMENTS"]
    )

    st.divider()

    # Additional KPIs
    col5, col6, col7 = st.columns(3)

    col5.metric(
        "Average CTC (LPA)",
        data["AVG_CTC_LPA"]
    )

    col6.metric(
        "Highest CTC (LPA)",
        data["HIGHEST_CTC_LPA"]
    )

    col7.metric(
        "Join Rate",
        f'{data["JOIN_RATE_PERCENT"]}%'
    )

    st.divider()

    # Placement Status Chart
    st.subheader("Placement Status")

    status_query = """
    SELECT
        OFFER_STATUS,
        COUNT(*) AS OFFER_COUNT
    FROM STUDENT_PLACEMENT_DB.ANALYTICS.VW_PLACEMENT_ANALYTICS
    GROUP BY OFFER_STATUS
    ORDER BY OFFER_COUNT DESC
    """

    status_df = pd.read_sql(
        status_query,
        conn
    )

    if not status_df.empty:
        st.bar_chart(
            status_df.set_index("OFFER_STATUS")["OFFER_COUNT"]
        )
    else:
        st.warning("No placement status data available.")