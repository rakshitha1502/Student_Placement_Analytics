import streamlit as st
import pandas as pd


def show_data_quality(conn):

    st.header("✅ Data Quality")

    query = """
    SELECT *
    FROM STUDENT_PLACEMENT_DB.ANALYTICS.VW_DATA_QUALITY_SUMMARY
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No data quality information available.")
        return

    data = df.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Raw Offers", data["RAW_OFFER_COUNT"])
    col2.metric("Fact Offers", data["FACT_OFFER_COUNT"])
    col3.metric("Invalid CTC", data["INVALID_CTC_COUNT"])
    col4.metric(
        "Critical Field Errors",
        data["INVALID_CRITICAL_FIELD_COUNT"]
    )

    st.divider()

    st.subheader("Data Quality Status")

    if (
        data["INVALID_CTC_COUNT"] == 0
        and data["INVALID_CRITICAL_FIELD_COUNT"] == 0
        and data["RAW_OFFER_COUNT"] == data["FACT_OFFER_COUNT"]
    ):
        st.success("✅ All data quality checks passed.")
    else:
        st.error("❌ Data quality issues detected.")

    st.subheader("Data Quality Summary")

    st.dataframe(
        df,
        use_container_width=True
    )