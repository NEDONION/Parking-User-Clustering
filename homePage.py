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
            We provide **end-to-end** machine learning solutions for typical user segmentation problems, including data preprocess, training, and prediction. It's easy to use, quick to modify, and deployed on the Streamlit Cloud.
             """
    )

    space(1)
