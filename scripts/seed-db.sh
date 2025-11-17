#!/bin/bash

# seed-db.sh: Seeds the MongoDB database with lessons using the seed.js script

set -euo pipefail

# Paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

cd "$BACKEND_DIR"

if [[ ! -f seed.js ]]; then
  echo "❌ seed.js not found in $BACKEND_DIR"
  exit 1
fi

echo "🌱 Seeding database with lessons..."
node seed.js

echo "✅ Database seeded."
