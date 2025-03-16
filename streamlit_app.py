import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")



import streamlit as st
import pandas as pd

st.title("Superstore Sales Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=['Order_Date'])
    df.columns = df.columns.str.strip()  # Fix column name issues
    return df

df = load_data()

# Check column names
st.write("### Column Names in DataFrame")
st.write(df.columns)

# Check data preview
st.write("### Data Preview")
st.dataframe(df.head())

# Dropdown for category selection
category = st.selectbox("Select a Category", df["Category"].unique())

# Ensure sub-category selection only works if data exists
filtered_df = df[df["Category"] == category]

if not filtered_df.empty:
    sub_categories = st.multiselect("Select Sub-Categories", filtered_df["Sub-Category"].unique())
else:
    st.warning("No data found for this category. Please choose another.")



# (1) Dropdown for Category Selection
category = st.selectbox("Select a Category", df["Category"].unique())

# (2) Multi-Select for Sub-Category
filtered_df = df[df["Category"] == category]
sub_categories = st.multiselect("Select Sub-Categories", filtered_df["Sub-Category"].unique())

if sub_categories:
    # (3) Show a line chart of sales for the selected sub-categories
    sub_df = filtered_df[filtered_df["Sub-Category"].isin(sub_categories)]
    sales_by_month_sub = sub_df.groupby([pd.Grouper(freq='M'), "Sub-Category"])["Sales"].sum().unstack()
    
    st.line_chart(sales_by_month_sub)

    # (4) Metrics for selected items
    total_sales = sub_df["Sales"].sum()
    total_profit = sub_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    
    # (5) Delta for Profit Margin (compared to overall average)
    overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
    delta = profit_margin - overall_profit_margin
    
    st.metric(label="Profit Margin (%)", value=f"{profit_margin:.2f}%", delta=f"{delta:.2f}%")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
