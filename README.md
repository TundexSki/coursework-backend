# After-School Lessons Backend

Express.js + MongoDB backend API for the CST3144 After-School Lessons coursework project.

## Links

- **Live API**: https://tundeh-backend.onrender.com
- **Frontend App**: https://TundexSki.github.io/coursework-frontend/
- **Frontend Repo**: https://github.com/TundexSki/coursework-frontend

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and available routes |
| GET | `/lessons` | Get all lessons |
| GET | `/lessons/:id` | Get single lesson by ID |
| GET | `/search?q=` | Search lessons by subject/location |
| POST | `/orders` | Create a new order |
| PUT | `/lessons/:id` | Update lesson (e.g., reduce spaces) |
| GET | `/images/:name` | Get lesson image |

## Tech Stack

- **Node.js** with Express.js
- **MongoDB** native driver (no Mongoose)
- **CORS** enabled for frontend access

## Environment Variables

Create a `.env` file with:

```
MONGODB_URI=mongodb+srv://...
DB_NAME=coursework
RENDER_URL=https://your-backend.onrender.com
```

## Setup

```sh
npm install
```

### Seed Database

```sh
node seed.js
```

### Run Server

```sh
npm start
```

## Deployment

Deployed on Render.com with the following settings:
- **Build Command**: `npm install`
- **Start Command**: `npm start`
- **Environment Variables**: Set in Render dashboard

## Project Structure

```
├── server.js          # Main Express server
├── seed.js            # Database seeding script
├── package.json       # Dependencies
├── images/            # Lesson images (SVG)
├── scripts/           # Utility scripts
│   ├── build-submission.sh
│   ├── export-data.py
│   └── seed-db.sh
└── exports/           # MongoDB/Postman exports
```
