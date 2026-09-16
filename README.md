# 🌍 GeoLand Portal — Technology-Driven Land Survey & Resurvey System

> **A modern, enterprise-grade unified digital land information system integrating Drone Photogrammetry (WebODM), Cadastral Mapping (QGIS), Record of Rights (RoR 7/12), Mutation Records, Real-Time Kinematic (RTK) GPS, and Dynamic QR-Code Land Verification.**

---

## 🚀 1. The Technology Pipeline

```
┌─────────────────┐       ┌─────────────────┐       ┌──────────────────────┐
│  Drone Capture  │ ────> │     WebODM      │ ────> │ True Orthophoto (TIF) │
│ (DJI RTK / GCP) │       │ (OpenSfM / MVS) │       │  (2.1 cm/px GSD)     │
└─────────────────┘       └─────────────────┘       └──────────┬───────────┘
                                                               │
┌─────────────────┐       ┌─────────────────┐                  │
│ QGIS Processing │ <──────────────────────────────────────────┘
│ (Cadastre Bound)│
└────────┬────────┘
         │ GeoJSON
         ▼
┌─────────────────┐       ┌─────────────────┐       ┌──────────────────────┐
│ GeoLand Portal  │ ────> │   Google Maps   │ ────> │      Parcel ID       │
│  (GIS Engine)   │       │ Hybrid Satellite│       │ (e.g. GLP-MH-001)    │
└────────┬────────┘       └─────────────────┘       └──────────┬───────────┘
         │                                                     │
         ▼                                                     ▼
┌─────────────────┐       ┌─────────────────┐       ┌──────────────────────┐
│ Dynamic QR Code │ ────> │ Land Details    │ ────> │   Confidence Score   │
│ (Scan to Verify)│       │ (RoR 7/12/Waras)│       │ (Old vs New Survey)  │
└─────────────────┘       └─────────────────┘       └──────────────────────┘
```

---

## 🌟 2. Core Features Built & Verified

| Feature | Description |
|---|---|
| **📊 Real-Time Cadastral KPI Metrics** | Live counters for **Total Parcels**, **Verified Parcels** ($\ge 90\%$), **Needing Review** ($70\% - 89\%$), **Under Dispute** ($<70\%$), and **Weighted Average Confidence Index**. |
| **🛰️ Google Hybrid Satellite Cadastral Map** | High-resolution satellite tiles (`mt1.google.com/vt/lyrs=y`) with interactive vector boundaries, survey number centroid markers, and status color coding. |
| **🔄 WebODM Orthophoto Viewer** | True orthomosaic layer with live toggle and opacity slider overlay directly atop satellite imagery. |
| **📐 Real QGIS GeoJSON Ingestion** | Drag-and-drop or file upload of actual `.geojson` polygons exported from QGIS desktop. Automatic area calculation via **Turf.js**. |
| **📱 Dynamic Verifiable QR Codes** | Crisp client-side QR generation via `QRCode.js` linking directly to verifiable digital land record certificates with 1-click PNG download. |
| **⚖️ Survey Comparison (Old vs New)** | Side-by-side comparison between **Traditional Chain/Plane Table Survey** area and **Modern Drone RTK Resurvey** area with variance percentage. |
| **📜 RoR 7/12 & Mutation History** | Complete chain-of-title timeline: Original Allotment &rarr; Succession / Waras &rarr; Partition / Watap &rarr; Registered Sale Deeds. |
| **💯 Multi-Factor Confidence Score** | Calculated based on RTK GPS centimeter precision, Ground Control Points (GCP) count, boundary marker tag status, and area discrepancy. |

---

## 💻 3. How to Run Locally Right Now (100% Free)

### Option A: Zero Install (Instant Browser Open)
You do not need to install anything! Simply open the project directory:
```
C:\Users\Atharva\.gemini\antigravity\scratch\geoland-portal
```
Double-click **`index.html`** in any web browser (Chrome, Edge, Firefox, Brave). 
The entire GIS portal, satellite map, Turf.js spatial analysis, QR generator, and sample QGIS datasets will run instantly!

---

