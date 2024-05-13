import streamlit as st
import pandas as pd
import save_customer_and_files_data
import connection_database
import save_and_view_blouse_data, save_and_view_boys_data
from datetime import datetime, timedelta
import save_and_view_blouse_lehenga_data
import save_and_view_maggam_data
import save_and_view_topbottom_data
import pdf
columns_to_convert = ['Order Date', 'Delivery Date', 'Submission Date']

def blouse_dataframe(blouse_data):
    
    df_blouse = pd.DataFrame(blouse_data, columns=["Customer ID", "Name", "Phone", "Email", "Order Date", "Delivery Date","Garment Type", "Submission Date",
                                            "Blouse Full Length", "Shoulder", "Hand Length", "Hand Rounding",
                                            "Arm Hole", "Upper Chest", "Chest", "Waist", "Front Neck Deep",
                                            "Back Neck Deep", "Boat Neck","Collar","Preferred Neck Style", "Preferred Blouse Style",
                                            "Closing With", "Padding", "Piping", "Lace", "Tassels", "Comments","File Name"])

    df_blouse[columns_to_convert] = df_blouse[columns_to_convert].apply(lambda x: pd.to_datetime(x).dt.strftime('%d-%m-%Y'))      
    st.dataframe(df_blouse, use_container_width=True)

def topbottom_dataframe(topbottom_data):
    df_topbottom = pd.DataFrame(topbottom_data, columns=["Customer ID", "Name", "Phone", "Email", "Order Date", "Delivery Date","Garment Type", "Submission Date",
                                            "Top Full Length", "Shoulder", "Hand Length", "Hand Rounding",
                                            "Arm Hole", "Upper Chest", "Chest", "Top Waist", "Front Neck Deep",
                                            "Back Neck Deep", "Boat Neck","Collar","Side Cuts","Hip","Bottom Full Length",
                                            "Leg Rounding","Thigh Rounding","Bottom Waist","Bottom Style",
                                             "Comments","File Name"])
    
    df_topbottom[columns_to_convert] = df_topbottom[columns_to_convert].apply(lambda x: pd.to_datetime(x).dt.strftime('%d-%m-%Y'))          
    st.dataframe(df_topbottom, use_container_width=True)

def boys_dataframe(boys_data):
    df_boys = pd.DataFrame(boys_data, columns=["Customer ID", "Name", "Phone", "Email", "Order Date", "Delivery Date","Garment Type", "Submission Date",
                                            "Full Length", "Hand Length", "Collar","Shoulder","Side Cuts","Pant Length",
                                            "Thigh Rounding", "Leg Rounding", "Pant Style",
                                             "Comments","File Name"])
    df_boys[columns_to_convert] = df_boys[columns_to_convert].apply(lambda x: pd.to_datetime(x).dt.strftime('%d-%m-%Y'))          
    st.dataframe(df_boys, use_container_width=True)

def blouse_lehenga_dataframe(blouse_lehenga_data):
    df_blouse_lehenga = pd.DataFrame(blouse_lehenga_data, columns=["Customer ID", "Name", "Phone", "Email", "Order Date", "Delivery Date","Garment Type", "Submission Date",
                                            "Blouse Full Length", "Shoulder", "Hand Length", "Hand Rounding",
                                            "Arm Hole", "Upper Chest", "Chest", "Waist", "Front Neck Deep",
                                            "Back Neck Deep", "Boat Neck","Collar","Preferred Neck Style", "Preferred Blouse Style",
                                            "Closing With", "Padding", "Piping", "Lace", "Tassels","Lehenga Full Length", "Waist Rounding",
                                            "Hip Around","Frock Full Length","Comments","File Name"])
    df_blouse_lehenga[columns_to_convert] = df_blouse_lehenga[columns_to_convert].apply(lambda x: pd.to_datetime(x).dt.strftime('%d-%m-%Y'))          
    st.dataframe(df_blouse_lehenga, use_container_width=True)

