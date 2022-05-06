import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn import preprocessing
import streamlit as st
import seaborn as sns


def preprocess(df):
    df1 = df[df.frequency <= 300]

    df1 = df1[df1.total_minutes <= 100000]
    df1.drop(columns=["Unnamed: 0"], inplace=True)

    dfk = df1[
        [
            "customer_id",
            "frequency",
            "number_of_locations",
            "total_minutes",
            "total_amount_user",
        ]
    ]

    dfk = dfk.set_index("customer_id")

    # using normalazation instead of guiyi due to max big and min =1

    dfk_3 = pow(dfk, 1 / 3)
    train_data = dfk_3.apply(lambda x: (x - np.mean(x) / (np.std(x))))

    return train_data


def showClusterPlt(train_data):
    """
    draw elbow pic
    """
    dfk_nor = train_data

    SSE = []  # 存放每次结果的误差平方和
    for k in range(1, 9):
        estimator = KMeans(n_clusters=k)  # new Kmeans instance
        estimator.fit(dfk_nor)
        SSE.append(estimator.inertia_)  # estimator.inertia_获取聚类准则的总和

    st.header("Elbow Point")

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.lineplot(x=list(range(1, 9)), y=SSE, ax=ax)
    ax.set_title("Searching for Elbow")
    ax.set_xlabel("Clusters")
    ax.set_ylabel("Inertia")
    st.pyplot(fig)


def inference(train_data, k):
    kmeans = KMeans(n_clusters=k)
    model = kmeans.fit(train_data)

    label_pred = model.labels_  # get cluster labels
    centroids = model.cluster_centers_  # get cluster center
    inertia = model.inertia_  # 获取聚类准则的总和

    return label_pred


def getResultTable(dfk, label_pred):
    dfk["label_pred"] = list(label_pred)

    return dfk


def drawClusterPic(df, label_pred, clustersNumber):

    df1 = df[df.frequency <= 300]
    df1 = df1[df1.total_minutes <= 100000]
    df1.drop(columns=["Unnamed: 0"], inplace=True)
    dfk = df1[
        [
            "customer_id",
            "frequency",
            "number_of_locations",
            "total_minutes",
            "total_amount_user",
        ]
    ]
    dfk = dfk.set_index("customer_id")
    dfk["label_pred"] = list(label_pred)

    # randomly select
    X = dfk.sample(n=1000, random_state=88)
    km_header = st.empty()
    km_plot = st.empty()

    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        X["total_amount_user"],
        X["total_minutes"],
        hue=X["label_pred"],
        markers=True,
        size=X["label_pred"],
        palette=sns.color_palette("hls", clustersNumber),
    )

    for label in X["label_pred"]:
        plt.annotate(
            label,
            (
                X[X["label_pred"] == label]["total_amount_user"].mean(),
                X[X["label_pred"] == label]["total_minutes"].mean(),
            ),
            horizontalalignment="center",
            verticalalignment="center",
            size=20,
            weight="bold",
            color="black",
        )
    # #                  #backgroundcolor=customPalette[i])

    km_header.header("User distribution in different clusters")
    km_plot.pyplot()
