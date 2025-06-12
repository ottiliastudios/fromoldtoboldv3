
import streamlit as st
import pandas as pd
from PIL import Image
import os
import math

st.set_page_config(page_title="From Old to Bold", layout="centered")

# Centered logo
st.markdown(
    "<div style='text-align: center;'><img src='logo.png' width='180'></div>",
    unsafe_allow_html=True
)

st.write("Upload a photo of your old piece of jewelry. Our AI estimates the weight and suggests matching new designs.")

# Material selection
material = st.selectbox("Choose material", ["Silver", "Gold", "Other"])
if material == "Other":
    other_material = st.text_input("Please specify the material")

# Dummy volume-based estimation function (simplified)
def estimate_weight(image, density=10.5):
    r_outer = 1.0  # cm
    r_inner = 0.8  # cm
    height = 1.0   # cm
    volume = math.pi * (r_outer**2 - r_inner**2) * height
    return volume * density

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    predicted_weight = estimate_weight(image)
    st.success(f"Estimated weight: {predicted_weight:.2f} g")

    df = pd.read_csv("designs.csv")
    tolerance = 0.7
    matched = df[abs(df["weight"] - predicted_weight) <= tolerance]

    st.subheader("Matching new designs:")
    if not matched.empty:
        for _, row in matched.iterrows():
            st.image(row ["filename"], caption=f"{row['name']} – {row['weight']} g", use_container_width=True)
    else:
        st.write("No matching designs found.")