def maggam_dataframe(maggam_data):
    df_maggam = pd.DataFrame(maggam_data, columns=["Customer ID", "Name", "Phone", "Email", "Order Date", "Delivery Date","Garment Type", "Submission Date",
                                            "Blouse Full Length", "Shoulder", "Hand Length", "Hand Rounding",
                                            "Arm Hole", "Upper Chest", "Chest", "Waist", "Front Neck Deep",
                                            "Back Neck Deep", "Boat Neck","Collar","Preferred Neck Style", "Preferred Blouse Style",
                                            "Closing With", "Padding", "Piping", "Lace", "Tassels", "Comments","File Name"])
    
    df_maggam[columns_to_convert] = df_maggam[columns_to_convert].apply(lambda x: pd.to_datetime(x).dt.strftime('%d-%m-%Y'))  
    st.dataframe(df_maggam, use_container_width=True)

def cus_dataframe(cus_data):
    df_cus = pd.DataFrame(cus_data, columns=["Customer ID", "Name", "Phone", "Email", "Order Date", "Delivery Date","Garment Type","Status", "Submission Date"])
    # Convert 'Delivery Date' column to datetime if not already
    df_cus[columns_to_convert] = df_cus[columns_to_convert].apply(lambda x: pd.to_datetime(x).dt.strftime('%d-%m-%Y'))  
    st.dataframe(df_cus, use_container_width=True)
    return df_cus

#########################################


# Inject custom CSS into Streamlit app

