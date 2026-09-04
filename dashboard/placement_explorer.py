import streamlit as st
import pandas as pd


def show_placement_explorer(conn):

    st.header("🔎 Placement Explorer")

    query = """
    SELECT
        OFFER_ID,
        OFFER_DATE,
        STUDENT_ID,
        FIRST_NAME,
        LAST_NAME,
        COLLEGE_NAME,
        COMPANY_NAME,
        INDUSTRY,
        ROLE_TITLE,
        CTC_LPA,
        OFFER_STATUS,
        IS_JOINED
    FROM STUDENT_PLACEMENT_DB.ANALYTICS.VW_PLACEMENT_EXPLORER
    ORDER BY OFFER_DATE DESC
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No placement data available.")
        return

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        college_options = ["All"] + sorted(
            df["COLLEGE_NAME"].dropna().unique().tolist()
        )

        selected_college = st.selectbox(
            "College",
            college_options
        )

    with col2:
        company_options = ["All"] + sorted(
            df["COMPANY_NAME"].dropna().unique().tolist()
        )

        selected_company = st.selectbox(
            "Company",
            company_options
        )

    with col3:
        status_options = ["All"] + sorted(
            df["OFFER_STATUS"].dropna().unique().tolist()
        )

        selected_status = st.selectbox(
            "Offer Status",
            status_options
        )

    # CTC Filter
    st.subheader("CTC Filter")

    min_ctc = float(df["CTC_LPA"].min())
    max_ctc = float(df["CTC_LPA"].max())

    selected_ctc = st.slider(
        "Select CTC range (LPA)",
        min_value=min_ctc,
        max_value=max_ctc,
        value=(min_ctc, max_ctc)
    )

    # Apply filters
    filtered_df = df.copy()

    if selected_college != "All":
        filtered_df = filtered_df[
            filtered_df["COLLEGE_NAME"] == selected_college
        ]

    if selected_company != "All":
        filtered_df = filtered_df[
            filtered_df["COMPANY_NAME"] == selected_company
        ]

    if selected_status != "All":
        filtered_df = filtered_df[
            filtered_df["OFFER_STATUS"] == selected_status
        ]

    filtered_df = filtered_df[
        (filtered_df["CTC_LPA"] >= selected_ctc[0]) &
        (filtered_df["CTC_LPA"] <= selected_ctc[1])
    ]

    # Record count
    st.write(
        f"Showing **{len(filtered_df)}** placement records"
    )

    # Top Job Roles
    st.subheader("Top Job Roles by Offers")

    role_df = (
        filtered_df
        .groupby("ROLE_TITLE")
        .size()
        .reset_index(name="OFFER_COUNT")
        .sort_values("OFFER_COUNT", ascending=False)
        .head(10)
    )

    if not role_df.empty:
        st.bar_chart(
            role_df.set_index("ROLE_TITLE")["OFFER_COUNT"]
        )
    else:
        st.info("No job role data available for the selected filters.")

    # Results
    st.subheader("Placement Records")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )