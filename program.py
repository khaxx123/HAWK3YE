# hawk3ye_survey.py

import os
import cv2
import numpy as np
import pandas as pd
import math

# --- 1. CONFIGURATION ---
# IMPORTANT: Update these values based on your drone and site data
# CAMERA PARAMETERS (iPhone Camera)
FOCAL_LENGTH_PIXELS = 4000  # Placeholder - Must be accurately calibrated!
KNOWN_DRONE_FLIGHT_HEIGHT_M = 100  # Height the drone flies at, in meters
KNOWN_REFERENCE_OBJECT_HEIGHT_M = 1.0  # e.g., a known surveying pole on the ground

# WIND FARM PARAMETERS (NEW GLOBAL CONSTANT)
WIND_TURBINE_HUB_HEIGHT_M = 80.0 # Common hub height (Moved here to be global)
def estimate_height_and_wind_shear(image_path, reference_pixel_height=None):
    """
    Processes an image to estimate the height of an object (wind turbine or 
    reference pole) and then calculates the wind shear exponent.
    
    This function uses a simplified image-to-world conversion based on a 
    known flight height (or a known reference object for better accuracy).
    """
    
    # --- IMAGE LOADING AND PRE-PROCESSING ---
    image = cv2.imread(image_path)
    if image is None:
        return f"Error: Failed to load image at {image_path}", None
    
    # Resize for faster processing and display (similar to your existing code)
    image_resized = cv2.resize(image, (800, 600))
    gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
    
    # Simple edge detection to find contours (like a turbine/pole)
    # Using a Gaussian Blur and Canny Edge Detector as a starting point.
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # --- 2. HEIGHT DETECTION ---
    
    if not contours:
        print(f"Warning: No significant objects/contours detected in {os.path.basename(image_path)}")
        # Proceed to wind shear calculation using default ground roughness
        estimated_real_height = 0
    else:
        # Find the largest contour (assuming it's the primary object of interest or a clear reference)
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Pixel height of the detected object
        object_pixel_height = h
        
        if reference_pixel_height is None:
            # Method A: Use Drone's known flight height (less accurate for ground objects)
            # The Ground Sampling Distance (GSD) is approximated here.
            # GSD = (sensor_height * flight_height) / focal_length_mm
            # Simplified Pixel-to-Meter Scale Factor at the known flight height (H)
            # Scale Factor (M/Pixel) = Real_World_Reference_Size_M / Pixel_Reference_Size_P
            # We assume a fixed scale factor derived from known parameters for simplicity.
            # For a wind turbine in an aerial image, this is highly complex, so a reference object is needed.
            
            # --- For this simplified code, we must use a scale factor derived from a reference object ---
            # **IMPORTANT: The image processing step (contour detection) needs significant tuning/ML** # for reliable, consistent object and reference pole detection in real-world drone images.
            # We'll rely on the simplified method from your sample output slide for this demo.
            
            # Since no reference_pixel_height is passed, this is a placeholder for better code structure.
            print("INFO: Performing Height Estimation without a ground reference pixel. Accuracy may be low.")
            # A simple factor for demonstration - needs real world calibration
            scale_factor_m_per_pixel = KNOWN_REFERENCE_OBJECT_HEIGHT_M / 100 # Assuming 1m object is 100 pixels in this resized image
            estimated_real_height = object_pixel_height * scale_factor_m_per_pixel
            
        else:
            # Method B: Use a ground-based reference object (better for height)
            # Real_Height = (Object_Pixel_Height / Reference_Pixel_Height) * Known_Reference_Height_M
            # Assuming the largest contour IS the reference object for calibration:
            
            # --- The following logic should be integrated with an Object Detection (YOLO/HAAR) system ---
            # For the purpose of providing a functional Python file:
            
            # Use the known reference object's pixel height to establish the scale
            scale_factor = KNOWN_REFERENCE_OBJECT_HEIGHT_M / reference_pixel_height
            estimated_real_height = object_pixel_height * scale_factor
        
        # Display the result (similar to your slide)
        height_text = f"Est. Height: {estimated_real_height:.2f} m"
        cv2.rectangle(image_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image_resized, height_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow("HAWK3YE Object Detection", image_resized)
        cv2.waitKey(1) # Display for 1 ms
        
        # --- Using the object's height as the assumed wind turbine hub height ---
        # This will be the reference height for the wind shear calculation
        hub_height_m = max(estimated_real_height, 30.0) # Assume at least 30m if detection fails
        
    # --- 3. WIND SHEAR CALCULATION ---
    
    # Assuming typical average wind speeds at a reference mast height (like 10m)
    # In a real project, this data comes from a long-term measurement mast.
    REFERENCE_HEIGHT_M = 10.0
    AVERAGE_WIND_SPEED_REF_M_S = 6.5  # Example: 6.5 m/s at 10m height

    # The Power Law for Wind Shear: V2 = V1 * (Z2 / Z1)^alpha
    # We want to find the exponent 'alpha' that represents the site's terrain roughness.
    
    # For preliminary assessment, we can estimate roughness length (Z0) from terrain, 
    # then calculate alpha. Given the complexity, we will use a simplified fixed 'alpha' 
    # based on the *estimated terrain roughness* (e.g., Ramakkalmedu) 
    
    # Ramakkalmedu (India) is a hilly/mountainous region, which implies a higher surface roughness.
    # Typical Roughness Length (Z0) for Open Terrain with scattered obstacles: ~0.05 - 0.2 m
    # Let's assume a slightly rough terrain for the preliminary site.
    Z0_ROUGHNESS_M = 0.15 # Meters (e.g., for land with scattered trees/buildings)
    
    # The Power Law Exponent (alpha) can be approximated for a specific site from its roughness:
    # A simplified formula for the Power Law Exponent 'alpha'
    alpha_exponent = 0.20 # A standard average value for hilly terrain/complex sites is often between 0.15 and 0.25
    
    # Calculate the projected wind speed at a common wind turbine hub height (e.g., 80m)
    WIND_TURBINE_HUB_HEIGHT_M = 80.0 # Common hub height
    
    # Wind Speed at Hub Height (V2) = V1 * (Z2 / Z1)^alpha
    projected_wind_speed = AVERAGE_WIND_SPEED_REF_M_S * (WIND_TURBINE_HUB_HEIGHT_M / REFERENCE_HEIGHT_M)**alpha_exponent
    
    # Site Suitability Check
    # A commercially viable site typically needs an average wind speed > 6.0 m/s at hub height.
    is_suitable = projected_wind_speed >= 6.0
    
    # Create the result dictionary
    result = {
        "Image": os.path.basename(image_path),
        "Est. Hub Height (m)": hub_height_m if 'hub_height_m' in locals() else 'N/A',
        "Ref. Wind Speed (m/s) @ 10m": AVERAGE_WIND_SPEED_REF_M_S,
        "Wind Shear Alpha": alpha_exponent,
        f"Proj. Wind Speed (m/s) @ {WIND_TURBINE_HUB_HEIGHT_M}m": f"{projected_wind_speed:.2f}",
        "Site Suitability": "High Potential" if is_suitable else "Moderate/Low Potential"
    }
    
    return "Processing Complete", result

def main():
    # Ask the user for the folder path containing images
    image_folder_path = input("Enter the full path to the image folder (e.g., C:\\Users\\User\\HAWK3YE_Images): ").strip()
    
    if not os.path.isdir(image_folder_path):
        print(f"Error: Folder path '{image_folder_path}' is not a valid directory.")
        return

    # Get all image files (jpg, jpeg, png) from the folder
    image_files = [f for f in os.listdir(image_folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        print(f"Error: No images found in '{image_folder_path}'. Please check the path and file types.")
        return

    print(f"\nFound {len(image_files)} images. Starting HAWK3YE Analysis...\n")
    
    analysis_results = []
    
    # --- IMPORTANT Calibration Step ---
    # To perform the height calculation accurately, you MUST calibrate.
    # This simulates a quick manual calibration from the first image:
    first_image_path = os.path.join(image_folder_path, image_files[0])
    
    # For a real project, this must be a pixel measurement of a known object (e.g., a 1m pole)
    # This is a placeholder for the pixel height of the reference object as it appears in the RESIZED image (600px height).
    # You would typically zoom in on the reference object in the first image and input its pixel height.
    # For this script's demo purposes, we will assume a value.
    # (If the 1m pole is 50 pixels high in the resized (800x600) image)
    REFERENCE_PIXEL_HEIGHT_DEMO = 50.0 
    
    # Run the analysis for all images
    for filename in image_files:
        full_path = os.path.join(image_folder_path, filename)
        status, result = estimate_height_and_wind_shear(full_path, REFERENCE_PIXEL_HEIGHT_DEMO)
        
        if result:
            analysis_results.append(result)
            print(f"Image: {filename} \nProjected Wind Speed: {result[f'Proj. Wind Speed (m/s) @ {WIND_TURBINE_HUB_HEIGHT_M}m']}\nSuitability: {result['Site Suitability']}")

    # --- FINAL REPORT GENERATION ---
    if analysis_results:
        df = pd.DataFrame(analysis_results)
        output_file = "HAWK3YE_Wind_Farm_Survey_Report.csv"
        df.to_csv(output_file, index=False)
        print(f"\n--- Analysis Complete ---")
        print(f"Detailed report saved to: {output_file}")
        
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()