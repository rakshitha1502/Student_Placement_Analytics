import streamlit as st
import pandas as pd


def show_college_performance(conn):

    st.header("🏫 College Performance")

    query = """
    SELECT
        COLLEGE_NAME,
        TOTAL_OFFERS,
        STUDENTS_PLACED,
        AVG_CTC_LPA,
        HIGHEST_CTC_LPA,
        STUDENTS_JOINED,
        JOIN_RATE_PERCENT
    FROM STUDENT_PLACEMENT_DB.ANALYTICS.VW_COLLEGE_PERFORMANCE
    ORDER BY TOTAL_OFFERS DESC
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No college placement data available.")
        return

    st.subheader("Offers by College")

    st.bar_chart(
        df.set_index("COLLEGE_NAME")["TOTAL_OFFERS"]
    )

    st.subheader("Average CTC by College")

    ctc_df = df[
        ["COLLEGE_NAME", "AVG_CTC_LPA"]
    ].set_index("COLLEGE_NAME")

    st.bar_chart(ctc_df)

    st.subheader("College Placement Details")

    st.dataframe(
        df,
        use_container_width=True
    )