require('dotenv').config()

const { MongoClient } = require('mongodb')

// Connection settings for the coursework MongoDB database
const MONGODB_URI = process.env.MONGODB_URI
const DB_NAME = process.env.DB_NAME || 'courseworkDB'

if (!MONGODB_URI) {
  console.error('MONGODB_URI is not set in .env')
  process.exit(1)
}

// Seed data for the lessons collection using numeric IDs
const seedLessons = [
  {
    _id: 1,
    subject: 'Algebra II',
    location: 'Room 204',
    price: 38,
    spaces: 5,
    description: 'Quadratic, exponential, and polynomial problem solving with guided practice.',
    image: 'algebra.svg'
  },
  {
    _id: 2,
    subject: 'Biology Lab',
    location: 'Science Lab B',
    price: 42,
    spaces: 5,
    description: 'Microscope work and dissections that bring cellular biology to life.',
    image: 'biology-lab.svg'
  },
  {
    _id: 3,
    subject: 'Chemistry Honors',
    location: 'Chemistry Lab',
    price: 44,
    spaces: 5,
    description: 'Reactions, stoichiometry, and weekly safety-focused experiments.',
    image: 'chemistry-honors.svg'
  },
  {
    _id: 4,
    subject: 'Physics Workshop',
    location: 'Innovation Studio',
    price: 46,
    spaces: 5,
    description: 'Motion labs, energy challenges, and simple robotics tie-ins.',
    image: 'physics-workshop.svg'
  },
  {
    _id: 5,
    subject: 'English Literature',
    location: 'Library Commons',
    price: 36,
    spaces: 5,
    description: 'Close reading, essay writing, and seminar-style discussions.',
    image: 'english-literature.svg'
  },
  {
    _id: 6,
    subject: 'World History',
    location: 'Room 112',
    price: 34,
    spaces: 5,
    description: 'Global movements and key decisions from ancient to modern eras.',
    image: 'world-history.svg'
  },
  {
    _id: 7,
    subject: 'Computer Science Principles',
    location: 'Tech Lab',
    price: 48,
    spaces: 5,
    description: 'Algorithms, interactive apps, and ethical computing foundations.',
    image: 'computer-science-principles.svg'
  },
  {
    _id: 8,
    subject: 'French Conversation',
    location: 'Language Studio',
    price: 33,
    spaces: 5,
    description: 'Roleplay, listening drills, and everyday vocabulary.',
    image: 'french-conversation.svg'
  },
  {
    _id: 9,
    subject: 'Studio Art',
    location: 'Art Atelier',
    price: 40,
    spaces: 5,
    description: 'Charcoal, acrylics, and mixed media portfolio pieces.',
    image: 'studio-art.svg'
  },
  {
    _id: 10,
    subject: 'Music Ensemble',
    location: 'Music Room',
    price: 37,
    spaces: 5,
    description: 'Contemporary charts and small-group performance skills.',
    image: 'music-ensemble.svg'
  },
  {
    _id: 11,
    subject: 'AP Economics',
    location: 'Room 305',
    price: 45,
    spaces: 5,
    description: 'Market simulations and data-driven policy case studies.',
    image: 'ap-economics.svg'
  },
  {
    _id: 12,
    subject: 'Health & Wellness',
    location: 'Wellness Center',
    price: 32,
    spaces: 5,
    description: 'Nutrition, mindfulness, and fitness planning for balanced living.',
    image: 'health-wellness.svg'
  },
  {
    _id: 13,
    subject: 'Environmental Science',
    location: 'Greenhouse Lab',
    price: 41,
    spaces: 5,
    description: 'Ecosystems, sustainability challenges, and field data collection.',
    image: 'environmental-science.svg'
  }
]

// Connects to MongoDB, clears existing lessons, and inserts the seed data.
async function run() {
  const client = new MongoClient(MONGODB_URI)

  try {
    await client.connect()
    const db = client.db(DB_NAME)
    const lessons = db.collection('lessons')

    console.log(`[seed] Connected to ${DB_NAME}, seeding lessons...`)

    await lessons.deleteMany({})
    const result = await lessons.insertMany(seedLessons)

    console.log(`[seed] Inserted ${result.insertedCount} lessons.`)
  } catch (err) {
    console.error('[seed] Failed to seed lessons:', err)
    process.exitCode = 1
  } finally {
    await client.close()
  }
}

run()
