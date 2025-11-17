#!/bin/bash

# build-submission.sh: Automates the submission zip creation for the AfterSchool project

set -euo pipefail

# Paths
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SUBMISSION_DIR="$PROJECT_ROOT/submission"
ZIP_FILE="$PROJECT_ROOT/submission.zip"

# Clean previous artifacts
echo "Cleaning previous submission artifacts..."
rm -rf "$SUBMISSION_DIR" "$ZIP_FILE"

# Create directory structure
echo "Creating submission directory structure..."
mkdir -p "$SUBMISSION_DIR"/{vue-app,express-app,exports,postman}

# Copy Vue app (exclude node_modules and dist)
echo "Copying Vue app..."
cp -r vue-frontend/* "$SUBMISSION_DIR/vue-app/"
rm -rf "$SUBMISSION_DIR/vue-app/node_modules"
rm -rf "$SUBMISSION_DIR/vue-app/dist"

# Copy Express app (exclude node_modules)
echo "Copying Express app..."
cp -r express-backend/* "$SUBMISSION_DIR/express-app/"
rm -rf "$SUBMISSION_DIR/express-app/node_modules"

# Copy live exports (use live versions if they exist, otherwise fallback)
echo "Copying exports..."
if [[ -f express-backend/lessons-live-export.json ]]; then
  cp express-backend/lessons-live-export.json "$SUBMISSION_DIR/exports/lessons.json"
else
  cp express-backend/lessons-export.json "$SUBMISSION_DIR/exports/lessons.json"
fi

if [[ -f express-backend/orders-live-export.json ]]; then
  cp express-backend/orders-live-export.json "$SUBMISSION_DIR/exports/orders.json"
else
  cp express-backend/orders-export.json "$SUBMISSION_DIR/exports/orders.json"
fi

# Copy Postman collection (prefer live version)
echo "Copying Postman collection..."
if [[ -f express-backend/Test-API-Live.postman_collection.json ]]; then
  cp express-backend/Test-API-Live.postman_collection.json "$SUBMISSION_DIR/postman/AfterSchool-API.postman_collection.json"
else
  cp express-backend/Test-API.postman_collection.json "$SUBMISSION_DIR/postman/AfterSchool-API.postman_collection.json"
fi

# Create README with links
echo "Creating README..."
cat > "$SUBMISSION_DIR/README.md" <<'EOF'
# Coursework Submission

## Links

- **[Vue.js App]** GitHub Repository: https://github.com/aneski/vue-coursework
- **[Vue.js App]** GitHub Pages (live app): https://aneski.github.io/vue-coursework/
- **[Express.js App]** GitHub Repository: https://github.com/haxsysgit/aneskibackend
- **[Render.com Express.js App]** All lessons endpoint: https://aneskibackend.onrender.com/lessons

## Contents

- `vue-app/`: Vue.js frontend source code (node_modules excluded)
- `express-app/`: Express.js backend source code (node_modules excluded)
- `exports/`: MongoDB Atlas collections exported as JSON
  - `lessons.json`: All lessons from the live backend
  - `orders.json`: Sample orders created for testing
- `postman/`: Postman collection for API testing
  - `AfterSchool-API.postman_collection.json`: Import into Postman to run against the live backend

## Setup Notes

- Frontend is configured to communicate with the live Render backend via `VITE_API_URL`.
- Backend includes API documentation at the root (`/`).
- Sample orders were created to demonstrate order creation and export functionality.
EOF

# Create zip
echo "Creating submission.zip..."
cd "$SUBMISSION_DIR"
zip -r "$ZIP_FILE" .
cd "$PROJECT_ROOT"

# Report size
SIZE=$(du -h "$ZIP_FILE" | cut -f1)
echo "✅ submission.zip created ($SIZE)"

# Optional: show contents
echo "Contents:"
unzip -l "$ZIP_FILE" | tail -n +4 | head -n -2
