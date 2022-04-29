import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn import preprocessing
import streamlit as st


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
    # dfk['total_minutes'].min()
    train_data = dfk_3.apply(lambda x: (x - np.mean(x) / (np.std(x))))

    return train_data


def showClusterPlt(train_data):

    dfk_nor = train_data

    SSE = []  # 存放每次结果的误差平方和
    for k in range(1, 9):
        estimator = KMeans(n_clusters=k)  # 构造聚类器
        estimator.fit(dfk_nor)
        SSE.append(estimator.inertia_)  # estimator.inertia_获取聚类准则的总和

    X = range(1, 9)
    plt.xlabel("k")
    plt.ylabel("SSE")
    plt.plot(X, SSE, "o-")
    fig = plt.show()
    return fig


def inference(train_data, k):
    kmeans = KMeans(n_clusters=k)
    model = kmeans.fit(train_data)

    label_pred = model.labels_  # 获取聚类标签
    centroids = model.cluster_centers_  # 获取聚类中心
    inertia = model.inertia_  # 获取聚类准则的总和

    return label_pred


def getResultTable(dfk, label_pred):
    dfk["label_pred"] = list(label_pred)

    return dfk
