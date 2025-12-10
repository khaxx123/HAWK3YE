README.md — HAWK3YE
🚀 Overview

HAWK3YE is an aerial intelligence system designed to support pre-construction surveying for wind farm site selection.
By integrating drone imagery, computer vision, and wind shear modeling, HAWK3YE evaluates whether a location has high potential for wind turbine installation.

This project contributes directly to UN SDG 7 – Affordable & Clean Energy, supporting India’s 500GW renewable mission.
(Ref: Slides on SDG7 and preconstruction surveying — 

HAWK3YE_PRECONSTRUCTION MAPPING…

)

📌 Key Features
1. Drone-Based Image Capture

360° coverage from a 45° camera angle

Images used for height estimation and wind shear analysis
(Workflow from slides — 

HAWK3YE_PRECONSTRUCTION MAPPING…

)

2. Height Estimation Using Photogrammetry

Contour-based object detection

Reference-object-based scaling

Supports turbine hub height estimation
(Code logic — 

program

)

3. Wind Shear & Site Suitability Analysis

Power law-based wind shear exponent

Predicts wind speed at 80m hub height

Labels site as High Potential, Moderate, or Low
(Code: projected_wind_speed, alpha exponent — 

program

)

4. Interactive Web Interface

Upload multiple drone images

Real-time previews

AI-processed results visualized using charts & tables

CSV export
(Full frontend system — 

html _ hawk3ye

)

🧠 System Architecture
Drone → Image Capture → Python Backend (CV + Wind Model) →  
Flask API → Interactive HTML/JS Dashboard → Site Analysis Report

📁 Project Structure
├── hawk3ye_survey.py        # Core backend processing (CV + wind modeling)
├── index.html               # Frontend UI for uploads and visualization
├── static/                  # (Optional) Images, CSS, JS
├── templates/               # (If using Flask templating)
├── HAWK3YE_Wind_Report.csv  # Generated output report
└── README.md                # Project documentation

⚙️ Installation
Prerequisites

Python 3.8+

pip

Any drone images in .jpg, .png

Install Dependencies

Run:

pip install opencv-python numpy pandas flask

🚀 Running the Backend
python hawk3ye_survey.py


This script will:

Ask for folder path containing drone images

Process each image (height + wind shear)

Generate a CSV report: HAWK3YE_Wind_Farm_Survey_Report.csv
(Report generation code — 

program

)

🌐 Running the Frontend

Open index.html in your browser.
Front features include:

Drag-and-drop uploads

Preview grid

Wind turbine animation during processing

Wind speed vertical profile chart

Result table displaying:

Hub height

Wind speed at 10m

Expected speed at 80m

Wind shear alpha

Site suitability
(All features defined in the HTML — 

html _ hawk3ye

)

📊 Output

The system generates:

1. On-Screen Dashboard

Hub height estimation

Wind speed projection

Suitability classification

Full results table

Wind speed profile chart

2. CSV Report

Contains:

Image name

Estimated hub height

Wind speed @10m

Wind speed @80m

Wind shear exponent

Suitability label
(Backend CSV export — 

program

)

🔍 Methodology
1. Object Height Estimation

Uses:

Contour detection

Bounding boxes

Reference object scaling

Conversion from pixel height → real height
Formula (from code):

Real Height = (PixelHeight_object / PixelHeight_reference) × ReferenceHeight_m

2. Wind Shear Modeling

Power-law equation used in the backend:

V₂ = V₁ × (Z₂ / Z₁)^α


Where:

α = 0.20 (hilly terrain assumption — 

program

)

Z₂ = 80m (hub height)

3. Suitability Classification

High Potential: V₂ ≥ 6.0 m/s

Moderate/Low: otherwise
(Code: suitability flag — 

program

)

🛠 Future Enhancements

YOLO-based turbine & reference object detection

True photogrammetry using structure-from-motion

Real-time wind speed estimation using on-site sensors

Integration into cloud dashboard for wind farm investors

👥 Team

Khahini B I – Lead

Shankar Durai N – Aerodynamics & Drone Systems

Siddharth K Ravani – Data & Deployment
