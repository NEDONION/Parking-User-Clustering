import streamlit as st
import pandas as pd
import time

from model import dataClean
from model import clustering


def app():
    # setting
    st.set_option("deprecation.showPyplotGlobalUse", False)

    def space(n):
        for i in range(n):
            st.markdown(" ")

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")

    st.markdown(
        "<h3 style='text-align: left; color:#F63366; font-size:24px;'><b>SQL code for querying the raw data<b></h3>",
        unsafe_allow_html=True,
    )

    st.write(
        """
            - Replace the `year(created_at)` into other years.
            - Memory limit of 200MB for a single csv file
            - We used Python to do some complex data processing, and this part of the code is more difficult to maintain. 
            - In the future, we recommend using more easily queried data features and using SQL to do the aggregation of data.
             """
    )

    code = """
    SELECT [id]
      ,[order_number_id]
      ,[customer_id]
      ,[minutes]
      ,[created_at]
      ,[location_name]
      ,[formatted_source]
      ,[payment_method_type]
      ,[transaction_type]
      ,[rate_group_name]
      ,[channel_code]
      ,[channel_type]
      ,[customer_type]
      ,[product_type]
  FROM [dbo].[LocationRevenues]
 WHERE year(created_at) = 2022;
    """
    st.code(code, language="sql")

    space(1)

    st.markdown(
        "<h3 style='text-align: left; color:#F63366; font-size:24px;'><b>Data preprocess<b></h3>",
        unsafe_allow_html=True,
    )
    uploaded_raw_data = st.file_uploader(
        "Choose the raw data (The process takes 3-5 minutes)"
    )

    if uploaded_raw_data is not None:

        st.markdown(" --- ")
        if st.button("Clean the raw data"):
            # with st.spinner("Processing..."):
            #     time.sleep(1)

            df = pd.read_csv(uploaded_raw_data)
            df_new = dataClean.data_clean(df)
            st.write("Let's take a look at the data after data clean")
            st.write(df_new.head(5))

            trainData = convert_df(df_new)
            st.success("Done!")

            st.download_button(
                label="Download the train data as CSV",
                data=trainData,
                file_name="trainData.csv",
                mime="text/csv",
            )

    space(1)
    st.markdown(
        "<h3 style='text-align: left; color:#F63366; font-size:24px;'><b>Dataset features<b></h3>",
        unsafe_allow_html=True,
    )

    st.write(
        """
        - **frequency**: user's total number of parking
        - **number of locations**: for each user  total number of lot they had parked
        - **total_minutes**: total minutes used by this user
        - **total_amount**: total amount spent by this user
        - **popular_formatted_source**: the most often used device type
        - **popular_payment_method_type**: the most often used payment method type
        - **popular_transaction_type**: the most often used transaction type
        - **popular_customer_type**: the most often used device type
        - **popular_product_type**: the most often used product type
              
             """
    )

    space(1)
    st.markdown(
        "<h3 style='text-align: left; color:#F63366; font-size:24px;'><b>Model training and prediction<b></h3>",
        unsafe_allow_html=True,
    )
    st.write(
        """
        - Step1. Import the train dataset
        - Step2. Train and choose the number of clusters
        - Step3. Predict
        - Step4. Save the results csv
              
        """
    )

    uploaded_train_data = st.file_uploader("Already has the train data")

    if uploaded_train_data is not None:

        st.markdown(" --- ")
        train_data = pd.read_csv(uploaded_train_data)
        clean_data = clustering.preprocess(train_data)

        # show the elbow pic
        clustering.showClusterPlt(clean_data)

        clustersNumber = st.number_input(
            "Number of clusters (1 - 9)",
            value=1,
            step=1,
            max_value=9,
            min_value=1,
        )
        st.write("The current clustersNumber is ", clustersNumber)

        if st.button("Predict and get results"):
            label_pred = clustering.inference(clean_data, k=clustersNumber)

            # get result table
            resultTable = clustering.getResultTable(clean_data, label_pred)
            # draw the cluter points pic
            clustering.drawClusterPic(train_data, label_pred, clustersNumber)

            resultTableCsv = convert_df(resultTable)
            st.write(resultTable.head(5))
            st.success("Done!")

            st.download_button(
                label="Download resultTable as CSV",
                data=resultTableCsv,
                file_name="resultTableCsv.csv",
                mime="text/csv",
            )
