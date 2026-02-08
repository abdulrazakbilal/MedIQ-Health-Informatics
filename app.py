import streamlit as st
import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(page_title="MedIQ Analytics", layout="wide", page_icon="🩺")

# Style tweak to make it look professional
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
def analyze_image(image_file):
    """
    Same logic as your backend, tailored for Streamlit upload.
    """
    # Convert uploaded file to OpenCV format
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        return None, None

    # Calculate Metrics
    brightness = np.mean(img)
    contrast = np.std(img)
    # Laplacian Variance for Sharpness
    sharpness = cv2.Laplacian(img, cv2.CV_64F).var()
    snr = brightness / contrast if contrast != 0 else 0

    metrics = {
        'Brightness': round(brightness, 2),
        'Contrast': round(contrast, 2),
        'Sharpness': round(sharpness, 2),
        'SNR': round(snr, 2)
    }
    return img, metrics

# --- 3. MAIN DASHBOARD UI ---
st.title("🩺 MedIQ: Medical Image Quality Intelligence")
st.markdown("### Automated Quality Control & Health Informatics System")

# TABS for different views
tab1, tab2 = st.tabs(["🚀 Live Image Analysis", "📊 Research Insights"])

# --- TAB 1: LIVE ANALYSIS ---
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info("Upload a Chest X-ray to inspect its quality metrics in real-time.")
        uploaded_file = st.file_uploader("Upload X-Ray (PNG/JPG)", type=['png', 'jpg', 'jpeg'])

    with col2:
        if uploaded_file is not None:
            # Process the image
            img, metrics = analyze_image(uploaded_file)
            
            if img is not None:
                st.image(uploaded_file, caption="Analyzed Sample", width=300)
                
                # Display Metrics in a Grid
                st.subheader("Quality Diagnostics")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Brightness", metrics['Brightness'], help="Avg pixel intensity (Target: 100-150)")
                m2.metric("Contrast", metrics['Contrast'], help="Std Dev of intensity (Target: >40)")
                m3.metric("Sharpness", metrics['Sharpness'], help="Laplacian Variance. <500 usually implies blur.")
                m4.metric("SNR (Signal/Noise)", metrics['SNR'], help="Higher is clearer.")
                
                # Automated Recommendation
                st.subheader("System Verdict")
                if metrics['Sharpness'] < 100 or metrics['Contrast'] < 20:
                    st.error("🔴 REJECT: Image quality too low for reliable diagnosis.")
                elif metrics['Sharpness'] < 500:
                    st.warning("🟡 WARNING: Marginal quality. Check for motion blur.")
                else:
                    st.success("🟢 ACCEPT: High quality scan suitable for CAD analysis.")

# --- TAB 2: RESEARCH INSIGHTS (The "Health Informatics" Part) ---
with tab2:
    st.header("Dataset Analytics")
    
    # Load the processed data
    try:
        df = pd.read_csv("data/final_data.csv")
        
        # Row 1: Dataset Overview
        st.write(f"**Analyzing {len(df)} Patient Records** (Merged with Image Metadata)")
        st.dataframe(df.head())

        # Row 2: Visualizations
        row2_col1, row2_col2 = st.columns(2)
        
        with row2_col1:
            st.subheader("Image Sharpness Distribution")
            fig, ax = plt.subplots()
            sns.histplot(df['Sharpness'], kde=True, color="blue", ax=ax)
            ax.set_title("Are most scans sharp or blurry?")
            st.pyplot(fig)
            
        with row2_col2:
            st.subheader("Brightness vs. Patient Age")
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x='Patient Age', y='Brightness', hue='Patient Gender', ax=ax)
            ax.set_title("Does age affect scan quality? (Motion artifacts)")
            st.pyplot(fig)

    except FileNotFoundError:
        st.error("❌ Data not found. Please run 'src/process_data.py' first.")