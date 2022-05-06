import streamlit as st
import pandas as pd
import time

from model import dataClean
from model import clustering


def app():
    # setting
    # st.set_option("deprecation.showPyplotGlobalUse", False)

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
    uploaded_raw_data = st.file_uploader("Choose the raw data")

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
        "<h3 style='text-align: left; color:#F63366; font-size:24px;'><b>Model training and prediction<b></h3>",
        unsafe_allow_html=True,
    )
    uploaded_train_data = st.file_uploader("Already has the train data")

    @st.cache(allow_output_mutation=True)
    def trainAndShow(uploaded_train_data):
        train_data = pd.read_csv(uploaded_train_data)
        # preprocess for data
        clean_data = clustering.preprocess(train_data)
        # train
        fig = clustering.showClusterPlt(clean_data)
        return fig, clean_data

    if uploaded_train_data is not None:

        st.markdown(" --- ")

        # 加缓存
        fig, clean_data = trainAndShow(uploaded_train_data)
        st.pyplot(fig)

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

            resultTableCsv = convert_df(resultTable)

            st.write(resultTable.head(5))
            st.success("Done!")

            st.download_button(
                label="Download resultTable as CSV",
                data=resultTableCsv,
                file_name="resultTableCsv.csv",
                mime="text/csv",
            )
