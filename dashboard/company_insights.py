import streamlit as st
import pandas as pd


def show_company_insights(conn):

    st.header("🏢 Company Insights")

    query = """
    SELECT
        COMPANY_NAME,
        INDUSTRY,
        TOTAL_OFFERS,
        STUDENTS_SELECTED,
        AVG_CTC_LPA,
        HIGHEST_CTC_LPA,
        STUDENTS_JOINED,
        JOIN_RATE_PERCENT
    FROM STUDENT_PLACEMENT_DB.ANALYTICS.VW_COMPANY_INSIGHTS
    ORDER BY TOTAL_OFFERS DESC
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No company placement data available.")
        return

    st.subheader("Offers by Company")

    st.bar_chart(
        df.set_index("COMPANY_NAME")["TOTAL_OFFERS"]
    )

    st.subheader("Average CTC by Company")

    ctc_df = df[
        ["COMPANY_NAME", "AVG_CTC_LPA"]
    ].set_index("COMPANY_NAME")

    st.bar_chart(ctc_df)

    st.subheader("Company Placement Details")

    st.dataframe(
        df,
        use_container_width=True
    )