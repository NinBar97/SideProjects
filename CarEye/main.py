import streamlit as st
import json
import os
import pandas as pd


def reset_app():
    # Clear specific session state variables
    st.session_state["reg_number"] = ""
    st.session_state["selected_package"] = ""
    st.session_state["compare_packages"] = []


def load_car_data(json_path):
    # Load car data from JSON file
    try:
        with open(json_path, "r") as f:
            car_data = json.load(f)
        return car_data
    except FileNotFoundError:
        st.error(
            "Error: 'car_data.json' file not found. Please ensure it is in the same directory as 'app.py'."
        )
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


def display_package_info(package_name, package_info):
    st.header(f"Package: {package_name}")
    st.write(package_info["description"])


def display_car_view(view_name, features):
    # Map view names to image files
    image_files = {
        "Front View": os.path.join("./CarEye/Images", "front_view.png"),
        "Side View": os.path.join("./CarEye/Images", "side_view.png"),
        "Rear View": os.path.join("./CarEye/Images", "rear_view.png"),
        "Interior View": os.path.join("./CarEye/Images", "interior_view.png"),
    }

    # Display Image
    image_path = image_files.get(view_name)
    if image_path and os.path.exists(image_path):
        st.image(image_path, width=800)
    else:
        st.warning(f"No image available for {view_name}.")

    # Display Features
    if features:
        display_features(features)
    else:
        st.info(f"No features available for {view_name}.")


def display_features(features):
    st.subheader("Explore Features")
    for feature_name, feature_description in features.items():
        with st.expander(feature_name):
            st.write(feature_description)


def compare_features(packages_info):
    st.subheader("Feature Comparison")
    view_names = ["Front View", "Side View", "Rear View", "Interior View"]
    for view_name in view_names:
        st.write(f"### {view_name}")
        view_key = view_name.lower().replace(" ", "")

        # Collect features for each package
        data = {}
        all_features = set()
        for pkg_name, pkg_info in packages_info.items():
            features = pkg_info["features"].get(view_key, {})
            data[pkg_name] = features
            all_features.update(features.keys())

        # Convert the set to a sorted list
        all_features = sorted(list(all_features))

        # Create a DataFrame for comparison
        comparison_table = pd.DataFrame(index=all_features)
        for pkg_name, features in data.items():
            # Map features to the DataFrame
            comparison_table[pkg_name] = comparison_table.index.map(features).fillna(
                "Not Available"
            )

        # Display the table
        st.table(comparison_table)
        st.markdown("---")


def main():
    st.set_page_config(
        page_title="Car Feature Explorer",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("Car Feature Explorer")

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "car_data.json")

    car_data = load_car_data(json_path)

    # Initialize session state variables if not already set
    if "reg_number" not in st.session_state:
        st.session_state["reg_number"] = ""
    if "selected_package" not in st.session_state:
        st.session_state["selected_package"] = ""
    if "compare_packages" not in st.session_state:
        st.session_state["compare_packages"] = []

    # Move inputs to sidebar
    st.sidebar.title("Search for a Car")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Enter Registration Number")
    st.sidebar.text_input(
        "Registration Number", value=st.session_state["reg_number"], key="reg_number"
    )
    st.sidebar.markdown("---")
    st.sidebar.button("Reset", on_click=reset_app)

    reg_number = st.session_state["reg_number"]

    if reg_number:
        car_info = car_data.get(reg_number.upper())
        if car_info:
            display_car_info(car_info)

            # Package Selection
            packages = list(car_info.get("packages", {}).keys())
            if packages:
                st.sidebar.subheader("Select Package")
                selected_package = st.sidebar.selectbox(
                    "Package", packages, key="selected_package"
                )
                st.sidebar.markdown("---")

                # Package Comparison
                st.sidebar.subheader("Compare Packages")
                compare_packages = st.sidebar.multiselect(
                    "Select Packages to Compare", packages, key="compare_packages"
                )

                # Display Selected Package
                if selected_package:
                    package_info = car_info["packages"][selected_package]
                    display_package_info(selected_package, package_info)

                    # Create tabs for different views
                    tabs = st.tabs(
                        ["Front View", "Side View", "Rear View", "Interior View"]
                    )
                    view_names = [
                        "Front View",
                        "Side View",
                        "Rear View",
                        "Interior View",
                    ]
                    for tab, view_name in zip(tabs, view_names):
                        with tab:
                            view_key = view_name.lower().replace(" ", "")
                            features = package_info["features"].get(view_key)
                            if features:
                                display_car_view(view_name, features)
                            else:
                                st.info(f"No features available for {view_name}.")

                # Display Comparison if more than one package is selected
                if len(compare_packages) > 1:
                    st.header("Package Comparison")
                    compare_packages_info = {
                        pkg: car_info["packages"][pkg] for pkg in compare_packages
                    }
                    compare_features(compare_packages_info)
            else:
                st.info("No packages available for this car.")
        else:
            st.error("Car not found. Please check the registration number.")
    else:
        st.info("Enter a registration number in the sidebar to begin.")


if __name__ == "__main__":
    main()
