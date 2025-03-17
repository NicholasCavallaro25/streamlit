import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment,Nicholas Cavallaro")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# Bar charts for category sales
st.bar_chart(df, x="Category", y="Sales")
st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Convert Order_Date to datetime and set index
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)

# Aggregating sales by month
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

# (1) 
categories = df["Category"].unique().tolist()
selected_category = st.selectbox("Select a Category:", categories)

# (2)
filtered_df = df[df["Category"] == selected_category]
sub_categories = filtered_df["Sub_Category"].unique().tolist()
selected_sub_categories = st.multiselect("Select Sub-Categories:", sub_categories, default=sub_categories[:2])

# Filter data based on selected sub-categories
filtered_data = filtered_df[filtered_df["Sub_Category"].isin(selected_sub_categories)]

# (3) 
sales_by_month_filtered = filtered_data.groupby(pd.Grouper(freq='M')).sum()
st.line_chart(sales_by_month_filtered, y="Sales")

# (4) 
if not filtered_data.empty:
    total_sales = filtered_data["Sales"].sum()
    total_profit = filtered_data["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    # (5) 
    overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
    profit_margin_delta = profit_margin - overall_profit_margin

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("Total Profit", f"${total_profit:,.2f}")
    with col3:
        st.metric("Profit Margin", f"{profit_margin:.2f}%", delta=f"{profit_margin_delta:.2f}%")
