#!/usr/bin/env python3
"""
export-data-fallback.py: Fallback version that copies existing JSON exports and exports Postman collection.
Use this if mongosh is not available.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.resolve()
BACKEND_DIR = PROJECT_ROOT / "express-backend"
EXPORT_DIR = PROJECT_ROOT / "auto-exports"
EXPORT_DIR.mkdir(exist_ok=True)

def copy_existing_exports():
    """Copy existing lesson/order exports with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    lessons_src = BACKEND_DIR / "lessons-live-export.json"
    orders_src = BACKEND_DIR / "orders-live-export.json"
    lessons_dst = EXPORT_DIR / f"lessons-{timestamp}.json"
    orders_dst = EXPORT_DIR / f"orders-{timestamp}.json"

    for src, dst, name in [(lessons_src, lessons_dst, "lessons"), (orders_src, orders_dst, "orders")]:
        if src.is_file():
            shutil.copy(src, dst)
            size_kb = dst.stat().st_size // 1024
            print(f"✅ Copied {name} to {dst.name} ({size_kb} KB)")
        else:
            print(f"⚠️  {src.name} not found; skipping.")

def export_postman_collection():
    """Export the live Postman collection with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    src = BACKEND_DIR / "Test-API-Live.postman_collection.json"
    dst = EXPORT_DIR / f"AfterSchool-API-{timestamp}.postman_collection.json"
    if src.is_file():
        shutil.copy(src, dst)
        size_kb = dst.stat().st_size // 1024
        print(f"✅ Copied Postman collection to {dst.name} ({size_kb} KB)")
    else:
        print(f"⚠️  {src.name} not found; skipping.")

def main():
    print("🚀 Starting fallback export (copies existing files)...")
    copy_existing_exports()
    export_postman_collection()
    print("\n🎉 Fallback export complete!")
    print(f"📂 Files saved in: {EXPORT_DIR}")

if __name__ == "__main__":
    main()
