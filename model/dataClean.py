import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def data_clean(df):

    df["minutes"] = df["minutes"].fillna(180)  # 180 = minutes mode
    # df['total_amount'].median() = 10.47
    df["total_amount"] = df["total_amount"].apply(lambda x: 10.47 if x <= 0 else x)

    # find the frequency of transaction for each customer
    df2 = df.groupby(by="customer_id")[["order_number_id"]].count()
    df2.rename(columns={"order_number_id": "frequency"}, inplace=True)

    # merge to the whole data
    df3 = pd.merge(df, df2, on="customer_id")
    df4 = df.groupby(by=["customer_id", "location_name"])[["order_number_id"]].count()
    # find a customer has parked one or more places
    df5 = df4.groupby(by=["customer_id"]).count()
    df5.rename(columns={"order_number_id": "number_of_locations"}, inplace=True)
    df6 = pd.merge(df3, df5, on="customer_id")
    df7 = df6.groupby(by="customer_id")[["minutes"]].sum()
    df8 = df6.groupby(by="customer_id")[["total_amount"]].sum()
    df7.rename(columns={"minutes": "total_minutes"}, inplace=True)
    df8.rename(columns={"total_amount": "total_amount_user"}, inplace=True)
    df9 = pd.merge(df7, df8, on="customer_id")
    df_new = pd.merge(df6, df9, on="customer_id")

    # find the most popular things for a customer
    dfb = df_new.groupby(by=["customer_id", "formatted_source"])[
        ["order_number_id"]
    ].count()
    g = dfb.reset_index().groupby(["customer_id"])["order_number_id"].idxmax()
    dfb = dfb.reset_index("formatted_source")
    dfb.rename(columns={"formatted_source": "popular_formatted_source"}, inplace=True)
    dfc = dfb.iloc[g]

    dfc.drop(columns=["order_number_id"], inplace=True)

    df_new = pd.merge(df_new, dfc, on="customer_id")

    dfb = df_new.groupby(by=["customer_id", "payment_method_type"])[
        ["order_number_id"]
    ].count()
    g = dfb.reset_index().groupby(["customer_id"])["order_number_id"].idxmax()
    dfb = dfb.reset_index("payment_method_type")
    dfb.rename(
        columns={"payment_method_type": "popular_payment_method_type"}, inplace=True
    )
    dfc = dfb.iloc[g]
    dfc.drop(columns=["order_number_id"], inplace=True)

    df_new = pd.merge(df_new, dfc, on="customer_id")

    dfb = df_new.groupby(by=["customer_id", "transaction_type"])[
        ["order_number_id"]
    ].count()
    g = dfb.reset_index().groupby(["customer_id"])["order_number_id"].idxmax()
    dfb = dfb.reset_index("transaction_type")
    dfb.rename(columns={"transaction_type": "popular_transaction_type"}, inplace=True)
    dfc = dfb.iloc[g]
    dfc.drop(columns=["order_number_id"], inplace=True)

    df_new = pd.merge(df_new, dfc, on="customer_id")

    dfb = df_new.groupby(by=["customer_id", "customer_type"])[
        ["order_number_id"]
    ].count()
    g = dfb.reset_index().groupby(["customer_id"])["order_number_id"].idxmax()
    dfb = dfb.reset_index("customer_type")
    dfb.rename(columns={"customer_type": "popular_customer_type"}, inplace=True)
    dfc = dfb.iloc[g]
    dfc.drop(columns=["order_number_id"], inplace=True)

    df_new = pd.merge(df_new, dfc, on="customer_id")

    dfb = df_new.groupby(by=["customer_id", "product_type"])[
        ["order_number_id"]
    ].count()
    g = dfb.reset_index().groupby(["customer_id"])["order_number_id"].idxmax()
    dfb = dfb.reset_index("product_type")
    dfb.rename(columns={"product_type": "popular_product_type"}, inplace=True)
    dfc = dfb.iloc[g]
    dfc.drop(columns=["order_number_id"], inplace=True)

    df_new = pd.merge(df_new, dfc, on="customer_id")

    df_new.drop(
        columns=[
            "order_number_id",
            "minutes",
            "total_amount",
            "formatted_source",
            "payment_method_type",
            "transaction_type",
            "customer_type",
            "product_type",
        ],
        inplace=True,
    )

    df_new.drop_duplicates("customer_id", "first", inplace=True)

    return df_new
