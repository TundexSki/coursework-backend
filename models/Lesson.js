const mongoose = require('mongoose')

const lessonSchema = new mongoose.Schema(
  {
    subject: {
      type: String,
      required: true,
      trim: true
    },
    location: {
      type: String,
      required: true,
      trim: true
    },
    price: {
      type: Number,
      required: true,
      min: 0
    },
    spaces: {
      type: Number,
      required: true,
      min: 0
    },
    description: {
      type: String,
      trim: true
    },
    image: {
      type: String,
      trim: true
    }
  },
  {
    timestamps: true
  }
)

module.exports = mongoose.model('Lesson', lessonSchema)
