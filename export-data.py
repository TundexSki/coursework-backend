#!/usr/bin/env python3
"""
export-data.py: Automatically exports MongoDB collections and Postman collection.
- Reads .env from express-backend to get MongoDB URI and DB name.
- Exports lessons and orders collections to JSON.
- Exports the live Postman collection from the running backend.
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Paths
PROJECT_ROOT = Path(__file__).parent.resolve()
BACKEND_DIR = PROJECT_ROOT / "express-backend"
ENV_FILE = BACKEND_DIR / ".env"

EXPORT_DIR = PROJECT_ROOT / "auto-exports"
EXPORT_DIR.mkdir(exist_ok=True)

def load_env():
    """Load key=value pairs from .env file (ignore comments, strip whitespace)."""
    env = {}
    if not ENV_FILE.is_file():
        sys.exit(f"❌ .env file not found at {ENV_FILE}")
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

def export_collection(mongo_uri, db_name, collection_name, out_path):
    """Export a MongoDB collection to JSON using mongosh (fallback to mongo if unavailable)."""
    # Prefer mongosh; fallback to mongo
    cmd = [
        "mongosh",
        mongo_uri,
        "--eval",
        f"db.getSiblingDB('{db_name}').{collection_name}.find().forEach(printjson);"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
        # Parse output lines (skip MongoDB shell chatter)
        json_lines = [ln for ln in result.stdout.splitlines() if ln.startswith("{")]
        data = [json.loads(ln) for ln in json_lines]
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"✅ Exported {collection_name} to {out_path.name} ({len(data)} records)")
    except subprocess.CalledProcessError as e:
        sys.exit(f"❌ Failed to export {collection_name}: {e.stderr}")
    except FileNotFoundError:
        sys.exit("❌ 'mongosh' not found. Please install MongoDB Shell.")
    except Exception as e:
        sys.exit(f"❌ Unexpected error exporting {collection_name}: {e}")

def export_postman_collection(base_url, out_path):
    """Export the live Postman collection from the backend (assumes Test-API-Live endpoint)."""
    # We'll fetch the collection file we created earlier; if you have an endpoint to generate it, replace this.
    collection_path = BACKEND_DIR / "Test-API-Live.postman_collection.json"
    if not collection_path.is_file():
        sys.exit(f"❌ Postman collection file not found at {collection_path}")
    with open(collection_path, encoding="utf-8") as f:
        data = json.load(f)
    # Optionally, replace placeholder URLs with the live base_url
    for item in data.get("item", []):
        url_obj = item["request"]["url"]
        if isinstance(url_obj, dict) and "raw" in url_obj:
            if "localhost:3000" in url_obj["raw"]:
                url_obj["raw"] = url_obj["raw"].replace("http://localhost:3000", base_url)
                url_obj["host"] = base_url.replace("https://", "").replace("http://", "").split("/")
                url_obj["host"] = url_obj["host"][0].split(".")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Exported Postman collection to {out_path.name}")

def main():
    print("🚀 Starting automated export...")
    env = load_env()
    mongo_uri = env.get("MONGODB_URI")
    db_name = env.get("DB_NAME", "courseworkDB")
    backend_url = env.get("BACKEND_URL", "https://aneskibackend.onrender.com")

    if not mongo_uri:
        sys.exit("❌ MONGODB_URI not found in .env")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    lessons_out = EXPORT_DIR / f"lessons-{timestamp}.json"
    orders_out = EXPORT_DIR / f"orders-{timestamp}.json"
    postman_out = EXPORT_DIR / f"AfterSchool-API-{timestamp}.postman_collection.json"

    export_collection(mongo_uri, db_name, "lessons", lessons_out)
    export_collection(mongo_uri, db_name, "orders", orders_out)
    export_postman_collection(backend_url, postman_out)

    print("\n🎉 Export complete!")
    print(f"📂 Files saved in: {EXPORT_DIR}")
    for p in (lessons_out, orders_out, postman_out):
        size_kb = p.stat().st_size // 1024
        print(f" - {p.name} ({size_kb} KB)")

if __name__ == "__main__":
    main()
