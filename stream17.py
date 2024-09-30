import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Helper functions
def load_geotiff(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1)  # Read the first band
        transform = src.transform
        crs = src.crs
    return data, transform, crs

def band_arithmetic(data1, data2, operation='add'):
    if operation == 'add':
        result = data1 + data2
    elif operation == 'subtract':
        result = data1 - data2
    elif operation == 'multiply':
        result = data1 * data2
    elif operation == 'divide':
        result = np.divide(data1, data2, out=np.zeros_like(data1), where=data2!=0)
    else:
        raise ValueError("Operation not supported")
    return result

def apply_color_adjustment(data, brightness=1.0, contrast=1.0):
    adjusted_data = (data - np.mean(data)) * contrast + np.mean(data) * brightness
    adjusted_data = np.clip(adjusted_data, 0, 255)  # Ensure values are within valid range
    return adjusted_data

# Streamlit app
st.title("GeoTIFF Image Processing")

# Sidebar for user inputs
st.sidebar.header("Select Operation")
operation_type = st.sidebar.selectbox("Choose an Operation", ["Band Arithmetic", "Color Adjustment"])

if operation_type == "Band Arithmetic":
    st.header("Band Arithmetic")

    # Upload files
    uploaded_file1 = st.file_uploader("Upload First GeoTIFF Image", type=["tif"])
    uploaded_file2 = st.file_uploader("Upload Second GeoTIFF Image", type=["tif"])

    if uploaded_file1 and uploaded_file2:
        data1, _, _ = load_geotiff(uploaded_file1)
        data2, _, _ = load_geotiff(uploaded_file2)
        
        # Select operation
        operation = st.selectbox("Select Arithmetic Operation", ["add", "subtract", "multiply", "divide"])

        # Perform the band arithmetic
        result = band_arithmetic(data1, data2, operation)

        # Display the result
        st.subheader(f"Result of {operation.capitalize()} Operation")
        plt.imshow(result, cmap='gray')
        plt.colorbar()
        st.pyplot()

elif operation_type == "Color Adjustment":
    st.header("Color Adjustment")

    # Upload file
    uploaded_file = st.file_uploader("Upload GeoTIFF Image", type=["tif"])

    if uploaded_file:
        data, _, _ = load_geotiff(uploaded_file)

        # Slider for brightness and contrast
        brightness = st.sidebar.slider("Adjust Brightness", 0.0, 2.0, 1.0, 0.1)
        contrast = st.sidebar.slider("Adjust Contrast", 0.0, 2.0, 1.0, 0.1)

        # Apply color adjustment
        adjusted_data = apply_color_adjustment(data, brightness, contrast)

        # Display the result
        st.subheader("Color Adjusted Image")
        plt.imshow(adjusted_data, cmap='gray')
        plt.colorbar()
        st.pyplot()

# End of Streamlit app
