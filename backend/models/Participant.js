const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const participantSchema = new mongoose.Schema({
  firstName: {
    type: String,
    required: true,
    trim: true
  },
  lastName: {
    type: String,
    required: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true
  },
  participantType: {
    type: String,
    enum: ['IIIT', 'Non-IIIT'],
    required: true
  },
  collegeName: {
    type: String,
    required: true,
    trim: true
  },
  contactNumber: {
    type: String,
    required: true,
    trim: true
  },
  role: {
    type: String,
    default: 'participant'
  },
  // User preferences
  areasOfInterest: [{
    type: String,
    trim: true
  }],
  followedClubs: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Organizer'
  }],
  // Additional fields
  registeredEvents: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Event'
  }],
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

// Hash password before saving
participantSchema.pre('save', async function(next) {
  if (!this.isModified('password')) {
    return next();
  }
  const salt = await bcrypt.genSalt(10);
  this.password = await bcrypt.hash(this.password, salt);
  next();
});

// Method to compare password
participantSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('Participant', participantSchema);
