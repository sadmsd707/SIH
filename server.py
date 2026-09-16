"""
GeoLand Portal - Enterprise FastAPI Backend
Unified Digital Land Information System
"""

import json
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel

app = FastAPI(
    title="GeoLand Portal API",
    description="Technology-Driven Land Survey & Resurvey System with ISRO Bhuvan, Mahabhulekh 7/12, & QGIS Integration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SAMPLE_GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "sample_qgis_parcels.geojson")

def load_parcels_db():
    if os.path.exists(SAMPLE_GEOJSON_PATH):
        try:
            with open(SAMPLE_GEOJSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"type": "FeatureCollection", "features": []}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "GeoLand Portal API",
        "cadastre_version": "2024.1",
        "crs": "EPSG:4326 (WGS 84)"
    }

@app.get("/api/stats")
def get_stats():
    data = load_parcels_db()
    features = data.get("features", [])
    total = len(features)
    verified = sum(1 for f in features if f.get("properties", {}).get("status") == "verified")
    needs_review = sum(1 for f in features if f.get("properties", {}).get("status") == "needs_review")
    dispute = sum(1 for f in features if f.get("properties", {}).get("status") == "dispute")
    
    scores = [float(f.get("properties", {}).get("confidence_score", 0)) for f in features]
    avg_confidence = round(sum(scores) / total, 1) if total > 0 else 0.0
    
    total_acres = round(sum(
        float(f.get("properties", {}).get("new_survey_area_acres") or f.get("properties", {}).get("area_acres") or 0)
        for f in features
    ), 2)

    return {
        "total_parcels": total,
        "verified_parcels": verified,
        "needs_review": needs_review,
        "dispute": dispute,
        "average_confidence": avg_confidence,
        "total_surveyed_acres": total_acres,
        "data_source": "Mahabhulekh 7/12 / QGIS / ISRO Bhuvan",
        "state": "Maharashtra"
    }

@app.get("/api/parcels")
def list_parcels(status: Optional[str] = None, q: Optional[str] = None):
    data = load_parcels_db()
    features = data.get("features", [])
    
    if status and status != "all":
        features = [f for f in features if f.get("properties", {}).get("status") == status]
        
    if q:
        query = q.lower()
        features = [
            f for f in features 
            if query in str(f.get("properties", {}).get("owner_name", "")).lower()
            or query in str(f.get("properties", {}).get("survey_no", "")).lower()
            or query in str(f.get("properties", {}).get("parcel_id", "")).lower()
        ]
        
    return {"type": "FeatureCollection", "features": features}

@app.get("/api/parcels/{parcel_id}")
def get_parcel(parcel_id: str):
    data = load_parcels_db()
    features = data.get("features", [])
    for f in features:
        if f.get("properties", {}).get("parcel_id") == parcel_id:
            return f
    raise HTTPException(status_code=404, detail="Cadastral parcel not found")

@app.post("/api/parcels/import-qgis")
async def import_qgis_geojson(geojson_payload: dict):
    features = geojson_payload.get("features", [])
    if not features:
        raise HTTPException(status_code=400, detail="Empty or invalid GeoJSON payload")
    
    db = load_parcels_db()
    existing_ids = {f.get("properties", {}).get("parcel_id") for f in db.get("features", [])}
    
    imported_count = 0
    for f in features:
        pid = f.get("properties", {}).get("parcel_id")
        if not pid or pid in existing_ids:
            pid = f"GLP-QGIS-{len(db.get('features', [])) + 1:03d}"
            f.setdefault("properties", {})["parcel_id"] = pid
        db["features"].append(f)
        imported_count += 1
        
    with open(SAMPLE_GEOJSON_PATH, "w", encoding="utf-8") as out:
        json.dump(db, out, indent=2)
        
    return {
        "success": True,
        "imported_features": imported_count,
        "total_in_db": len(db["features"])
    }

@app.get("/api/webodm/status")
def webodm_status():
    return {
        "connected": True,
        "url": "http://localhost:8000",
        "api_version": "v1",
        "node": "WebODM Photogrammetry Engine",
        "status": "Ready to process aerial drone survey photos"
    }

@app.post("/api/webodm/upload-drone-images")
async def upload_drone_images(files: List[UploadFile] = File(...)):
    filenames = [f.filename for f in files]
    return {
        "success": True,
        "received_count": len(files),
        "files": filenames[:10],
        "estimated_gsd_cm": 2.1,
        "task_id": f"ODM-TASK-{len(filenames)}-FRAMES"
    }

@app.get("/api/export/geojson")
def export_geojson():
    data = load_parcels_db()
    return Response(
        content=json.dumps(data, indent=2),
        media_type="application/geo+json",
        headers={"Content-Disposition": "attachment; filename=geoland_cadastral_registry.geojson"}
    )

# Static file serving
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/styles.css", include_in_schema=False)
def serve_css():
    return FileResponse(os.path.join(BASE_DIR, "styles.css"))

@app.get("/app.js", include_in_schema=False)
def serve_js():
    return FileResponse(os.path.join(BASE_DIR, "app.js"))

@app.get("/sample_qgis_parcels.geojson", include_in_schema=False)
def serve_sample_geojson():
    return FileResponse(os.path.join(BASE_DIR, "sample_qgis_parcels.geojson"))

@app.get("/sample_1_exact_match_user_coords.geojson", include_in_schema=False)
def serve_sample1():
    return FileResponse(os.path.join(BASE_DIR, "sample_1_exact_match_user_coords.geojson"))

@app.get("/sample_2_bund_shift_user_coords.geojson", include_in_schema=False)
def serve_sample2():
    return FileResponse(os.path.join(BASE_DIR, "sample_2_bund_shift_user_coords.geojson"))

@app.get("/sample_3_road_dispute_user_coords.geojson", include_in_schema=False)
def serve_sample3():
    return FileResponse(os.path.join(BASE_DIR, "sample_3_road_dispute_user_coords.geojson"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
