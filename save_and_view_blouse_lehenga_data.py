
import connection_database
import os
import save_customer_and_files_data
def save_blouse_lehenga_data(submitted_details):
    customer_id = save_customer_and_files_data.save_customer_data(submitted_details)
    category = "Blouse/Lehenga/Girls"
   # Insert into blouse_data table
    conn = connection_database.db()
    cursor = conn.cursor()
    blouse_query = """INSERT INTO blouse_data (customer_id, blouse_full_length, shoulder, hand_length,
                     hand_rounding, arm_hole, upper_chest, chest, waist, front_neck_deep,
                     back_neck_deep, boat_neck, collar, preferred_neck_style, preferred_blouse_style, closingwith,
                     padding, piping, lace, tassels, comments)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"""
    blouse_data = (customer_id, submitted_details["BlouseFullLength"], submitted_details["Shoulder"],
                   submitted_details["HandLength"], submitted_details["HandRounding"],
                   submitted_details["ArmHole"], submitted_details["UpperChest"],
                   submitted_details["Chest"], submitted_details["Waist"], submitted_details["FrontNeck"],
                   submitted_details["BackNeck"], submitted_details["BoatNeck"],
                   submitted_details["Collar"],submitted_details["NeckStyle"],
                   submitted_details["BlouseStyle"], ", ".join(submitted_details["ClosingWith"]),
                   submitted_details["Padding"], submitted_details["Piping"],
                   submitted_details["Lace"], submitted_details["Tassels"],
                   submitted_details["Comments"])
    
    cursor.execute(blouse_query, blouse_data)
    conn.commit()
    cursor.execute("Select LAST_INSERT_ID()")
    blouse_id = cursor.fetchone()[0]
    
    # Insert lehenga into blehenga_data table
    lehenga_query = """INSERT INTO blehenga_data(customer_id,blouse_id, lehenga_full_length, waist_rounding,
                       hip_around, frock_full_length) VALUES (%s, %s,%s, %s, %s, %s)"""
    
    lehenga_data = (customer_id, blouse_id, submitted_details["LehengaFullLength"], submitted_details["WaistRounding"],
                    submitted_details["HipAround"], submitted_details["FrockFullLength"])
    
    cursor.execute(lehenga_query, lehenga_data)
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    blehenga_id = cursor.fetchone()[0]

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
            composite_file_name = f"{customer_id}-{blehenga_id}-{category}-{file_name}"
            

            # Perform the database insertion
            file_query = """INSERT INTO blouse_files (blouse_id, file_data, file_name)
                            VALUES (%s, %s, %s)"""
            file_data_tuple = (blouse_id, file_data, composite_file_name)
            cursor.execute(file_query, file_data_tuple)
    conn.commit()
    conn.close()
    pdf_file_name = f"{customer_id}-{blouse_id}-{category}"
    return pdf_file_name, customer_id

def view_all_blouse_lehenga_data():
    conn = connection_database.db()
    cursor = conn.cursor()

    
    query = """SELECT cd.customer_id, cd.name, cd.phone, cd.email, cd.dates, cd.delivery_date,cd.category, cd.registration_date,
                      bd.blouse_full_length, bd.shoulder, bd.hand_length, bd.hand_rounding, bd.arm_hole,
                      bd.upper_chest, bd.chest, bd.waist, bd.front_neck_deep, bd.back_neck_deep,
                      bd.boat_neck, bd.collar,
                      bd.preferred_neck_style, bd.preferred_blouse_style, bd.closingwith,
                      bd.padding, bd.piping, bd.lace, bd.tassels, bl.lehenga_full_length,
                      bl.waist_rounding, bl.hip_around, bl.frock_full_length,bd.comments,bf.file_name
               FROM customer_data cd
               JOIN blehenga_data bl ON bl.customer_id = cd.customer_id
               LEFT JOIN blouse_data bd ON bl.customer_id = bd.customer_id
               LEFT JOIN blouse_files bf ON bd.blouse_id = bf.blouse_id"""

    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data

