import connection_database
from datetime import datetime


# Function to update delivery date # extended status
def update_extended_status(order_id):
    conn = connection_database.db()
    cursor = conn.cursor()
    update_query = f"UPDATE customer_data SET status = 'extended' WHERE status ='overdue' and customer_id = {order_id}"
    cursor.execute(update_query)
    conn.commit()
    conn.close()

#overdue
def update_overdue_status():
    conn = connection_database.db()
    cursor = conn.cursor()

    # Get current date
    current_date = datetime.now().date()

    # Update status to "overdue" for orders where delivery date is in the past
    update_query = f"UPDATE customer_data SET status = 'overdue' WHERE delivery_date < '{current_date}'"
    
    cursor.execute(update_query)
    conn.commit()
    conn.close()


# Delivered

def update_delivered_status():
    conn = connection_database.db()
    cursor = conn.cursor()

    update_query = f"UPDATE customer_data SET status = 'delivered'"
    cursor.execute(update_query)
    conn.commit()
    conn.close()


# Cancelled

def update_cancelled_status():
    conn = connection_database.db()
    cursor = conn.cursor()

    update_query = f"UPDATE customer_data SET status = 'cancelled'"
    cursor.execute(update_query)
    conn.commit()
    conn.close()










