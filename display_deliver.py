
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import connection_database

# Function to get remaining days to deliver from today
def remaining_days_to_deliver(delivery_date):
    today = datetime.now().date()
    remaining_days = (delivery_date - today).days
    return remaining_days

# Function to retrieve orders based on delivery date range
def retrieve_orders(start_date, end_date):
    conn = connection_database.db()
    query = f"SELECT * FROM customer_data WHERE delivery_date BETWEEN '{start_date}' AND '{end_date}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to display urgent orders
def display_urgent_orders(df):
    urgent_orders = df[df['delivery_date'] < datetime.now().date()]
    return urgent_orders

# Function to update delivery date
def update_delivery_date(order_id, new_delivery_date):
    conn = connection_database.db()
    cursor = conn.cursor()
    update_query = f"UPDATE customer_data SET delivery_date = '{new_delivery_date}' WHERE customer_id = {order_id}"
    cursor.execute(update_query)
    conn.commit()
    conn.close()

# Function to create delivery dashboard
def delivery_dashboard():
    st.title("Delivery Dashboard")

    # Date range selection
    st.sidebar.title("Date Range Selection")
    date_options = ["Today", "Tomorrow", "Within 7 days", "Within 30 days", "Within 180 days", "Custom"]
    selected_date_option = st.sidebar.selectbox("Select Date Range", date_options)

    # Calculate date range based on selected option
    if selected_date_option == "Today":
        start_date = datetime.now().date()
        end_date = start_date
    elif selected_date_option == "Tomorrow":
        start_date = datetime.now().date() + timedelta(days=1)
        end_date = start_date
    elif selected_date_option == "Within 7 days":
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=7)
    elif selected_date_option == "Within 30 days":
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=30)
    elif selected_date_option == "Within 180 days":
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=180)
    elif selected_date_option == "Custom":
        start_date = st.sidebar.date_input("Start Date", format= "DD-MM-YYYY")
        end_date = st.sidebar.date_input("End Date", value=datetime.now().date(), format= "DD-MM-YYYY")

    # Retrieve orders based on selected date range
    orders_df = retrieve_orders(start_date, end_date)

    # Remaining days to deliver
    remaining_days_df = orders_df.copy() 
    remaining_days_df['Remaining Days to Deliver'] = remaining_days_df['delivery_date'].apply(remaining_days_to_deliver)

    # Sort orders by remaining days to deliver
    remaining_days_df = remaining_days_df.sort_values(by='Remaining Days to Deliver')

    st.subheader("Orders Overview")
    st.write(f"Total Orders: {len(orders_df)}")

    # Display urgent orders
    urgent_orders_df = display_urgent_orders(orders_df)
    if not urgent_orders_df.empty:
        st.subheader("Urgent Orders")
        st.write(urgent_orders_df)

    # Display remaining days to deliver
    st.subheader("Remaining Days to Deliver")
    st.write(remaining_days_df[['customer_id','name', 'delivery_date', 'Remaining Days to Deliver']])

    # Group orders by garment type
    group_by_garment = st.checkbox("Group Orders by Garment Type")
    if group_by_garment:
        garment_groups = orders_df.groupby('category')
        st.subheader("Orders Grouped by Garment Type")
        for garment, group in garment_groups:
            total_orders = len(group)  # Calculate total orders for the current category
            st.write(f"**{garment}** - Total Orders: {total_orders}")  # Display total orders
            group['Remaining Days to Deliver'] = group['delivery_date'].apply(remaining_days_to_deliver)
            group = group.sort_values(by='Remaining Days to Deliver')
            st.write(group[['customer_id', 'name', 'delivery_date', 'category', 'Remaining Days to Deliver']])
        
    
    
        # Add section for today's orders to be delivered
    st.subheader("Today's Orders to be Delivered")
    today = datetime.now().date()
    todays_orders = orders_df[orders_df['delivery_date'] == today]

    # Filter orders by category
    categories = todays_orders['category'].unique()
    selected_categories = st.multiselect("Filter by Category", categories, default=categories)

    # Add clear filter option
    if st.button("Clear Filters"):
        selected_categories = []

    # Apply category filter
    filtered_orders = todays_orders[todays_orders['category'].isin(selected_categories)]

    # Display filtered orders
    if not filtered_orders.empty:
        st.write(filtered_orders)
    else:
        st.write("No orders to be delivered today.")
        
    # Add delivery date update option
    st.subheader("Update Delivery Date")
    order_id = st.text_input("Enter Order ID:")
    new_delivery_date = st.date_input("Enter New Delivery Date:")
    if st.button("Update Delivery Date"):
        if order_id and new_delivery_date:
            update_delivery_date(int(order_id), new_delivery_date)
            st.success("Delivery date updated successfully!")
        else:
            st.warning("Please enter valid Order ID and Delivery Date.")


