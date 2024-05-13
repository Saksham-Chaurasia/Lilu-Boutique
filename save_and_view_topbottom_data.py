
import connection_database
import os
import save_customer_and_files_data
def save_topbottom_data(submitted_details):
    customer_id = save_customer_and_files_data.save_customer_data(submitted_details)
   # Insert into blouse_data table
    category = "Top/Bottom"
    conn = connection_database.db()
    cursor = conn.cursor()
    topbottom_query = """INSERT INTO topbottom_data (customer_id, top_full_length, shoulder, hand_length,
                     hand_rounding, arm_hole, upper_chest, chest, top_waist, front_neck_deep,
                     back_neck_deep, boat_neck, collar, side_cuts, hip, bottom_full_length,
                     leg_rounding, thigh_rounding, bottom_waist, bottom_style, comments)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    topbottom_data = (customer_id, submitted_details["TopFullLength"], submitted_details["Shoulder"],
                   submitted_details["HandLength"], submitted_details["HandRounding"],
                   submitted_details["ArmHole"], submitted_details["UpperChest"],
                   submitted_details["Chest"], submitted_details["TopWaist"], submitted_details["FrontNeck"],
                   submitted_details["BackNeck"], submitted_details["BoatNeck"],
                   submitted_details["Collar"],submitted_details["SideCuts"],
                   submitted_details["Hip"], 
                   submitted_details["BottomFullLength"], submitted_details["LegRounding"],
                   submitted_details["ThighRounding"], submitted_details["BottomWaist"],
                   submitted_details["BottomStyle"],
                   submitted_details["Comments"])
    cursor.execute(topbottom_query, topbottom_data)
    conn.commit()
    cursor.execute("Select LAST_INSERT_ID()")
    topbottom_id = cursor.fetchone()[0]

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
            composite_file_name = f"{customer_id}-{topbottom_id}-{category}-{file_name}"
            # Perform the database insertion
            file_query = """INSERT INTO topbottom_files (topbottom_id, file_data, file_name)
                            VALUES (%s, %s, %s)"""
            file_data_tuple = (topbottom_id, file_data, composite_file_name)
            cursor.execute(file_query, file_data_tuple)
    conn.commit()
    conn.close()
    pdf_file_name = f"{customer_id}-{topbottom_id}-{category}"
    return pdf_file_name, customer_id

def view_all_topbottom_data():
    conn = connection_database.db()
    cursor = conn.cursor()
    
    query = """SELECT cd.customer_id, cd.name, cd.phone, cd.email, cd.dates, cd.delivery_date,cd.category, cd.registration_date,
                      tb.top_full_length, tb.shoulder, tb.hand_length, tb.hand_rounding, tb.arm_hole,
                      tb.upper_chest, tb.chest, tb.top_waist, tb.front_neck_deep, tb.back_neck_deep,
                      tb.boat_neck, tb.collar, tb.side_cuts, tb.hip, tb.bottom_full_length,
                      tb.leg_rounding, tb.thigh_rounding, tb.bottom_waist, tb.bottom_style,
                     tb.comments,bf.file_name
               FROM customer_data cd
               JOIN topbottom_data tb ON cd.customer_id = tb.customer_id
               LEFT JOIN topbottom_files bf ON tb.topbottom_id = bf.topbottom_id"""

    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data

