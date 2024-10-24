import streamlit as st
import json
import os

def reset_app():
    # Clear specific session state variables
    st.session_state['reg_number'] = ''
    st.session_state['selected_view'] = 'Front View'

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

def display_features(features):
    st.subheader("Explore Features")
    # Create buttons for each feature
    cols = st.columns(len(features))
    for idx, (feature_name, feature_description) in enumerate(features.items()):
        if cols[idx].button(feature_name):
            st.info(f"**{feature_name}:** {feature_description}")

def main():
    st.title("Car Feature Explorer")
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'car_data.json')
    
    car_data = load_car_data(json_path)
    
    # Move inputs to sidebar
    st.sidebar.title("Car Selection")
    
    # Initialize session state variables if not already set
    if 'reg_number' not in st.session_state:
        st.session_state['reg_number'] = ''
    if 'selected_view' not in st.session_state:
        st.session_state['selected_view'] = 'Front View'
    
    # Input for car registration number
    reg_number = st.sidebar.text_input("Enter Car Registration Number", 
                                       value=st.session_state['reg_number'], 
                                       key="reg_number")
    
    # View selection without Bird's Eye View
    view_options = ["Front View", "Side View", "Rear View", "Interior View"]
    selected_view = st.sidebar.selectbox("Select a view to explore", 
                                         view_options, index=view_options.index(st.session_state['selected_view']), 
                                         key="selected_view")

    # Add Reset button in the sidebar
    st.sidebar.button("Reset", on_click=reset_app)
    
    reg_number = st.session_state['reg_number']
    selected_view = st.session_state['selected_view']
    
    if reg_number:
        car_info = car_data.get(reg_number.upper())
        if car_info:
            display_car_info(car_info)
        
            # Map views to image files
            view_images = {"Front View": "./CarEye/front_view.png", 
                           "Side View": "./CarEye/side_view.png", 
                           "Rear View": "./CarEye/rear_view.png", 
                           "Interior View": "./CarEye/interior_view.png"}
        
            display_car_image(selected_view, view_images)
        
            # Features for each view
            view_features = {"Front View": car_info['features']['front'],
                              "Side View": car_info['features']['side'], 
                              "Rear View": car_info['features']['rear'], 
                              "Interior View": car_info['features']['interior']}
        
            # Get features for the selected view
            features = view_features[selected_view]
        
            display_features(features)
        else:
            st.error("Car not found. Please check the registration number.")
    else:
        st.info("Description of the application...")

if __name__ == "__main__":
    main()
