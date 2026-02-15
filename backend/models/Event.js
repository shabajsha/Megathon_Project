const mongoose = require('mongoose');

const eventSchema = new mongoose.Schema({
  eventName: {
    type: String,
    required: true,
    trim: true
  },
  eventDescription: {
    type: String,
    required: true,
    trim: true
  },
  eventType: {
    type: String,
    enum: ['Normal', 'Merchandise'],
    required: true
  },
  eligibility: {
    type: String,
    enum: ['IIIT Only', 'Non-IIIT Only', 'All'],
    required: true,
    default: 'All'
  },
  registrationDeadline: {
    type: Date,
    required: true
  },
  eventStartDate: {
    type: Date,
    required: true
  },
  eventEndDate: {
    type: Date,
    required: true
  },
  registrationLimit: {
    type: Number,
    required: true
  },
  registrationFee: {
    type: Number,
    default: 0
  },
  organizer: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Organizer',
    required: true
  },
  eventTags: [{
    type: String,
    trim: true
  }],
  status: {
    type: String,
    enum: ['Draft', 'Published', 'Ongoing', 'Completed', 'Closed'],
    default: 'Draft'
  },
  // For Normal Events - Custom Registration Form
  customForm: [{
    fieldName: String,
    fieldType: {
      type: String,
      enum: ['text', 'email', 'number', 'dropdown', 'checkbox', 'file', 'textarea']
    },
    isRequired: Boolean,
    options: [String], // For dropdown
    order: Number
  }],
  // For Merchandise Events
  merchandiseDetails: {
    itemName: String,
    variants: [{
      size: String,
      color: String,
      stockQuantity: Number
    }],
    purchaseLimit: {
      type: Number,
      default: 1
    }
  },
  // Registrations and Analytics
  registrations: [{
    participant: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Participant'
    },
    registrationDate: {
      type: Date,
      default: Date.now
    },
    formData: mongoose.Schema.Types.Mixed,
    ticketId: String,
    paymentStatus: {
      type: String,
      enum: ['Pending', 'Approved', 'Rejected', 'Completed'],
      default: 'Completed'
    },
    attended: {
      type: Boolean,
      default: false
    },
    attendanceTime: Date
  }],
  // Analytics
  totalRegistrations: {
    type: Number,
    default: 0
  },
  totalRevenue: {
    type: Number,
    default: 0
  },
  isFormLocked: {
    type: Boolean,
    default: false
  }
}, {
  timestamps: true
});

// Index for search
eventSchema.index({ eventName: 'text', eventDescription: 'text', eventTags: 'text' });

module.exports = mongoose.model('Event', eventSchema);
