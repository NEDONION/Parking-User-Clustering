from numpy import full
import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns


def app():
    # setting
    # st.set_option("deprecation.showPyplotGlobalUse", False)

    def space(n):
        for i in range(n):
            st.markdown(" ")

    # image = Image.open("static/homepage.jpg")
    # st.image(
    #     image,
    #     caption=None,
    #     # width=1200,
    #     use_column_width=None,
    #     clamp=False,
    #     channels="RGB",
    #     output_format="auto",
    # )

    # html语法设置主页
    st.markdown(
        "<h1 style='text-align: center; '>User Segmentation for Premium Parking</h1>",
        unsafe_allow_html=True,
    )
    # st.markdown("<h3 style='text-align: center; font-size:56px;'<p>&#129302;</p></h3>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='text-align: center; color: grey; font-size:20px;'>An application for user clustering.</h3>",
        unsafe_allow_html=True,
    )

    space(1)

    st.markdown(
        "<h3 style='text-align: left; color:#F63366; font-size:24px;'><b>What is this App about?<b></h3>",
        unsafe_allow_html=True,
    )
    st.write(
        """
             Whether you want to borrow money to buy real estate, cars or to open up a start-up, **Borrow Faster** offers a quick credit evaluation to help you judge whether you are eligible for the Lending Club loan application. With a user-friendly interface, and offering many evaluation models for loan applicants.
             """
    )

    space(1)

    df = pd.read_csv("data/data_final.csv")
    x = pd.DataFrame(df)
    # freguency > 3 * 100 (assume parking 3 times a day during 2022) is dirty data drop them
    df1 = df[df.frequency <= 300]
    df1 = df1[df1.total_minutes <= 100000]
    df1.drop(columns=["Unnamed: 0"], inplace=True)

    st.write(df1)
