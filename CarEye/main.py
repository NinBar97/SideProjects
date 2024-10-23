import streamlit as st
import json

st.title("Car Feature Explorer")

# Input for car registration number
reg_number = st.text_input("Enter Car Registration Number")

# Load car data from JSON file
with open('./CarEye/car_data.json', 'r') as f:
    car_data = json.load(f)

if reg_number:
    car_info = car_data.get(reg_number.upper())
    if car_info:
        st.success(f"Details for {reg_number.upper()}:")
        
        # Display brand, model, and year in the same row
        col1, col2, col3 = st.columns(3)
        col1.write(f"**Brand:** {car_info['brand']}")
        col2.write(f"**Model:** {car_info['model']}")
        col3.write(f"**Year:** {car_info['year']}")
        
        # View selection without Bird's Eye View
        view_options = ["Front View", "Side View", "Rear View", "Interior View"]
        selected_view = st.selectbox("Select a view to explore", view_options)

        # Map views to image files
        view_images = {
            "Front View": "./CarEye/front_view.png",
            "Side View": "./CarEye/side_view.png",
            "Rear View": "./CarEye/rear_view.png",
            "Interior View": "./CarEye/interior_view.png"
        }

        # Display the selected image
        st.image(view_images[selected_view], caption=selected_view, use_column_width=True)

        # Features for each view
        view_features = {
            "Front View": car_info['features']['front'],
            "Side View": car_info['features']['side'],
            "Rear View": car_info['features']['rear'],
            "Interior View": car_info['features']['interior']
        }

        # Get features for the selected view
        features = view_features[selected_view]

        st.subheader("Explore Features")

        # Create buttons for each feature
        cols = st.columns(len(features))
        for idx, (feature_name, feature_description) in enumerate(features.items()):
            if cols[idx].button(feature_name):
                st.info(f"**{feature_name}:** {feature_description}")
    else:
        st.error("Car not found. Please check the registration number.")
