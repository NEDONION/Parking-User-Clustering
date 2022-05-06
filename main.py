from operator import imod
import streamlit as st
import homePage
import modelPage

# import connectSQLserver
from multiapp import MultiApp
from PIL import Image

#############
# PAGE SET UP
#############

# ICON = Image.open("img/icon2.png")

st.set_page_config(
    page_title="User Clustering App for Premium Parking",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)


app = MultiApp()
app.add_app("Homepage", homePage.app)
app.add_app("Model Page", modelPage.app)
# app.add_app("Connect to SQL Server", connectSQLserver.app)
# app.add_app("Connect to AWS Service", awsPredict.app)
app.run()
