# 🚁 HAWK3YE — Pre construction and mapping for setting up a  Wind Farm

## 🌍 Overview

**HAWK3YE** is an aerial intelligence system built to support **pre-construction surveying and site suitability analysis for wind farm development**.

By integrating **drone imagery**, **computer vision**, and **wind shear modeling**, HAWK3YE evaluates whether a given location has strong potential for wind turbine installation — *before* heavy investments are made.

This project aligns directly with **UN SDG 7 – Affordable & Clean Energy** and contributes to **India’s 500 GW renewable energy mission**, enabling smarter, data-driven renewable infrastructure planning.

---

## ✨ Key Features

### 1️⃣ Drone-Based Image Capture

* 360° aerial coverage using drones
* Optimized **45° camera tilt** for vertical object visibility
* Captured images serve as inputs for height estimation and wind analysis

---

### 2️⃣ Height Estimation Using Photogrammetry

* Contour-based object detection using OpenCV
* Bounding box extraction for objects
* **Reference-object-based scaling** for real-world measurement
* Supports **turbine hub height estimation** from aerial images

**Core Formula:**
[\text{Real Height} = \frac{\text{Pixel Height (Object)}}{\text{Pixel Height (Reference)}} \times \text{Reference Height (m)}]

---

### 3️⃣ Wind Shear & Site Suitability Analysis

* Implements **power-law wind shear model**
* Predicts wind speed at **80 m turbine hub height**
* Automatically classifies sites as:

  * 🟢 **High Potential**
  * 🟡 **Moderate Potential**
  * 🔴 **Low Potential**

**Wind Shear Equation:**
[V_2 = V_1 \times (Z_2 / Z_1)^\alpha]

Where:

* (\alpha = 0.20) (hilly terrain assumption)
* (Z_1 = 10,m), (Z_2 = 80,m)

---

### 4️⃣ Interactive Web Interface

* Drag-and-drop multiple image uploads
* Real-time image previews
* Animated turbine indicator during processing
* Dynamic charts for wind-speed vertical profiles
* Tabular result visualization
* **CSV export for reports**

---

## 🧠 System Architecture

```
Drone
  ↓
Image Capture
  ↓
Python Backend (Computer Vision + Wind Modeling)
  ↓
Flask API
  ↓
HTML / JavaScript Dashboard
  ↓
Wind Site Analysis Report
```

---

## 📁 Project Structure

```
HAWK3YE/
├── hawk3ye_survey.py        # Core backend (CV + wind modeling)
├── index.html               # Frontend UI & visualization
├── static/                  # CSS, JS, images (optional)
├── templates/               # Flask templates (optional)
├── HAWK3YE_Wind_Report.csv  # Generated analysis report
└── README.md                # Project documentation
```

---

## ⚙️ Installation

### 🔧 Prerequisites

* Python **3.8+**
* pip package manager
* Drone images (`.jpg`, `.png`)

### 📦 Install Dependencies

```bash
pip install opencv-python numpy pandas flask
```

---

## 🚀 Running the Backend

```bash
python hawk3ye_survey.py
```

### Backend Workflow

* Prompts for image folder path
* Processes each image for:

  * Object height estimation
  * Wind shear calculation
* Generates:

  * **HAWK3YE_Wind_Farm_Survey_Report.csv**

---

## 🌐 Running the Frontend

* Open `index.html` in any modern browser

### Frontend Capabilities

* Upload & preview drone images
* Animated processing indicators
* Wind-speed vertical profile chart
* Results table showing:

  * Estimated hub height
  * Wind speed @ 10 m
  * Wind speed @ 80 m
  * Wind shear exponent
  * Site suitability

---

## 📊 Output

### 🖥 On-Screen Dashboard

* Hub height estimation
* Wind speed projection
* Suitability classification
* Visual charts & tables

### 📄 CSV Report

Each record includes:

* Image name
* Estimated hub height
* Wind speed @ 10 m
* Wind speed @ 80 m
* Wind shear exponent (α)
* Suitability label

---

## 🔍 Methodology Summary

### Object Height Estimation

* Contour detection
* Bounding box analysis
* Reference-based scaling
* Pixel-to-meter conversion

### Wind Modeling

* Power-law based vertical wind profile
* Terrain-aware wind shear assumption

### Site Classification Logic

* **High Potential:** (V_{80} \ge 6.0,m/s)
* **Moderate / Low:** Below threshold

---

## 🛠 Future Enhancements

* YOLO-based object & reference detection
* True photogrammetry (Structure-from-Motion)
* On-site sensor integration for real-time wind data
* Cloud-based dashboard for investors & planners

---

## 👥 Team

* **Khahini B I** — Project Lead & System Design
* **Shankar Durai N** — Aerodynamics & Drone Systems
* **Siddharth K Ravani** — Data Analytics & Deployment

---

## 📌 Vision

*Measure before you build. Decide before you deploy.*
**HAWK3YE** empowers renewable planners with aerial intelligence — turning pixels into power.

