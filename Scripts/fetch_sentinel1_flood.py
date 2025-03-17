import os
import json
import time
import requests
import geopandas as gpd
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Load credentials
load_dotenv()
CLIENT_ID = os.getenv("SENTINELHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("SENTINELHUB_CLIENT_SECRET")

# API Endpoints
TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
SEARCH_URL = "https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel1/search.json"

# Define Paths
BASE_DIR = "/mnt/c/Users/wilfr/Amini-project-assessment"
BOUNDARY_PATH = os.path.join(BASE_DIR, "data/admin_boundaries/gadm41_KEN_3.shp")

# Load the shapefile
try:
    print(f"📂 Loading shapefile: {BOUNDARY_PATH}")
    boundary = gpd.read_file(BOUNDARY_PATH)
    print("✅ Shapefile loaded successfully!")
except Exception as e:
    raise FileNotFoundError(f"❌ Error loading shapefile: {e}")

# Convert boundary to bounding box
try:
    print("🔹 Simplifying geometry...")
    minx, miny, maxx, maxy = boundary.total_bounds
    # Create a WKT polygon string from the bounding box
    wkt_geometry = f"POLYGON(({minx} {miny}, {maxx} {miny}, {maxx} {maxy}, {minx} {maxy}, {minx} {miny}))"
    print(f"🗺 Bounding Box (WKT): {wkt_geometry}")
except Exception as e:
    raise RuntimeError(f"❌ Error processing boundary: {e}")

# Function to get date range (last 6 months)
def get_date_range():
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=180)
    return start_date.strftime("%Y-%m-%dT%H:%M:%SZ"), end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

# Function to authenticate and get access token
def get_access_token():
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "openid"
    }
    for attempt in range(3):
        try:
            response = requests.post(TOKEN_URL, data=payload)
            if response.status_code == 200:
                token = response.json()["access_token"]
                print("🔑 Successfully retrieved access token.")
                return token
            else:
                print(f"⚠ API Token Request Failed (Attempt {attempt+1}): {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"⚠ Network error: {e}")
        time.sleep(5)
    raise RuntimeError("❌ Failed to get access token after multiple attempts.")

# Function to search for Sentinel-1 data
def search_sentinel1_data(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    start_date, end_date = get_date_range()

    params = {
        "maxRecords": 5,
        "startDate": start_date,
        "completionDate": end_date,
        "processingLevel": "GRD",
        "geometry": wkt_geometry,  # Use the WKT geometry string
        "productType": "GRD"
    }

    for attempt in range(3):
        try:
            print(f"🔍 Searching Sentinel-1 data (Attempt {attempt+1})...")
            response = requests.get(SEARCH_URL, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if "features" in data and len(data["features"]) > 0:
                    print(f"✅ Found {len(data['features'])} Sentinel-1 products.")
                    return data["features"]
                else:
                    print("⚠ No Sentinel-1 products found.")
                    return None
            elif response.status_code == 503:
                print(f"⚠ API service unavailable (Attempt {attempt+1}). Retrying...")
                time.sleep(10)
            else:
                raise RuntimeError(f"❌ API search failed: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"⚠ Network error during search: {e}")
            time.sleep(5)

    raise RuntimeError("❌ Failed to retrieve Sentinel-1 data after multiple attempts.")

# Main Execution
try:
    print("🔑 Getting API Access Token...")
    access_token = get_access_token()

    print("🔍 Searching for Sentinel-1 GRD Data...")
    products = search_sentinel1_data(access_token)

    if products:
        for product in products:
            print(f"✅ Found Sentinel-1 Product: {json.dumps(product, indent=2)}")
    else:
        print("⚠ No Sentinel-1 data found for the given date range.")
except Exception as e:
    print(f"❌ Error: {e}")
