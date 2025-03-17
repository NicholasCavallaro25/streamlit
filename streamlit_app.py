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



category = st.selectbox("Select a Category", df['Category'].unique())
sub_categories = df[df['Category'] == category]['Sub_Category'].unique()
selected_sub_categories = st.multiselect(
    "Select Sub-Categories",
    sub_categories,
    sub_categories
)

st.write("### (3) show a line chart of sales for the selected items in (2)")

import streamlit as st
import pandas as pd

# Load the dataset
file_path = "/mnt/data/Superstore_Sales_utf8.csv"
df = pd.read_csv(file_path)

# Clean column names (strip spaces)
df.columns = df.columns.str.strip()

# Ensure necessary columns exist
required_columns = {'Category', 'Sub_Category', 'Order Date', 'Sales'}
if required_columns.issubset(df.columns):
    # Convert 'Order Date' to datetime safely
    try:
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    except Exception as e:
        st.error(f"Error converting 'Order Date' to datetime: {e}")

    # Select a Category
    category = st.selectbox("Select a Category", df['Category'].unique())

    # Filter Sub_Categories based on selected Category
    sub_categories = df[df['Category'] == category]['Sub_Category'].unique()

    # Multi-select for Sub_Category (default selects all subcategories)
    selected_sub_categories = st.multiselect(
        "Select Sub-Categories",
        sub_categories,
        sub_categories  # Pre-select all subcategories by default
    )

    # Display selected options
    st.write("You selected:", selected_sub_categories)

    # Filter data based on selections
    if selected_sub_categories:
        filtered_df = df[(df['Category'] == category) & (df['Sub_Category'].isin(selected_sub_categories))]

        # Check if 'Order Date' has valid values after conversion
        if filtered_df['Order Date'].isna().all():
            st.error("All 'Order Date' values are invalid. Please check the dataset format.")
        else:
            # Drop rows with NaT values in 'Order Date'
            filtered_df = filtered_df.dropna(subset=['Order Date'])

            # Aggregate sales by date
            sales_trend = filtered_df.groupby('Order Date')['Sales'].sum().reset_index()

            # Show the filtered data
            st.write("### Filtered Data", filtered_df)

            # Show the line chart
            st.write("### Sales Trend Over Time")
            st.line_chart(sales_trend.set_index('Order Date'))

    else:
        st.write("### Select Sub-Categories to view data and chart")
else:
    st.error(f"Dataset is missing required columns: {required_columns - set(df.columns)}")


st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
