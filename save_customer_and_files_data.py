import connection_database
import os
def save_customer_data(submitted_details):
    conn = connection_database.db()
    cursor = conn.cursor()

    # Insert into customer_data table
    customer_query = """INSERT INTO customer_data (dates, name, phone, email, delivery_date, category)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
    customer_data = (submitted_details["Date"], submitted_details["Name"],
                     submitted_details["MobileNumber"], submitted_details["Email"],
                     submitted_details["DeliveryDate"], submitted_details["Category"])
    
    cursor.execute(customer_query, customer_data)
    conn.commit()
    cursor.execute("Select LAST_INSERT_ID()")
    customer_id = cursor.fetchone()[0]

    return customer_id

# particular filters on customer for viewing only
def view_cus_data():
    conn = connection_database.db()
    cursor = conn.cursor()

    query = """SELECT cd.customer_id, cd.name, cd.phone, cd.email, cd.dates, cd.delivery_date, cd.category,cd.status, cd.registration_date
                FROM customer_data cd
               ;"""
    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data