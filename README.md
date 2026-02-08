# 🩺 MedIQ: Medical Image Quality & Metadata Intelligence System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)

## 📌 Project Overview
**MedIQ** is a Health Informatics tool designed to solve the "Garbage In, Garbage Out" problem in medical AI. 

In real-world hospital settings, poor-quality X-rays (low contrast, motion blur, noise) lead to misdiagnosis. MedIQ automates the **Quality Control (QC)** process by:
1.  **Scanning** X-ray images using Computer Vision (OpenCV).
2.  **Calculating** objective quality metrics (SNR, Sharpness, Contrast).
3.  **Correlating** image quality with patient metadata (Age, Gender, Disease) to identify systemic data issues.

## 🚀 Key Features
* **Automated Quality Scoring:** Instantly flags "Reject" or "Warning" images based on Laplacian Variance (blur detection).
* **Metadata Intelligence:** Merges image data with patient demographics to find patterns (e.g., *Are scans of elderly patients more likely to be blurry due to movement?*).
* **Privacy-First Architecture:** Processes data locally; no patient data leaves the secure environment.

## 🛠️ Technology Stack
* **Algorithm:** Laplacian Variance for Blur Detection, Signal-to-Noise Ratio (SNR) estimation.
* **Data Processing:** Pandas & NumPy for high-performance CSV manipulation.
* **Visualization:** Streamlit for interactive real-time dashboards.

## 📊 Methodology (OSEMN Framework)
1.  **O**btain: Ingested NIH Chest X-ray Dataset (Sample).
2.  **S**crub: Cleaned metadata and resized images for efficient processing.
3.  **E**xplore: Visualized distribution of "Sharpness" across different disease classes.
4.  **M**odel: Applied threshold-based logic (Contrast < 20 = Reject).
5.  **I**nterpret: Generated actionable insights for Radiology Technicians.

## 📸 Screenshots

<img width="1920" height="1020" alt="Screenshot 2026-02-08 173201" src="https://github.com/user-attachments/assets/6a7648b1-08be-45d8-946d-fa7993173d16" />

<img width="1920" height="1020" alt="Screenshot 2026-02-08 173143" src="https://github.com/user-attachments/assets/75a28d89-d9f8-4048-9d81-52712d0d0fd2" />


## 👨‍💻 Author
**Abdul Razak Bilal**
