import connection_database
import os
import save_customer_and_files_data, save_and_view_blouse_data


def save_maggam_data(submitted_details, Stiching):
    customer_id = save_customer_and_files_data.save_customer_data(submitted_details)
    #Insert into maggam_data table
    conn = connection_database.db()
    cursor = conn.cursor()
    
    if Stiching == "Yes":
        category = "Blouse-Stiching"
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
                    submitted_details["BlouseStyle"],", ".join(submitted_details["ClosingWith"]),
                    submitted_details["Padding"], submitted_details["Piping"],
                    submitted_details["Lace"], submitted_details["Tassels"],
                    submitted_details["Comments"])
        cursor.execute(blouse_query, blouse_data)
        conn.commit()
        cursor.execute("Select LAST_INSERT_ID()")
        blouse_id = cursor.fetchone()[0]
        maggam_blouse_stich = """
                        INSERT INTO maggam_data (customer_id, blouse_id,maggam_description, comments)
                        VALUES (%s, %s, %s, %s)"""
        maggam_blouse_data = (customer_id, blouse_id, category,
                        submitted_details["Comments"])
        
        cursor.execute(maggam_blouse_stich, maggam_blouse_data)
    else:
        category = "No-Stiching"
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
                    submitted_details["BlouseStyle"], submitted_details["ClosingWith"],
                    submitted_details["Padding"], submitted_details["Piping"],
                    submitted_details["Lace"], submitted_details["Tassels"],
                    submitted_details["Comments"])
        cursor.execute(blouse_query, blouse_data)
        conn.commit()
        cursor.execute("Select LAST_INSERT_ID()")
        blouse_id = cursor.fetchone()[0]
        maggam_no_stich = """INSERT INTO maggam_data (customer_id, maggam_description, comments) VALUES(%s,%s, %s)"""
        
        maggam_no_data = (customer_id, category, submitted_details["Comments"])
        cursor.execute(maggam_no_stich, maggam_no_data)
        
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    maggam_id = cursor.fetchone()[0]

    # Insert files into maggam_files table
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
            composite_file_name = f"{customer_id}-{maggam_id}-{category}-{file_name}"
            # Perform the database insertion
            file_query = """INSERT INTO maggam_files (maggam_id, file_data, file_name)
                            VALUES (%s, %s, %s)"""
            file_data_tuple = (maggam_id, file_data, composite_file_name)
            cursor.execute(file_query, file_data_tuple)
    conn.commit()
    conn.close()
    pdf_file_name = f"{customer_id}-{maggam_id}-{category}"
    return pdf_file_name, customer_id


def view_all_maggam_data():
    conn = connection_database.db()
    cursor = conn.cursor()

    query = """SELECT cd.customer_id, cd.name, cd.phone, cd.email, cd.dates, cd.delivery_date, cd.category, cd.registration_date,
                      bd.blouse_full_length, bd.shoulder, bd.hand_length, bd.hand_rounding, bd.arm_hole,
                      bd.upper_chest, bd.chest, bd.waist, bd.front_neck_deep, bd.back_neck_deep,
                      bd.boat_neck, bd.collar,
                      bd.preferred_neck_style, bd.preferred_blouse_style, bd.closingwith,
                      bd.padding, bd.piping, bd.lace, bd.tassels, md.comments, mf.file_name
               FROM customer_data cd
               JOIN maggam_data md ON md.customer_id = cd.customer_id
               LEFT JOIN maggam_files mf ON md.maggam_id = mf.maggam_id
               LEFT JOIN blouse_data bd ON md.customer_id = bd.customer_id
               """
    
    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data

