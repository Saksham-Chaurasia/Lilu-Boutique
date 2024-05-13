
import streamlit as st
import io
import zipfile
import connection_database 

# Function to fetch blouse files from the database
def fetch_blouse_files():
    conn = connection_database.db()
    cursor = conn.cursor()
    query = """
    SELECT bf.file_data, bf.file_name, bd.customer_id
    FROM blouse_files bf
    INNER JOIN blouse_data bd ON bf.blouse_id = bd.blouse_id
    """
    cursor.execute(query)
    files = cursor.fetchall()
    conn.close()
    return files

def fetch_topbottom_files():
    conn = connection_database.db()
    cursor = conn.cursor()
    query = """
    SELECT bf.file_data, bf.file_name, bd.customer_id
    FROM topbottom_files bf
    INNER JOIN topbottom_data bd ON bf.topbottom_id = bd.topbottom_id
    """
    cursor.execute(query)
    files = cursor.fetchall()
    conn.close()
    return files

def fetch_boys_files():
    conn = connection_database.db()
    cursor = conn.cursor()
    query = """
    SELECT bf.file_data, bf.file_name, bd.customer_id
    FROM boys_files bf
    INNER JOIN boys_data bd ON bf.boys_id = bd.boys_id
    """
    cursor.execute(query)
    files = cursor.fetchall()
    conn.close()
    return files

def fetch_maggam_files():
    conn = connection_database.db()
    cursor = conn.cursor()
    query = """
    SELECT bf.file_data, bf.file_name, bd.customer_id
    FROM maggam_files bf
    INNER JOIN maggam_data bd ON bf.maggam_id = bd.maggam_id
    """
    cursor.execute(query)
    files = cursor.fetchall()
    conn.close()
    return files

def fetch_blouselehenga_files():
    conn = connection_database.db()
    cursor = conn.cursor()
    query = """
    SELECT bf.file_data, bf.file_name, bd.customer_id
    FROM blouse_files bf
    INNER JOIN blehenga_data bd ON bf.blouse_id = bd.blouse_id
    """
    cursor.execute(query)
    files = cursor.fetchall()
    conn.close()
    return files


def image_gallery(image_type):
    # Define the appropriate fetch function based on the image type
    if image_type == "Blouse":
        fetch_files_func = fetch_blouse_files
    elif image_type == "Top/Bottom":
        fetch_files_func = fetch_topbottom_files
    elif image_type == "Boys":
        fetch_files_func = fetch_boys_files
    elif image_type == "Maggam":
        fetch_files_func = fetch_maggam_files
    elif image_type == "Blouse/Lehenga/Girls":
        fetch_files_func = fetch_blouselehenga_files
    else:
        st.error("Invalid image type!")
        return

    st.title(f"{image_type.capitalize()} Image Gallery")
    st.subheader("",divider="grey")

    # Fetch files from the database
    files = fetch_files_func()
    customer_ids = [customer_id for _, _, customer_id in files]

   # Sort the customer IDs
    sorted_customer_ids = sorted(list(set(customer_ids)))

    # Show popover with checkboxes for customer IDs
    st.sidebar.subheader("",divider="grey")
    

    # Multiselect widget for selecting customer IDs
    selected_customer_ids = []
    multiselect_key = f"select_customer_ids_{image_type.lower()}"
    selected_customer_ids += st.sidebar.multiselect(f"Select Customer IDs ({image_type.capitalize()})", sorted_customer_ids, key=multiselect_key)

    custom_input = st.sidebar.text_input(f"Enter custom range for {image_type} (e.g., 22-24)", "")
    

    # Parse custom range input
    if custom_input:
        if "-" in custom_input:
            start, end = map(int, custom_input.split("-"))
            selected_customer_ids.extend(range(start, end + 1))
        else:
            try:
                selected_customer_ids.append(int(custom_input))
            except ValueError:
                pass

    # Filter images based on selected customer IDs
    selected_images = [image for image, _, customer_id in files if customer_id in selected_customer_ids]
    selected_file_names = [file_name for _, file_name, customer_id in files if customer_id in selected_customer_ids]

    # Generate a unique key for the slider
    slider_key = f"grid_layout_{image_type.lower()}"

    # Customizable grid layout
    with st.expander("Grid Layout", True):
        num_columns = st.slider("", min_value=1, max_value=5, value=3, key=slider_key, label_visibility="collapsed")
    cols = st.columns(num_columns)
    for i, (image, file_name) in enumerate(zip(selected_images, selected_file_names)):
        if i % num_columns == 0:
            cols = st.columns(num_columns)
        with cols[i % num_columns]:
            st.image(image, caption=file_name, use_column_width=True)

    
    # Generate a unique key for the checkbox
    checkbox_key = f"select_all_checkbox_{image_type.lower()}"

    # Checkbox for selecting images to download
    selected_download_indices = []
    with st.expander("Download Images", True):
        select_all = st.checkbox("Select All", key=checkbox_key)
        if select_all:
            selected_download_indices = range(len(selected_file_names))
        else:
            # Generate a unique key for the multiselect widget
            multiselect_key = f"select_images_to_download_{image_type.lower()}"

            # Multiselect for selecting images to download
            selected_download_names = st.multiselect("Select Images to Download", selected_file_names, key=multiselect_key)
            selected_download_indices = [i for i, name in enumerate(selected_file_names) if name in selected_download_names]

        # Download button for selected images
        zip_data = io.BytesIO()
        with zipfile.ZipFile(zip_data, "w") as zip_file:
            for index in selected_download_indices: 
                img_data = files[index][0]  # Get image data directly from the database
                file_name = selected_file_names[index]
                zip_file.writestr(f"{file_name}.jpg", img_data)
        zip_data.seek(0)  # Reset the pointer to the beginning of the stream
        st.download_button(label="Download Images", data=zip_data.getvalue(), file_name=f"selected_{image_type.lower()}_images.zip")



