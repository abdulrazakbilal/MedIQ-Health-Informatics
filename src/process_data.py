import cv2
import numpy as np
import pandas as pd
import os

# --- Configuration ---
IMAGE_FOLDER = r'data/raw_images'
METADATA_FILE = r'data/Data_Entry_2017.csv'
OUTPUT_FILE = r'data/final_data.csv'

def calculate_metrics(image_path):
    """
    Calculates quality metrics for a single image.
    Returns: dictionary of metrics.
    """
    # Read image as grayscale (0 flag) - faster and uses less RAM
    img = cv2.imread(image_path, 0)
    
    if img is None:
        return None

    # 1. Brightness: Average pixel intensity (0-255)
    brightness = np.mean(img)

    # 2. Contrast: Standard deviation of pixel intensity
    contrast = np.std(img)

    # 3. Sharpness: Variance of Laplacian (Standard method for blur detection)
    # High value = Sharp, Low value = Blurry
    sharpness = cv2.Laplacian(img, cv2.CV_64F).var()

    # 4. SNR (Signal-to-Noise Ratio): Mean / Std Dev
    # Higher is better clarity
    snr = brightness / contrast if contrast != 0 else 0

    return {
        'Brightness': round(brightness, 2),
        'Contrast': round(contrast, 2),
        'Sharpness': round(sharpness, 2),
        'SNR': round(snr, 2)
    }

def main():
    print("🚀 Starting MedIQ Analysis Engine...")
    
    # 1. Get list of images in your folder
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]
    print(f"📂 Found {len(image_files)} images to process.")

    results = []

    # 2. Loop through images (Process one by one to save RAM)
    for idx, file_name in enumerate(image_files):
        file_path = os.path.join(IMAGE_FOLDER, file_name)
        
        metrics = calculate_metrics(file_path)
        
        if metrics:
            metrics['Image Index'] = file_name # ID to link with CSV
            results.append(metrics)
            
        # Simple progress bar
        if (idx + 1) % 5 == 0:
            print(f"   ... Processed {idx + 1}/{len(image_files)} images")

    # 3. Convert results to DataFrame
    metrics_df = pd.DataFrame(results)
    print("✅ Image Analysis Complete.")

    # 4. Merge with Metadata (The "Health Informatics" part)
    print("🔗 Merging with Patient Metadata...")
    
    # Load the big CSV
    metadata_df = pd.read_csv(METADATA_FILE)
    
    # INNER JOIN: Only keep rows where we have BOTH an image and metadata
    final_df = pd.merge(metrics_df, metadata_df, on='Image Index', how='inner')
    
    # 5. Clean up columns (Optional: select only what we need)
    # We keep: ID, Metrics, Finding Labels (Disease), Age, Gender
    columns_to_keep = ['Image Index', 'Brightness', 'Contrast', 'Sharpness', 'SNR', 
                       'Finding Labels', 'Patient Age', 'Patient Gender']
    
    # Check if columns exist before selecting (safety check)
    existing_cols = [c for c in columns_to_keep if c in final_df.columns]
    final_df = final_df[existing_cols]

    # 6. Save to CSV
    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"🎉 Success! Processed data saved to: {OUTPUT_FILE}")
    print(f"📊 Final Dataset Shape: {final_df.shape}")

if __name__ == "__main__":
    main()