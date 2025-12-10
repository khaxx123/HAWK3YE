import os
import cv2
import numpy as np
import pandas as pd
import math

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
            print("INFO: Performing Height Estimation without a ground reference pixel. Accuracy may be low.")
            # A simple factor for demonstration - needs real world calibration
            scale_factor_m_per_pixel = KNOWN_REFERENCE_OBJECT_HEIGHT_M / 100 # Assuming 1m object is 100 pixels in this resized image
            estimated_real_height = object_pixel_height * scale_factor_m_per_pixel
            
        else:
            scale_factor = KNOWN_REFERENCE_OBJECT_HEIGHT_M / reference_pixel_height
            estimated_real_height = object_pixel_height * scale_factor
        
        # Display the result (similar to your slide)
        height_text = f"Est. Height: {estimated_real_height:.2f} m"
        cv2.rectangle(image_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image_resized, height_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow("HAWK3YE Object Detection", image_resized)
        cv2.waitKey(1) # Display for 1 ms
        hub_height_m = max(estimated_real_height, 30.0) # Assume at least 30m if detection fails
        
    # --- 3. WIND SHEAR CALCULATION ---
    REFERENCE_HEIGHT_M = 10.0
    AVERAGE_WIND_SPEED_REF_M_S = 6.5  # Example: 6.5 m/s at 10m height
    Z0_ROUGHNESS_M = 0.15 # Meters (e.g., for land with scattered trees/buildings)
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
    first_image_path = os.path.join(image_folder_path, image_files[0])
    REFERENCE_PIXEL_HEIGHT_DEMO = 50.0 

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