### Option B: Local Web Server (Python)
If you install Python on your machine:
```bash
cd C:\Users\Atharva\.gemini\antigravity\scratch\geoland-portal
python -m http.server 8080
```
Open [http://localhost:8080](http://localhost:8080) in your browser.

---

### Option C: FastAPI Full-Stack Backend
```bash
cd C:\Users\Atharva\.gemini\antigravity\scratch\geoland-portal
pip install -r requirements.txt
python server.py
```
Open [http://localhost:8080](http://localhost:8080) for the portal and [http://localhost:8080/docs](http://localhost:8080/docs) for the interactive Swagger REST API.

---

## 🌐 4. Free Online Deployment Guide (Share with Judges/Users)

### Method 1: GitHub Pages (Recommended & 100% Free)
1. Create a free repository on [GitHub.com](https://github.com) named `geoland-portal`.
2. Push the files in `geoland-portal`:
   ```bash
   git init
   git add .
   git commit -m "Deploy GeoLand Cadastral Portal"
   git branch -M main
   git remote add origin https://github.com/<YOUR-USERNAME>/geoland-portal.git
   git push -u origin main
   ```
3. In GitHub, go to **Settings &rarr; Pages &rarr; Source &rarr; Select 'main' branch &rarr; Click Save**.
4. Your website will be live in ~60 seconds at:
   `https://<YOUR-USERNAME>.github.io/geoland-portal/`

---

### Method 2: Vercel / Netlify (Zero Configuration, Free HTTPS)
1. Sign up for free at [Vercel](https://vercel.com) or [Netlify](https://netlify.com).
2. Click **Add New Project** &rarr; Drag and drop the `geoland-portal` folder into the browser window.
3. Your site is deployed instantly on a custom `.vercel.app` or `.netlify.app` domain with free SSL!

---

### Method 3: Render.com (Full Python FastAPI Server)
1. Push this folder to GitHub.
2. Sign in to [Render.com](https://render.com) (Free Tier).
3. Click **New + &rarr; Web Service** &rarr; Select your GitHub repository.
4. Render will automatically detect `render.yaml` and deploy `server.py` with FastAPI on Python 3.11.

---

## 📂 5. How to Ingest Your Real QGIS / WebODM Data

1. **In QGIS Desktop**:
   - Create or edit your agricultural parcel boundary polygon layers.
   - Right-click layer &rarr; **Export &rarr; Save Features As... &rarr; Format: GeoJSON**.
   - CRS: Select **EPSG:4326 - WGS 84**.
   - Save file (e.g. `my_village_parcels.geojson`).
2. **In GeoLand Portal**:
   - Open the **"WebODM & QGIS Station"** tab in the top navigation.
   - Drag and drop your `.geojson` file into the **"Import Real QGIS Cadastral GeoJSON"** dropzone.
   - The portal will automatically compute geodesic acreage, vertex coordinates, centroid tags, and confidence scores using **Turf.js**, then instantly update the live satellite map and dashboard!
3. **In WebODM**:
   - Run your flight photogrammetry task.
   - Download the orthophoto (`orthophoto.tif`) or exported vector boundary shapefile/GeoJSON.
   - Toggle the **"Toggle WebODM Ortho"** button on the Satellite Map to compare the drone orthomosaic with historical satellite imagery!

---

## 📋 6. Complete Cadastral Parcel Card Specification

Every parcel in the system contains:
```
┌──────────────────────────────────────────────────────────────┐
│ Owner:               Ramesh Vishnu Patil (S/o Vishnu Patil)   │
│ Area (Old vs New):   2.50 Ac (Old RoR) vs 2.47 Ac (Drone RTK)│
│ Survey No. & Gat:    Survey 45/1A • Gat 104 • Khadkewadi     │
│ Coordinates:         Point 1: 17.672050, 75.900120           │
│                      Point 2: 17.672080, 75.901650 ...       │
│ Google Map:          Direct navigation link to coordinates   │
│ Boundary:            Interactive Leaflet Vector Polygon      │
│ QR Code:             Dynamic scannable cryptographic stamp   │
│ Confidence Score:    96.4% (RTK: ±1.8 cm, 8 GCP Targets)     │
│ RoR / Mutation:      7/12 Extract • 2 Recorded Mutations     │
│ Survey Comparison:   Delta: 1.2% (Within 2% legal tolerance) │
└──────────────────────────────────────────────────────────────┘
```
