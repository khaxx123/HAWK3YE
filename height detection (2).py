import cv2
import numpy as np
image_path = "E:\\WhatsApp Image 2025-03-31 at 10.57.05_0ea7835c.jpg"  # Change path if needed
image = cv2.imread(image_path)
if image is None:
    print("Error: Image not found!")
    exit()
image_resized = cv2.resize(image, (800, 600))
gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
known_height_meters = 120  #assunming to be 120m tall
reference_pixel_height = 300  # Adjust this based on actual pixel detection
scale_factor = known_height_meters / reference_pixel_height  # Meters per pixel
# Process each detected object
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)  # Get bounding box
    if h > 50:  # Filter small objects
        real_height_meters = h * scale_factor  # Convert pixels to meters
        cv2.rectangle(image_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image_resized, f"Height: {real_height_meters:.2f} m", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Show result
cv2.imshow("Detected Objects with Height Estimation", image_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