def customer_info():

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Customer Info 🔍","Blouses","Boys", "Top/Bottom", "Blouse/Lehenga/Girls", "Maggam Handwork" ,"All Data"])
    conn = connection_database.db()
    cursor = conn.cursor()
    


    with tab1:
        cus_data = save_customer_and_files_data.view_cus_data()
        cus_dataframe(cus_data)

        col1, col2, col3, col4 = st.columns(4)

        #Name
        with col1:
            cursor.execute("SELECT DISTINCT name FROM customer_data")
            names = [row[0] for row in cursor.fetchall()]

            with st.popover("🔍 Names"):
                single = st.text_input("Enter a data", value=None, placeholder="🔍 Names")
                selected_names = []
                for name in names:
                    selected = st.checkbox(name)
                    if selected:
                        selected_names.append(name)

            for name in selected_names:
                st.write(name)

            if single is not None:
                if single !="":
                    selected_names.append(single)
        
        if selected_names:
                # Constructing the SQL query with selected names
                selected_names_str = ",".join([f"'{name}'" for name in selected_names])
                query = f"""SELECT cd.customer_id, cd.name, cd.phone, cd.email , cd.dates ,
                         cd.delivery_date,  cd.category ,cd.status, cd.registration_date
                            FROM customer_data cd
                            LEFT JOIN blouse_data bd ON cd.customer_id = bd.customer_id
                            LEFT JOIN topbottom_data kd ON cd.customer_id = kd.customer_id
                            WHERE cd.name IN ({selected_names_str})"""

                cursor.execute(query)
                filtered_data = cursor.fetchall()
                st.subheader("Name", divider="grey")
                cus_dataframe(filtered_data)
                

        #Phone
        with col2:
            cursor.execute("Select distinct phone from customer_data")
            phone_numbers = [row[0]for row in cursor.fetchall()]
            with st.popover("🔍 Mobile"):
                single = st.text_input("Enter a data", value = None, placeholder="🔍 Mobile")
                selected_phones = []
                for phone_number in phone_numbers:
                    selected =st.checkbox(phone_number, key = phone_number)
                    if selected:
                        selected_phones.append(phone_number)

            for phone_number in selected_phones:
                st.write(phone_number)  
            
            if single is not None:
                if single !="":
                    selected_phones.append(single)


        if selected_phones:
                # Constructing the SQL query with selected names
                selected_phones_str = ",".join([f"'{phone}'" for phone in selected_phones])
                query = f"""SELECT cd.customer_id, cd.name, cd.phone, cd.email , cd.dates ,
                         cd.delivery_date,  cd.category,cd.status, cd.registration_date 
                            FROM customer_data cd
                            LEFT JOIN blouse_data bd ON cd.customer_id = bd.customer_id
                            LEFT JOIN topbottom_data kd ON cd.customer_id = kd.customer_id
                            WHERE cd.phone IN ({selected_phones_str})"""

                cursor.execute(query)
                filtered_data = cursor.fetchall()
                st.subheader("Phone", divider="grey")
                cus_dataframe(filtered_data)

        #Garment
        with col3:
            cursor.execute("Select distinct category from customer_data")
            categories = [row[0]for row in cursor.fetchall()]
            with st.popover("🔍 Garments"):
                single = st.text_input("Enter a data", value= None, placeholder="🔍 Garments")
                selected_category = []
                for category in categories:
                    selected = st.checkbox(category)
                    if selected:
                        selected_category.append(category)

            for category in selected_category:
                st.write(category)

            if single is not None:
                if single !="":
                    selected_category.append(single)
        if selected_category:
                # Constructing the SQL query with selected names
                selected_category_str = ",".join([f"'{category}'" for category in selected_category])
                query = f"""SELECT cd.customer_id, cd.name, cd.phone, cd.email , cd.dates ,
                         cd.delivery_date, cd.category , cd.status,cd.registration_date
                            FROM customer_data cd
                            LEFT JOIN blouse_data bd ON cd.customer_id = bd.customer_id
                            LEFT JOIN topbottom_data kd ON cd.customer_id = kd.customer_id
                            WHERE cd.category IN ({selected_category_str})"""

                cursor.execute(query)
                filtered_data = cursor.fetchall()
                st.subheader("Garment", divider="grey")
                cus_dataframe(filtered_data)

        #Days "🔍 Days"
        with col4:
            cursor.execute("Select distinct registration_date from customer_data")
            days = [row[0]for row in cursor.fetchall()]
            with st.popover("🔍 Days"):
                single = st.text_input("Enter a data", value = None, placeholder="🔍 Days")         
                selected_days = []
                for recent in days:
                    recent_str = recent.strftime("%Y-%m-%d")  # Convert datetime to string
                    selected =st.checkbox(recent_str)
                    if selected:
                        selected_days.append(recent)

            for recent in selected_days:
                st.write(recent.strftime("%d-%m-%Y"))

            if single is not None:
                if single !="":
                    selected_days.append(single)

        if selected_days:
                # Constructing the SQL query with selected names
                selected_days_str = ",".join([f"'{recent}'" for recent in selected_days])
                query = f"""SELECT cd.customer_id, cd.name, cd.phone, cd.email , cd.dates ,
                         cd.delivery_date, cd.category , cd.status,cd.registration_date
                            FROM customer_data cd
                            LEFT JOIN blouse_data bd ON cd.customer_id = bd.customer_id
                            LEFT JOIN topbottom_data kd ON cd.customer_id = kd.customer_id
                            WHERE cd.registration_date IN ({selected_days_str})"""

                cursor.execute(query)
                filtered_data = cursor.fetchall()
                st.subheader("Days", divider="grey")
                cus_dataframe(filtered_data)
            


    with tab2:
        blouse_data = save_and_view_blouse_data.view_all_blouse_data()
        blouse_dataframe(blouse_data)


    with tab3:
        boys_data = save_and_view_boys_data.view_all_boys_data()
        boys_dataframe(boys_data)

    with tab4:
        topbottom_data = save_and_view_topbottom_data.view_all_topbottom_data()
        topbottom_dataframe(topbottom_data)

    with tab5:
        blouse_lehenga_data = save_and_view_blouse_lehenga_data.view_all_blouse_lehenga_data()
        blouse_lehenga_dataframe(blouse_lehenga_data)

    with tab6:
        maggam_data = save_and_view_maggam_data.view_all_maggam_data()
        maggam_dataframe(maggam_data)

    with tab7:
        st.write("Blouse")
        blouse_dataframe(blouse_data)

        st.write("Top/Bottom")
        topbottom_dataframe(topbottom_data)

        st.write("Boys")
        boys_dataframe(boys_data)

        st.write("Blouse/Lehenga/Girls")
        blouse_lehenga_dataframe(blouse_lehenga_data)

        st.write("Maggam Handwork")
        maggam_dataframe(maggam_data)

        
        
    


