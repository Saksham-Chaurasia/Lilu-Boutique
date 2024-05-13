
import streamlit as st
from datetime import datetime, timedelta
import connection_database
import pandas as pd
import plotly.express as px
from datetime import datetime , date
import status


def editing():
    with st.expander("Edit"):
        # Input field for Order ID
        customer_id = st.text_input("Enter Customer ID:", key="customer_id_input")
        column_order = ["Customer ID", "Name", "Phone", "Email", "Order Date", "Delivery Date", "Garment Type", "Status"]
        
        # If Customer ID is provided
        if customer_id:
            current_values = retrieve_order_details(customer_id)  
            df = pd.DataFrame(current_values, index=[0])
            if current_values: 
                # Display the DataFrame with selected columns
                st.write("Current Order Details:")
                st.dataframe(df[["Customer ID", "Name", "Phone", "Email", "Order Date", "Delivery Date", "Garment Type", "Status"]])
                
                # Input fields for updating order attributes
                new_values = {}
                with st.container(border=True):
                    st.subheader("Updation", divider="grey")
                    for column in column_order:
                        if column == "Customer ID" or column == "Submission Date":
                            continue  # Skip updating Customer ID and Submission Date
                        elif column == "Status":
                            new_value = st.selectbox(f"Select new value for {column}:", ["Delivered", "Cancelled", "Extended", "Overdue", "Ordered"])
                        elif column in ["Order Date", "Delivery Date"]:
                            st.write(f"Current {column}: {current_values[column]}")
                            if current_values[column] is not None:
                                current_date = datetime.strptime(current_values[column], "%d-%m-%Y").date()
                            else:
                                current_date = None
                            new_date = st.date_input(f"Enter new value for {column}:", current_date, format="DD-MM-YYYY")
                            new_value = new_date.strftime("%Y-%m-%d") if new_date else None
                        else:
                            new_value = st.text_input(f"Enter new value for {column}:", current_values[column])
                        new_values[column] = new_value
                    
                # Button to update the order
                if st.button("Update Order"):
                    if new_values:
                        update_order(customer_id, new_values)
                        st.success("Order updated successfully!")
                    else:
                        st.warning("No columns selected for update.")
            else:
                st.warning("Customer ID not found.")
def update_order(customer_id, new_values):
    conn = connection_database.db()
    cursor = conn.cursor()
    
    # Construct the SQL UPDATE query
    update_query = "UPDATE customer_data SET "
    for column, value in new_values.items():
        # Properly escape column names with backticks
        if column == "Order Date":
            column = "dates"
        elif column == "Customer ID":
            column = "customer_id"
        elif column == "Name":
            column = "name"
        elif column == "Mobile Number":
            column = "phone"
        elif column == "Email":
            column = "email"
        elif column == "Delivery Date":
            column = "delivery_date"
        elif column == "Garment Type":
            column = "category"
        elif column == "Submission Date":
            column = "registration_date"
        elif column == "Status":
            column = "status"
        
        # Handle 'None' values
        if value is None:
            update_query += f"`{column.replace(' ', '_')}` = NULL, "
        else:
            update_query += f"`{column.replace(' ', '_')}` = '{value}', "
    
    update_query = update_query[:-2]  # Remove the trailing comma and space
    update_query += f" WHERE customer_id = '{customer_id}'"
    
    # Execute the update query
    cursor.execute(update_query)
    conn.commit()
    conn.close()




def retrieve_order_details(customer_id):
    conn = connection_database.db()
    cursor = conn.cursor()
    
    # Construct the SQL query to retrieve order details based on Order ID
    query = f"SELECT * FROM customer_data WHERE customer_id = '{customer_id}'"
    
    # Execute the query
    cursor.execute(query)
    result = cursor.fetchone()  # Assuming only one row will be returned
    
    if result:
        order_details = {}
        column_names = ["Customer ID", "Order Date", "Name", "Phone", "Email", "Delivery Date", "Garment Type", "Submission Date", "Status"]
        for i, value in enumerate(result):
            # Check if the column is a datetime column and format it accordingly
            if column_names[i] in ["Order Date", "Delivery Date", "Submission Date"]:
                if isinstance(value, date):
                    order_details[column_names[i]] = value.strftime('%d-%m-%Y')
                else:
                    order_details[column_names[i]] = value
            else:
                order_details[column_names[i]] = value
        return order_details
    else:
        return None



