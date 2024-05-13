import streamlit as st
import forms
import display_data
from streamlit_option_menu import option_menu
import pickle 
from pathlib import Path
import streamlit_authenticator as stauth 
import display_deliver, gallery
import dashboard, status
def sidebar():
    st.sidebar.image("Store_image.png", width=200)
    hide_img_fs = '''
    <style>
    button[title="View fullscreen"]{
        visibility:hidden;}
    </style>
    '''
    st.markdown(hide_img_fs, unsafe_allow_html=True)
    st.sidebar.markdown("#")
    st.sidebar.markdown("---")

    with st.sidebar:
        choose = option_menu("Main Menu",["Home", "Forms" ,"Maggam Handwork", "Garment Records","Gallery"],
                            icons = ['house','file-text','flower2','database-fill','images'],
                            menu_icon='list' , default_index=0,
                            styles={
                                "icon": {"color": "orange", "font-size": "25px"},
                                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color":"#888"},
                                "nav-link-selected": {"background-color": "#FFD700"},
                            })
     
    return choose
def home_page():
    # Set the background image
    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://t3.ftcdn.net/jpg/03/34/53/90/360_F_334539044_HHB5Xav4s5L6DRJB9BsLamDiU1NHefPl.jpg");
        background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
        background-position: center;  
        background-repeat: no-repeat;
    }
    </style>
    """

    st.markdown(background_image, unsafe_allow_html=True)
    st.markdown("# Welcome to the Customer Data App!")
    st.markdown("Select an option from the sidebar to get started.")

    #display_deliver.delivery_dashboard()
    status.update_overdue_status()
    dashboard.delivery_dashboard()


def main_page():
    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://thumbs.dreamstime.com/b/tailoring-cut-confection-sewing-tools-manufacture-clothing-90046013.jpg");
        background-size: 100vw 100vh; 
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(255, 255, 255, 0.5); 
        position: relative;
        z-index: 1;
    }
    </style>
    """

    st.markdown(background_image, unsafe_allow_html=True)
    #create_table()
    st.write("# Customer Data App")
    garment_type = st.selectbox("Select Garment Type", ["select any option","Blouses","Top/Bottom", "Blouse/Lehenga/Girls", "Boys"])

    if garment_type == "Blouses":
        forms.blouse_form()    
    elif garment_type == "Top/Bottom":
        forms.top_bottom_form()
    elif garment_type == "Blouse/Lehenga/Girls":
        forms.blouse_lehenga_girls_form()
    elif garment_type == "Boys":
        forms.boys_form()
    

def scissors_page():
    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://thumbs.dreamstime.com/b/tailoring-cut-confection-sewing-tools-manufacture-clothing-90046013.jpg");
        background-size: 100vw 100vh; 
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(255, 255, 255, 0.5); 
        position: relative;
        z-index: 1;
    }
    </style>
    """
    st.markdown(background_image, unsafe_allow_html=True)

    forms.maggam_form()
    



def view_all_data():
    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://media.istockphoto.com/id/488440872/photo/artisan-working-with-leather.webp?b=1&s=170667a&w=0&k=20&c=fAa2FnMBqkLokaDiJdMGZ0e4XwVd59Q9jj6p21sNH3Y=");
        background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
        background-position: center;  
        background-repeat: no-repeat;
    }
    """
    st.markdown(background_image, unsafe_allow_html=True)   
    display_data.customer_info()

def gallery_page():
    # Set the background image
    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://t3.ftcdn.net/jpg/03/34/53/90/360_F_334539044_HHB5Xav4s5L6DRJB9BsLamDiU1NHefPl.jpg");
        background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
        background-position: center;  
        background-repeat: no-repeat;
    }
    </style>
    """

    st.markdown(background_image, unsafe_allow_html=True)
    st.header("Welcome to the :rainbow[Gallery Section!]", divider="rainbow")
    
    
    with st.popover("Select Garment Section"):
        blouse = st.checkbox("Blouse")
        topbottom = st.checkbox("Top/Bottom")
        boys = st.checkbox("Boys")
        lehenga = st.checkbox("Blouse/Lehenga/Girls")
        maggam = st.checkbox("Maggam Handwork")

    
    if blouse:
        gallery.image_gallery("Blouse")
    elif topbottom:
        gallery.image_gallery("Top/Bottom")
    elif boys:
        gallery.image_gallery("Boys")
    elif lehenga:
        gallery.image_gallery("Blouse/Lehenga/Girls")
    elif maggam:
        gallery.image_gallery("Maggam")



choose = sidebar()

if choose == "Home":
    home_page()

elif choose == "Forms":
    main_page()

elif choose == "Maggam Handwork":
    scissors_page()

elif choose == "Garment Records":
    view_all_data()

elif choose =="Gallery":
    gallery_page()
    

###


