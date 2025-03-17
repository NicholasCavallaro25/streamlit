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
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")

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

            # ---- METRICS ----
            total_sales = filtered_df['Sales'].sum()
            total_profit = filtered_df['Profit'].sum()
            profit_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0

            # Display Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Sales ($)", f"${total_sales:,.2f}")
            col2.metric("Total Profit ($)", f"${total_profit:,.2f}")
            col3.metric("Profit Margin (%)", f"{profit_margin:.2f}%")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
