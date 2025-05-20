import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# Load color dataset
import pandas as pd
from io import StringIO

# Raw string with tab characters (⇨ copied exactly as you posted)
data = """color_name\thex\tR\tG\tB
Black\t#000000\t0\t0\t0
White\t#FFFFFF\t255\t255\t255
Red\t#FF0000\t255\t0\t0
Lime\t#00FF00\t0\t255\t0
Blue\t#0000FF\t0\t0\t255
Yellow\t#FFFF00\t255\t255\t0
Cyan\t#00FFFF\t0\t255\t255
Magenta\t#FF00FF\t255\t0\t255
Silver\t#C0C0C0\t192\t192\t192
Gray\t#808080\t128\t128\t128
Maroon\t#800000\t128\t0\t0
Olive\t#808000\t128\t128\t0
Green\t#008000\t0\t128\t0
Purple\t#800080\t128\t0\t128
Teal\t#008080\t0\t128\t128
Navy\t#000080\t0\t0\t128
Orange\t#FFA500\t255\t165\t0
Brown\t#A52A2A\t165\t42\t42
Pink\t#FFC0CB\t255\t192\t203"""

# Load the tab-separated values into a DataFrame
df = pd.read_csv(StringIO(data), sep="\t")

# ✅ Check it loaded correctly
print(df.head())
from math import sqrt

def closest_color(r, g, b, df):
    min_dist = float('inf')
    closest_name = 'Unknown'
    for _, row in df.iterrows():
        dist = sqrt((r - row['R'])**2 + (g - row['G'])**2 + (b - row['B'])**2)
        if dist < min_dist:
            min_dist = dist
            closest_name = row['color_name']
    return closest_name

# Your target color
target_rgb = (78, 59, 138)
closest = closest_color(*target_rgb, df)

print(f"🎯 Closest Color: {closest}")

@st.cache_data
def load_colors():
    df = pd.read_csv("colors.csv")
    return df
color_data = load_colors()
st.write("🎨 Loaded Color Data Sample:")
st.dataframe(color_data.head())

# Find closest color name
def get_color_name(R, G, B, color_data):
    min_dist = float('inf')
    closest_color = None
    for _, row in color_data.iterrows():
        try:
            d = ((R - int(row['R']))**2 + (G - int(row['G']))**2 + (B - int(row['B']))**2) ** 0.5  # Euclidean distance
            if d < min_dist:
                min_dist = d
                closest_color = row
        except Exception as e:
            st.write(f"Error reading row: {row} - {e}")
    return closest_color if closest_color is not None else {
        'color_name': 'Unknown',
        'hex': '#000000'
    }

# Streamlit UI
st.title("🎨 Color Detection from Image (No OpenCV)")


uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.write("**Click on the image below to detect a color**")

    coords = streamlit_image_coordinates(image, key="click_image")

    if coords is not None:
        x, y = int(coords['x']), int(coords['y'])
        st.write(f"📍 Clicked Coordinates: ({x}, {y})")

        image_np = np.array(image)
        if y < image_np.shape[0] and x < image_np.shape[1]:  # Ensure within bounds
            r, g, b = image_np[y, x]
            st.write(f"🎨 Clicked Pixel RGB: ({r}, {g}, {b})")

            color_data = load_colors()
            st.write("🎨 Loaded Color Data Sample:")
            st.dataframe(color_data.head())

            color_info = get_color_name(r, g, b, color_data)
            hex_color = color_info['hex']

            st.markdown(f"""
            ### 🎯 Detected Color: {color_info['color_name']}
            - RGB: ({r}, {g}, {b})
            - HEX: {hex_color}
            """)
            st.markdown(f"""
            <div style="width:100px; height:50px; background-color:{hex_color}; border:1px solid #000;"></div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Clicked outside image bounds.")
