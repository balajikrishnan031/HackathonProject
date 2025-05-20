import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# Load color dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

color_data = load_colors()

# Function to find the closest color
def get_color_name(R, G, B, color_data):
    min_dist = float('inf')
    closest_color = None
    for _, row in color_data.iterrows():
        try:
            d = ((R - int(row['R'])) ** 2 +
                 (G - int(row['G'])) ** 2 +
                 (B - int(row['B'])) ** 2) ** 0.5
            if d < min_dist:
                min_dist = d
                closest_color = row
        except Exception as e:
            st.write(f"Error processing row: {e}")
    return closest_color if closest_color is not None else {
        'color_name': 'Unknown',
        'hex': '#000000'
    }

# Streamlit UI
st.set_page_config(page_title="Color Picker from Image", layout="centered")
st.title("🎨 Detect Color from Image (No OpenCV)")

uploaded_file = st.file_uploader("📁 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.write("🖱️ Click on the image below to detect the color of that pixel.")

    # Display image and get click coordinates
    coords = streamlit_image_coordinates(image, key="click_image")

    # If the user clicked on the image
    if coords is not None:
        x, y = int(coords["x"]), int(coords["y"])
        st.write(f"📍 Clicked coordinates: ({x}, {y})")

        # Convert image to numpy array to extract pixel RGB
        image_np = np.array(image)
        if y < image_np.shape[0] and x < image_np.shape[1]:
            r, g, b = image_np[y, x]
            st.write(f"🔍 RGB value: ({r}, {g}, {b})")

            color_info = get_color_name(r, g, b, color_data)
            hex_color = color_info["hex"]
            color_name = color_info["color_name"]

            # Show result
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"""
                <div style="width:80px; height:80px; background-color:{hex_color}; border:1px solid #000;"></div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                ### 🎯 Detected Color: **{color_name}**
                - **RGB**: ({r}, {g}, {b})
                - **HEX**: `{hex_color}`
                """)
        else:
            st.warning("⚠️ You clicked outside the image bounds.")
else:
    st.info("👆 Please upload an image to begin.")
