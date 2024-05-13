import connection_database
import os
import save_customer_and_files_data
def save_boys_data(submitted_details):
    customer_id = save_customer_and_files_data.save_customer_data(submitted_details)
   # Insert into blouse_data table
    category = "Boys"
    conn = connection_database.db()
    cursor = conn.cursor()
    boys_query = """INSERT INTO boys_data (customer_id, full_length, hand_length, collar,
                    shoulder, side_cuts, pant_length, thigh_rounding, 
                    leg_rounding, pant_style, comments)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    boys_data = (customer_id, submitted_details["FullLength"], submitted_details["HandLength"],
                 submitted_details["Collar"],submitted_details["Shoulder"],
                   submitted_details["SideCuts"],
                   submitted_details["PantLength"], submitted_details["ThighRounding"],
                   submitted_details["LegRounding"], submitted_details["PantStyle"], 
                   submitted_details["Comments"])
    cursor.execute(boys_query, boys_data)
    conn.commit()
    cursor.execute("Select LAST_INSERT_ID()")
    boys_id = cursor.fetchone()[0]

    # Insert files into blouse_files table
    if submitted_details["Files"]:
        for uploaded_file in submitted_details["Files"]:
            # Save the uploaded file to a temporary location
            with open(uploaded_file.name, 'wb') as f:
                f.write(uploaded_file.getbuffer())

            # Open the saved file for reading
            with open(uploaded_file.name, 'rb') as f:
                file_data = f.read()

            # Get the filename using os.path.basename()
            file_name = os.path.basename(uploaded_file.name)
            # Construct the composite file name
            composite_file_name = f"{customer_id}-{boys_id}-{category}-{file_name}"
            # Perform the database insertion
            file_query = """INSERT INTO boys_files (boys_id, file_data, file_name)
                            VALUES (%s, %s, %s)"""
            file_data_tuple = (boys_id, file_data, composite_file_name)
            cursor.execute(file_query, file_data_tuple)
    conn.commit()
    conn.close()

    pdf_file_name = f"{customer_id}-{boys_id}-{category}"
    return pdf_file_name, customer_id

    


def view_all_boys_data():
    conn = connection_database.db()
    cursor = conn.cursor()

    
    query = """SELECT cd.customer_id, cd.name, cd.phone, cd.email, cd.dates, cd.delivery_date,cd.category, cd.registration_date,
                      bd.full_length,bd.hand_length, bd.collar, bd.shoulder,bd.side_cuts, bd.pant_length,
                       bd.thigh_rounding, bd.leg_rounding, bd.pant_style ,
                     bd.comments,bf.file_name
               FROM customer_data cd
               JOIN boys_data bd ON cd.customer_id = bd.customer_id
               LEFT JOIN boys_files bf ON bd.boys_id = bf.boys_id"""
    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data

