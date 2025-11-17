const mongoose = require('mongoose')

const orderItemSchema = new mongoose.Schema(
  {
    lessonId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Lesson',
      required: true
    },
    spaces: {
      type: Number,
      required: true,
      min: 1
    }
  },
  { _id: false }
)

const orderSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true
    },
    phone: {
      type: String,
      required: true,
      trim: true
    },
    email: {
      type: String,
      trim: true
    },
    items: {
      type: [orderItemSchema],
      required: true,
      validate: v => Array.isArray(v) && v.length > 0
    }
  },
  {
    timestamps: true
  }
)

module.exports = mongoose.model('Order', orderSchema)
