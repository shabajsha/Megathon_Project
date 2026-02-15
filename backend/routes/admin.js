const express = require('express');
const router = express.Router();
const { authenticate, isAdmin } = require('../middleware/auth');
const Admin = require('../models/Admin');
const Organizer = require('../models/Organizer');
const { sendOrganizerCredentials } = require('../utils/email');

// Initialize admin (run once)
router.post('/init', async (req, res) => {
  try {
    const existingAdmin = await Admin.findOne();
    if (existingAdmin) {
      return res.status(400).json({ message: 'Admin already exists' });
    }

    const admin = new Admin({
      email: process.env.ADMIN_EMAIL || 'admin@eventmanagement.com',
      password: process.env.ADMIN_PASSWORD || 'Admin@12345'
    });

    await admin.save();

    res.status(201).json({ message: 'Admin initialized successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Create new organizer
router.post('/organizers', authenticate, isAdmin, async (req, res) => {
  try {
    const { organizerName, category, description, contactEmail, contactNumber } = req.body;

    // Auto-generate login credentials
    const loginEmail = `${organizerName.toLowerCase().replace(/\s+/g, '.')}@org.events.com`;
    const tempPassword = Math.random().toString(36).slice(-8) + 'Org@1';

    // Check if organizer already exists
    const existingOrganizer = await Organizer.findOne({ email: loginEmail });
    if (existingOrganizer) {
      return res.status(400).json({ message: 'Organizer with similar name already exists' });
    }

    // Create new organizer
    const organizer = new Organizer({
      organizerName,
      email: loginEmail,
      password: tempPassword,
      category,
      description,
      contactEmail,
      contactNumber,
      createdBy: req.userId
    });

    await organizer.save();

    // Send credentials to contact email
    await sendOrganizerCredentials(contactEmail, {
      email: loginEmail,
      password: tempPassword
    });

    res.status(201).json({
      message: 'Organizer created successfully',
      credentials: {
        loginEmail,
        tempPassword
      },
      organizer: {
        id: organizer._id,
        organizerName: organizer.organizerName,
        email: loginEmail
      }
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Get all organizers
router.get('/organizers', authenticate, isAdmin, async (req, res) => {
  try {
    const organizers = await Organizer.find()
      .select('-password')
      .populate('eventsCreated', 'eventName eventType status');

    res.json(organizers);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Remove/Disable organizer
router.delete('/organizers/:organizerId', authenticate, isAdmin, async (req, res) => {
  try {
    const { organizerId } = req.params;
    const { permanent } = req.query;

    if (permanent === 'true') {
      await Organizer.findByIdAndDelete(organizerId);
      res.json({ message: 'Organizer permanently deleted' });
    } else {
      await Organizer.findByIdAndUpdate(organizerId, { isActive: false });
      res.json({ message: 'Organizer disabled' });
    }
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Reactivate organizer
router.put('/organizers/:organizerId/activate', authenticate, isAdmin, async (req, res) => {
  try {
    const { organizerId } = req.params;
    await Organizer.findByIdAndUpdate(organizerId, { isActive: true });
    res.json({ message: 'Organizer activated' });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

module.exports = router;
