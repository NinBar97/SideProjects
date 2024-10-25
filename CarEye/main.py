import streamlit as st
import json
import os

def reset_app():
    # Clear specific session state variables
    st.session_state['reg_number'] = ''

def load_car_data(json_path):
    # Load car data from JSON file
    try:
        with open(json_path, 'r') as f:
            car_data = json.load(f)
        return car_data
    except FileNotFoundError:
        st.error("Error: 'car_data.json' file not found. Please ensure it is in the same directory as 'app.py'.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while loading car data: {e}")
        st.stop()

def display_car_view(view_name, car_info):
    # Map view names to image files
    image_files = {
        "Front View": "./CarEye/front_view.png",
        "Side View": "./CarEye/side_view.png",
        "Rear View": "./CarEye/rear_view.png",
        "Interior View": "./CarEye/interior_view.png"
    }
    
    # Display Image
    image_path = image_files.get(view_name)
    if image_path and os.path.exists(image_path):
        st.image(image_path, width=1000)
    else:
        st.warning(f"No image available for {view_name}.")

    # Map view names to keys in features
    view_key = view_name.lower().replace(" ", "")
    features = car_info['features'].get(view_key)
    if features:
        display_features(features)
    else:
        st.info(f"No features available for {view_name}.")


def display_features(features):
    st.subheader("Explore Features")
    for feature_name, feature_description in features.items():
        with st.expander(feature_name):
            st.write(feature_description)

def display_car_info(car_info):
    st.success(f"Details for {st.session_state['reg_number'].upper()}:")
    
    # Display brand, model, and year in the same row
    col1, col2, col3 = st.columns(3)
    col1.write(f"**Brand:** {car_info['brand']}")
    col2.write(f"**Model:** {car_info['model']}")
    col3.write(f"**Year:** {car_info['year']}")

def display_car_image(selected_view, view_images):
    # Display the selected image
    image_path = view_images[selected_view]
    if os.path.exists(image_path):
        st.image(image_path, caption=selected_view, use_column_width=True)
    else:
        st.warning(f"Image for {selected_view} not available.")

def main():
    st.set_page_config(page_title="Car Feature Explorer", page_icon="🚗", layout="wide", initial_sidebar_state="expanded")
    st.title("Car Feature Explorer")
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'car_data.json')
    
    car_data = load_car_data(json_path)
    
    # Initialize session state variables if not already set
    if 'reg_number' not in st.session_state:
        st.session_state['reg_number'] = ''
    
    # Move inputs to sidebar
    st.sidebar.title("Search for a Car")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Enter Registration Number")
    st.sidebar.text_input("Registration Number", value=st.session_state['reg_number'], key="reg_number")
    st.sidebar.markdown("---")
    st.sidebar.button("Reset", on_click=reset_app)

    reg_number = st.session_state['reg_number']
    
    if reg_number:
        car_info = car_data.get(reg_number.upper())
        if car_info:
            display_car_info(car_info)
            
            # Create tabs for different views
            tabs = st.tabs(["Front View", "Side View", "Rear View", "Interior View"])
            view_names = ["Front View", "Side View", "Rear View", "Interior View"]
            for tab, view_name in zip(tabs, view_names):
                with tab:
                    display_car_view(view_name, car_info)
        else:
            st.error("Car not found. Please check the registration number.")
    else:
        st.info("Enter a registration number in the sidebar to begin.")

if __name__ == "__main__":
    main()