# Function to retrieve orders based on status and delivery date range
def retrieve_orders(status_list, start_date, end_date):
    conn = connection_database.db()
    status_filter = "','".join(status_list)  # Join status list with commas
    query = f"SELECT * FROM customer_data WHERE status IN ('{status_filter}') AND delivery_date BETWEEN '{start_date}' AND '{end_date}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def delivery_dashboard():
    # Initial state of checkboxes
    all_checked = True
    order_checked = False
    deliver_checked = False
    cancel_checked = False
    overdue_checked = False
    extended_checked = False
    
    # Popover for selecting status
    st.sidebar.divider()
    with st.sidebar.expander("Select Status"):
        all_checked = st.checkbox("All", value=all_checked)
        order_checked = st.checkbox("Ordered", value=order_checked)
        deliver_checked = st.checkbox("Delivered", value=deliver_checked)
        cancel_checked = st.checkbox("Cancelled", value=cancel_checked)
        overdue_checked = st.checkbox("Overdue", value=overdue_checked)
        extended_checked = st.checkbox("Extended", value=extended_checked)

        # Logic to deselect "All" if any other checkbox is selected
        if any([order_checked, deliver_checked, cancel_checked, overdue_checked, extended_checked]):
            all_checked = False
            
        
    # Convert status checkboxes to lowercase strings for SQL query
    status_list = []
    if all_checked:
        status_list = ["ordered", "delivered", "cancelled", "overdue", "extended"]
    else:
        if order_checked:
            status_list.append("ordered")
        if deliver_checked:
            status_list.append("delivered")
        if cancel_checked:
            status_list.append("cancelled")
        if overdue_checked:
            status_list.append("overdue")
        if extended_checked:
            status_list.append("extended")

    with st.container(border=True):
        # Date range selection
        st.subheader("Date Range Selection")
        date_options = ["Custom","Today", "Tomorrow", "Within 7 days", "Within 30 days", "Within 180 days"]
        selected_date_option = st.selectbox("Select Date Range", date_options)

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
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", value=datetime.now().date(), format="DD-MM-YYYY")
            with col2:
                end_date = st.date_input("End Date", value=datetime.now().date() + timedelta(days=7), format="DD-MM-YYYY")

    # Retrieve orders based on selected status and date range
    orders_df = retrieve_orders(status_list, start_date, end_date)
    
    with st.container(border=True):
        if not orders_df.empty:
            # orders by category wise
            st.subheader("Category wise orders", divider="grey")
            category_counts = orders_df['category'].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            fig = px.bar(category_counts, x = "Category", y = "Count", text = "Count", template = "seaborn", color = "Category", color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig)
        else:
            st.write("No data available for bar chart.")

    with st.container(border=True):
        if not orders_df.empty:
            # orders by category wise
            st.subheader("Status wise orders", divider="grey")
            # Group by status and count
            status_counts = orders_df['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']

            fig = px.pie(status_counts, values='Count', names='Status', hole=0.5,color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(text=status_counts['Status'], textposition="inside")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig)
        else:
            st.write("No data available for pie chart.")


    # Display orders and download data
    with st.expander("Status Wise Data"):
        if not orders_df.empty:
            st.write(orders_df.style.background_gradient(cmap='Oranges'))
            csv = orders_df.to_csv(index=False).encode('utf8')
            st.download_button("Download Data", data=csv, file_name="Status.csv", mime="text/csv",
                            help="Click here to download the data as a CSV file")
        else:
            st.write("No orders found for the selected criteria.")

    # Display orders and download data
    with st.expander("Category Wise Data"):
        if not orders_df.empty:
            # Display unique categories and let the user choose
            selected_category = st.selectbox("Select Category", sorted(orders_df["category"].unique()))
            
            # Filter the DataFrame based on the selected category
            category_df = orders_df[orders_df["category"] == selected_category]
            
            if not category_df.empty:
                st.write(category_df)
                csv = category_df.to_csv(index=False).encode('utf8')
                st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv",
                                help="Click here to download the data as a CSV file")
            else:
                st.write("No orders found for the selected category.")
        else:
            st.write("No orders found for the selected criteria.")

    editing()






    
   


