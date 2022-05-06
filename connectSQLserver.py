import streamlit as st
import pyodbc


def app():
    # Initialize connection.
    # Uses st.experimental_singleton to only run once.
    @st.experimental_singleton
    def init_connection():
        return pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
            + st.secrets["server"]
            + ";DATABASE="
            + st.secrets["database"]
            + ";UID="
            + st.secrets["username"]
            + ";PWD="
            + st.secrets["password"]
        )

    conn = init_connection()

    # Perform query.
    # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    @st.experimental_memo(ttl=600)
    def run_query(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    rows = run_query(
        "SELECT id,order_number_id,customer_id,minutes,created_at,location_name,formatted_source,payment_method_type,transaction_type,rate_group_name,channel_code,channel_type,customer_type,product_type FROM dbo.LocationRevenues WHERE year(created_at) = 2022 limit 100;"
    )

    # Print results.
    for row in rows:
        st.write(f"{row[0]} has a :{row[1]}:")
