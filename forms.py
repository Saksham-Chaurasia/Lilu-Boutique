import streamlit as st
import pandas as pd
import save_and_view_blouse_data
import connection_database
import mysql.connector
import save_and_view_maggam_data
import save_and_view_topbottom_data
import save_and_view_boys_data
import save_and_view_blouse_lehenga_data
import re
import pdf 

def common_viewing(submitted_details):
    df = pd.DataFrame([submitted_details])
    # Extract file names from UploadedFile objects
    df["Files"] = df["Files"].apply(lambda files: ", ".join([file.name for file in files]) if files else "")
    if "ClosingWith" in df.columns:
        df["ClosingWith"] = df["ClosingWith"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
        
    df_transposed = df.T.reset_index()

    # Rename the columns of the transposed DataFrame
    df_transposed.columns = ['Fields', 'Values']

    # converting the date into dd/mm/yyyy format
    date_indices = df_transposed['Fields'].isin(['Date', 'DeliveryDate'])
    df_transposed.loc[date_indices, 'Values'] = pd.to_datetime(df_transposed.loc[date_indices, 'Values']).dt.strftime('%d-%m-%Y')
    st.dataframe(df_transposed, use_container_width=True)
    return df_transposed

def font_size_controller():
    st.markdown("""<style>div[class*="stText"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 20px;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>div[class*="stNumber"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 20px;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>div[class*="stDate"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 20px;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 20px;}</style>""", unsafe_allow_html=True)

# Function to validate mobile number format
def validate_mobile_number(mobile_number):
    # Regular expression to match either 10 digit number or +91-xxxxxxxxxx format
    pattern = r'^(?:\+91 |0)?\d{10}$'
    if re.match(pattern, mobile_number):
        return True
    else:
        return False

# Function to validate email format
def validate_email(email):
    if "@" in email and "." in email:
        return True
    else:
        return False

# Customer Details
def customer_details():
    conn = connection_database.db()
    st.title("Measurements Form :pencil:")  
    st.subheader("",divider="grey")   
    # font_size_controller()
    # Fields for customer details
    Date = st.date_input("Date :date:", value=None,format="DD/MM/YYYY")
    Name = st.text_input("Name:red[*]", key = "name", placeholder="Sita Devi")
    Mobile_Number = st.text_input("Mobile Number:red[**]", key = "mobile", placeholder="XXX-XXXX-XXXX")
    
    # Validating mobile number format
    # if Mobile_Number != '':
    #     st.error("Invalid mobile number! Please enter a 10 digit number or in the format +91-xxxxxxxxxx.")
    
    # Checking in the database that mobile number exists already or not
    if Mobile_Number != '':
        conn.row_factory = mysql.connector.cursor.MySQLCursorDict
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customer_data WHERE phone=%s', (Mobile_Number,))
        row = cursor.fetchone()
        if row:
            st.warning("This Mobile Number already exists")
    
    # Validate email format
    Email = st.text_input("Email:", key="email",placeholder="example@example.com")  
    if Email and not validate_email(Email):
        st.error("Invalid email address! Please enter a valid email address.")  
    delivery_date = st.date_input("Delivery Date :calendar:", value=None,format="DD/MM/YYYY")
    
    return Date, Name, Mobile_Number, Email, delivery_date



# Blouse Styles
def blouse_styles():

    # Preferred Neck Styles
    neck_styles =["Round-Neck","V-Neck","Wide Square Neck","Basket Neck",
                  "Boat Neck","Sweet-Heart Neck","Others"]
    st.subheader("Neck Style")
    with st.expander("Select your option", True):
        selected_neck_style = st.radio("Neck Style",neck_styles, index=None,horizontal=True, label_visibility="collapsed")

    if selected_neck_style == "Others":
        selected_neck_style = st.text_input("Enter Custom Neck Style")
    else:
        selected_neck_style = None

    st.subheader('',divider="grey")
    blouse_styles = ["Front Hook Blouse","Back Hook Blouse"]

    st.subheader("Blouse Style")
    with st.expander("Select your option", True):
        selected_blouse_style = st.radio("Blouse Style",blouse_styles,index=None,horizontal=True, label_visibility="collapsed")
    
    # needed to work that when i don't want to select anyone how can i handle that
    return selected_neck_style, selected_blouse_style



def blouse_selections():
    font_size_controller()
    # Multiselect for closing with blouse
    st.write("Blouse-Features: Hook, Zip , Potali Button, Simple Button, Dori")
    option = ["None","Hook","Zip","Potali button","Simple Button","Dori"]
    closing_with = st.multiselect("", option, label_visibility="collapsed")
    st.subheader('',divider="grey")

    # Custom CSS for larger font size
    st.markdown("""<style>div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {font-size: 20px;}</style>""", unsafe_allow_html=True)

    # Yes/No options
    yes_no = ["Yes","No"]
    
    with st.container(border=True):
    # Use a column layout
        col1, col2 = st.columns(2)
        
            # First column
        with col1:
            # Padding
            padding = st.radio("Padding", yes_no, index=None, key="padding", horizontal=True)

            # Piping
            piping = st.radio("Piping", yes_no, index=None, key="piping", horizontal=True)

        # Second column
        with col2:
            # Lace
            
            lace = st.radio("Lace", yes_no, index=None, key="lace", horizontal=True)

            # Tassels
            tassels = st.radio("Tassels", yes_no, index=None, key="tassels", horizontal=True)

    st.subheader("",divider="grey")
    return closing_with, padding, piping, lace, tassels



# BLOUSE Form-------------------------------------
def blouse_form():

    with st.form("blouse", clear_on_submit=True):
        Date, Name, Mobile_Number, Email, delivery_date = customer_details()
        category = 'Blouse'

        st.header('Blouse Measures (in Inches) :straight_ruler:', divider='grey')
        Blouse_Full_Length = st.number_input("Full Length", min_value=0.00, value = None, placeholder="0.00")
        Shoulder = st.number_input("Shoulder",min_value=0.00, value = None, placeholder="0.00")
        Hand_Length = st.number_input("Hand Length",min_value=0.00, value = None, placeholder="0.00")
        Hand_Rounding = st.number_input("Hand Rounding",min_value=0.00, value = None, placeholder="0.00")
        Arm_Hole = st.number_input("Arm Hole",min_value=0.00, value = None, placeholder="0.00")
        Upper_Chest = st.number_input("Upper Chest",min_value=0.00, value = None, placeholder="0.00")
        Chest = st.number_input("Chest",min_value=0.00, value = None, placeholder="0.00")
        Waist = st.number_input("Waist",min_value=0.00, value = None, placeholder="0.00")
        Front_Neck = st.number_input("Front Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")
        Back_Neck = st.number_input("Back Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")

        #new one's
        Boat_Neck = st.number_input("Boat Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")
        Collar = st.number_input("Collar", min_value=0.00, value = None, placeholder="0.00")

        st.subheader('',divider="grey")
        with st.container(border=True):
            selected_neck_style, selected_blouse_style = blouse_styles()
        st.subheader("",divider="grey")
        closing_with, padding, piping, lace, tassels = blouse_selections()
        

        uploaded_files = st.file_uploader("Upload Reference pic", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        comments = st.text_area("Please list any comments or special requirements Below")
        
        if st.form_submit_button("Submit"):
            submitted_details = {
                "Date": Date,
                "Name": Name,
                "MobileNumber": Mobile_Number,
                "Email": Email,
                "DeliveryDate":delivery_date,
                "Category":category,
                "BlouseFullLength":Blouse_Full_Length,
                "Shoulder":Shoulder,
                "HandLength":Hand_Length,
                "HandRounding":Hand_Rounding,
                "ArmHole":Arm_Hole,
                "UpperChest":Upper_Chest,
                "Chest":Chest,
                "Waist":Waist,
                "FrontNeck":Front_Neck,
                "BackNeck":Back_Neck,
                "BoatNeck":Boat_Neck,
                "Collar":Collar,
                "NeckStyle":selected_neck_style,
                "BlouseStyle":selected_blouse_style,
                "ClosingWith":closing_with,
                "Padding":padding,
                "Piping":piping,
                "Lace":lace,
                "Tassels":tassels,
                "Files":uploaded_files,
                "Comments":comments
            }
            if not Name:
                st.write("Error: Name field is required.")
                return
            
            df_transposed=common_viewing(submitted_details)
            blouse_id,file_name,customer_id = save_and_view_blouse_data.save_blouse_data(submitted_details)
            st.success("Data submitted successfully!")

            # pdf generation
            
            pdf_filename = pdf.generate_pdf(df_transposed,file_name,customer_id)
            pdf.display_pdf(pdf_filename)

            
            print("saved") 
        

# Top/Bottom Form-------------------------------------
# Bottom Styles
def bottom_styles():
    bottom_styles =["Salwar","Straight Cut","Pencil Cut",
                    "Patiala","Chudi Pant","Others"]
    
    selected_bottom_style = st.radio("Bottom Style:",bottom_styles, index=None,horizontal=True)

    if selected_bottom_style == "Others":
        selected_bottom_style = st.text_input("Enter Custom Bottom Style")
    else:
        selected_bottom_style = None

    st.subheader('',divider="grey")
    
    # needed to work that when i don't want to select anyone how can i handle that
    return selected_bottom_style

def top_bottom_form():
    # with st.form("top_bottom_form",clear_on_submit=True):
        Date, Name, Mobile_Number, Email, delivery_date = customer_details()
        category = 'Top/Bottom'
        st.header('Top/Bottom Measures (in Inches) :straight_ruler:', divider='grey')
        font_size_controller()

        #Top
        with st.container(border=True):
            st.subheader("Top Measures (in inches)", divider="grey")
            Top_Full_Length = st.number_input("Top Full Length",min_value=0.00, value = None, placeholder="0.00")
            Shoulder = st.number_input("Shoulder",min_value=0.00, value = None, placeholder="0.00")
            Hand_Length = st.number_input("Hand Length",min_value=0.00, value = None, placeholder="0.00")
            Hand_Rounding = st.number_input("Hand Rounding",min_value=0.00, value = None, placeholder="0.00")
            Arm_Hole = st.number_input("Arm Hole",min_value=0.00, value = None, placeholder="0.00")
            Upper_Chest = st.number_input("Upper Chest",min_value=0.00, value = None, placeholder="0.00")
            Chest = st.number_input("Chest",min_value=0.00, value = None, placeholder="0.00")
            Top_Waist = st.number_input("Waist",min_value=0.00, value = None, placeholder="0.00" ,key = "top_waist")
            Front_Neck = st.number_input("Front Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")
            Back_Neck = st.number_input("Back Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")

            #new one's
            Boat_Neck = st.number_input("Boat Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")
            Collar = st.number_input("Collar", min_value=0.00, value = None, placeholder="0.00")
            Side_Cuts = st.number_input("Side Cuts", min_value=0.00, value = None, placeholder="0.00")
            Hip = st.number_input("Hip", min_value=0.00, value = None, placeholder="0.00")
        st.header('',divider="grey")
        #Bottom
        with st.container(border=True):
            st.subheader('Bottom Measures (in inches)',divider="grey")
            Bottom_Full_Length = st.number_input("Bottom Full Length",min_value=0.00, value = None, placeholder="0.00")
            Leg_Rounding = st.number_input("Leg Rounding", min_value=0.00, value = None, placeholder="0.00")
            Thigh_Rounding = st.number_input("Thigh Rounding", min_value=0.00, value = None, placeholder="0.00")
            Bottom_Waist = st.number_input("Waist", min_value=0.00, key="bottom_waist", value = None, placeholder="0.00")
            with st.container(border=True):
                selected_bottom_styles = bottom_styles()
        
        uploaded_files = st.file_uploader("Upload Reference pic", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        comments = st.text_area("Please list any comments or special requirements Below")
        
        if st.button("Submit"):
            submitted_details = {
                "Date": Date,
                "Name": Name,
                "MobileNumber": Mobile_Number,
                "Email": Email,
                "DeliveryDate":delivery_date,
                "Category":category,
                "TopFullLength":Top_Full_Length,
                "Shoulder":Shoulder,
                "HandLength":Hand_Length,
                "HandRounding":Hand_Rounding,
                "ArmHole":Arm_Hole,
                "UpperChest":Upper_Chest,
                "Chest":Chest,
                "TopWaist":Top_Waist,
                "FrontNeck":Front_Neck,
                "BackNeck":Back_Neck,
                "BoatNeck":Boat_Neck,
                "Collar":Collar,
                "SideCuts":Side_Cuts,
                "Hip":Hip,
                "BottomFullLength":Bottom_Full_Length,
                "LegRounding":Leg_Rounding,
                "ThighRounding":Thigh_Rounding,
                "BottomWaist":Bottom_Waist,
                "BottomStyle":selected_bottom_styles,
                "Files":uploaded_files,
                "Comments":comments
            }
            if not Name:
                st.write("Error: Name field is required.")
                return
            
            df_transposed=common_viewing(submitted_details)
        
            file_name,customer_id = save_and_view_topbottom_data.save_topbottom_data(submitted_details)
            st.success("Data submitted successfully!")
            
            file_name = file_name.replace("/","-")
            pdf_filename = pdf.generate_pdf(df_transposed,file_name,customer_id)
            pdf.display_pdf(pdf_filename)

            
            print("saved")  

def blouse_lehenga_girls_form():
    with st.form("blouse_lehenga_girls_form",clear_on_submit=True):
        Date, Name, Mobile_Number, Email, delivery_date = customer_details()
        category = 'Blouse/Lehenga/Girls'
        font_size_controller()
        st.header('Blouse/Lehenga Measures (in Inches) :straight_ruler:', divider='grey')
        Blouse_Full_Length = st.number_input("Blouse Full Length",min_value=0.00, value = None, placeholder="0.00")
        Shoulder = st.number_input("Shoulder",min_value=0.00, value = None, placeholder="0.00")
        Hand_Length = st.number_input("Hand Length",min_value=0.00, value = None, placeholder="0.00")
        Hand_Rounding = st.number_input("Hand Rounding",min_value=0.00, value = None, placeholder="0.00")
        Arm_Hole = st.number_input("Arm Hole",min_value=0.00, value = None, placeholder="0.00")
        Upper_Chest = st.number_input("Upper Chest",min_value=0.00, value = None, placeholder="0.00")
        Chest = st.number_input("Chest",min_value=0.00, value = None, placeholder="0.00")
        Waist = st.number_input("Waist",min_value=0.00, value = None, placeholder="0.00")
        Front_Neck = st.number_input("Front Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")
        Back_Neck = st.number_input("Back Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")

        #new one's
        Boat_Neck = st.number_input("Boat Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")
        Collar = st.number_input("Collar", min_value=0.00, value = None, placeholder="0.00")

        st.subheader('',divider="grey")
        with st.container(border=True):
            selected_neck_style, selected_blouse_style = blouse_styles()
        st.subheader("",divider="grey")
        closing_with, padding, piping, lace, tassels = blouse_selections()
        
        #Lehenga
        st.subheader('Lehenga Measures (in inches)',divider='grey')
        Lehenga_Full_Length = st.number_input("Lehenga Full Length", min_value=0.00, value = None, placeholder="0.00")
        Waist_Rounding = st.number_input("Waist Rounding", min_value=0.00, value = None, placeholder="0.00")
        Hip_Around = st.number_input("Hip Around", min_value=0.00, value = None, placeholder="0.00")

        #Frock
        st.subheader("Frock Measure (in inches)", divider="grey")
        Frock_Full_Length = st.number_input("Frock Full Length", min_value=0.00, value = None, placeholder="0.00")

        uploaded_files = st.file_uploader("Upload Reference pic", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        comments = st.text_area("Please list any comments or special requirements Below")
        
        if st.form_submit_button("Submit"):
            submitted_details = {
                "Date": Date,
                "Name": Name,
                "MobileNumber": Mobile_Number,
                "Email": Email,
                "DeliveryDate":delivery_date,
                "Category":category,
                "BlouseFullLength":Blouse_Full_Length,
                "Shoulder":Shoulder,
                "HandLength":Hand_Length,
                "HandRounding":Hand_Rounding,
                "ArmHole":Arm_Hole,
                "UpperChest":Upper_Chest,
                "Chest":Chest,
                "Waist":Waist,
                "FrontNeck":Front_Neck,
                "BackNeck":Back_Neck,
                "BoatNeck":Boat_Neck,
                "Collar":Collar,
                "NeckStyle":selected_neck_style,
                "BlouseStyle":selected_blouse_style,
                "ClosingWith":closing_with,
                "Padding":padding,
                "Piping":piping,
                "Lace":lace,
                "Tassels":tassels,
                "LehengaFullLength":Lehenga_Full_Length,
                "WaistRounding":Waist_Rounding,
                "HipAround":Hip_Around,
                "FrockFullLength":Frock_Full_Length,
                "Files":uploaded_files,
                "Comments":comments
            }
            if not Name:
                st.write("Error: Name field is required.")
                return
            
            df_transposed=common_viewing(submitted_details)
        
            file_name,customer_id =save_and_view_blouse_lehenga_data.save_blouse_lehenga_data(submitted_details)
            st.success("Data submitted successfully!")
            # pdf generation
            
            pdf_filename = pdf.generate_pdf(df_transposed,file_name,customer_id)
            pdf.display_pdf(pdf_filename)

            
            print("saved")  
def pant_styles():
    pant_styles =["Chudi","Patiala","Pyjama","Others"]
    
    selected_pant_style = st.radio("Pant Style:",pant_styles, index=None,horizontal=True)

    if selected_pant_style == "Others":
        selected_pant_style = st.text_input("Enter Custom Bottom Style")
    else:
        selected_pant_style = None

    st.subheader('',divider="grey")
    
    # needed to work that when i don't want to select anyone how can i handle that
    return selected_pant_style

def boys_form():
    with st.form("boys_form", clear_on_submit=True):
        category = 'Boys'
        st.header('Boys-Kurta Measurements (in Inches) :straight_ruler:', divider='grey')
        Date, Name, Mobile_Number, Email, delivery_date = customer_details()
        st.subheader('Boys-Kurta Measures (in Inches) :straight_ruler:', divider='grey')
        font_size_controller()
        Full_Length = st.number_input("Full Length", min_value=0.00, value = None, placeholder="0.00")
        Hand_Length = st.number_input("Hand Length", min_value=0.00, value = None, placeholder="0.00")
        Collar = st.number_input("Collar", min_value=0.00, value = None, placeholder="0.00")
        Shoulder = st.number_input("Shoulder", min_value=0.00, value = None, placeholder="0.00")
        Side_Cuts = st.number_input("Side Cuts", min_value=0.00, value = None, placeholder="0.00")
        Pant_Length = st.number_input("Pant Length",min_value=0.00, value = None, placeholder="0.00")
        Thigh_Rounding = st.number_input("Thigh Rounding", min_value=0.00, value = None, placeholder="0.00")
        Leg_Rounding = st.number_input("Down Leg Rounding", min_value=0.00, value = None, placeholder="0.00")
        with st.expander("Select your option", True):
            selected_pant_style = pant_styles()
        uploaded_files = st.file_uploader("Upload Reference pic", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        comments = st.text_area("Please list any comments or special requirements Below")

        if st.form_submit_button("Submit"):
            submitted_details = {
                "Date": Date,
                "Name": Name,
                "MobileNumber": Mobile_Number,
                "Email": Email,
                "DeliveryDate":delivery_date,
                "Category":category,
                "FullLength":Full_Length,
                "HandLength":Hand_Length,
                "Collar":Collar,
                "Shoulder":Shoulder,
                "SideCuts":Side_Cuts,
                "PantLength":Pant_Length,
                "ThighRounding":Thigh_Rounding,
                "LegRounding":Leg_Rounding,
                "PantStyle":selected_pant_style,
                "Files":uploaded_files,
                "Comments":comments
            }
            if not Name:
                st.write("Error: Name field is required.")
                return
            
            df_transposed=common_viewing(submitted_details)
        
            file_name,customer_id = save_and_view_boys_data.save_boys_data(submitted_details)
            st.success("Data submitted successfully!")
            # pdf generation
            
            pdf_filename = pdf.generate_pdf(df_transposed,file_name,customer_id)
            pdf.display_pdf(pdf_filename)

            
            print("saved")  

def maggam_form():
    with st.form("maggam_form", clear_on_submit=True):
        conn = connection_database.db()
        st.title("MaggamWork Enquiry Form :scroll:")  
        st.subheader("",divider="grey")   
        font_size_controller()
        # Fields for customer details
        Date = st.date_input("Date :date:", value=None,format="DD/MM/YYYY")
        Name = st.text_input("Name*", key = "name")
        Mobile_Number = st.text_input("Mobile Number**", key = "mobile")

        #---------------
        ## checking in the database that mobile number is exist already or not
        if Mobile_Number!='':
            conn.row_factory = mysql.connector.cursor.MySQLCursorDict
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customer_data WHERE phone=%s', (Mobile_Number,))
            row = cursor.fetchone()
            if row:
                st.write(":red[Warning: This Mobile Number already exists]")
        
        #--------------

        Email = st.text_input("Email :email:")  
        delivery_date = st.date_input("Delivery Date :calendar:", value=None,format="DD/MM/YYYY")
        
        with st.container(border=True):
            Stiching = st.radio("Stiching", ["Yes","No"], index = None, key = "stiching", horizontal=True)

        if Stiching == "Yes":
            category = "Blouse-Stiching"
            st.header('Blouse Measures (in Inches) :straight_ruler:', divider='grey')
            Blouse_Full_Length = st.number_input("Full Length",min_value=0.00, value = None, placeholder="0.00")
            Shoulder = st.number_input("Shoulder",min_value=0.00, value = None, placeholder="0.00")
            Hand_Length = st.number_input("Hand Length",min_value=0.00, value = None, placeholder="0.00")
            Hand_Rounding = st.number_input("Hand Rounding",min_value=0.00, value = None, placeholder="0.00")
            Arm_Hole = st.number_input("Arm Hole",min_value=0.00, value = None, placeholder="0.00")
            Upper_Chest = st.number_input("Upper Chest",min_value=0.00, value = None, placeholder="0.00")
            Chest = st.number_input("Chest",min_value=0.00, value = None, placeholder="0.00")
            Waist = st.number_input("Waist",min_value=0.00, value = None, placeholder="0.00")
            Front_Neck = st.number_input("Front Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")
            Back_Neck = st.number_input("Back Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")
            
                #new one's
            Boat_Neck = st.number_input("Boat Neck (Deep)",min_value=0.00, value = None, placeholder="0.00")
            Collar = st.number_input("Collar", min_value=0.00, value = None, placeholder="0.00")

            st.subheader('',divider="grey")
            with st.container(border=True):
                selected_neck_style, selected_blouse_style = blouse_styles()
            st.subheader("",divider="grey")
            closing_with, padding, piping, lace, tassels = blouse_selections()

        else:
            category = "No Stiching"
            # Initialize all variables with None
            Blouse_Full_Length = None
            Shoulder = None
            Hand_Length = None
            Hand_Rounding = None
            Arm_Hole = None
            Upper_Chest = None
            Chest = None
            Waist = None
            Front_Neck =None
            Back_Neck = None
                #new one's
            Boat_Neck = None
            Collar = None
            selected_neck_style = None
            selected_blouse_style = None
            closing_with= None 
            padding = None
            piping = None
            lace = None
            tassels = None
        uploaded_files = st.file_uploader("Upload Reference pic", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        comments = st.text_area("Please list any comments or special requirements Below")

        
        if st.form_submit_button("Submit"):
            submitted_details = {
                "Date": Date,
                "Name": Name,
                "MobileNumber": Mobile_Number,
                "Email": Email,
                "DeliveryDate":delivery_date,
                "Category":category,
                "BlouseFullLength":Blouse_Full_Length,
                "Shoulder":Shoulder,
                "HandLength":Hand_Length,
                "HandRounding":Hand_Rounding,
                "ArmHole":Arm_Hole,
                "UpperChest":Upper_Chest,
                "Chest":Chest,
                "Waist":Waist,
                "FrontNeck":Front_Neck,
                "BackNeck":Back_Neck,
                "BoatNeck":Boat_Neck,
                "Collar":Collar,
                "NeckStyle":selected_neck_style,
                "BlouseStyle":selected_blouse_style,
                "ClosingWith":closing_with,
                "Padding":padding,
                "Piping":piping,
                "Lace":lace,
                "Tassels":tassels,
                "Files": uploaded_files,
                "Comments":comments
            }
            if not Name:
                st.write("Error: Name field is required.")
                return
            df_transposed=common_viewing(submitted_details)
        
            file_name,customer_id  = save_and_view_maggam_data.save_maggam_data(submitted_details,Stiching)
            st.success("Data submitted successfully!")
        # pdf generation
            
            pdf_filename = pdf.generate_pdf(df_transposed,file_name,customer_id)
            pdf.display_pdf(pdf_filename)

            
            print("saved")  