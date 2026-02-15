const express = require('express');
const router = express.Router();
const Participant = require('../models/Participant');
const Organizer = require('../models/Organizer');
const Admin = require('../models/Admin');
const { generateToken } = require('../utils/jwt');

// Participant Registration
router.post('/register/participant', async (req, res) => {
  try {
    const { firstName, lastName, email, password, contactNumber, collegeName, participantType } = req.body;

    // Validate IIIT email if participant type is IIIT
    if (participantType === 'IIIT') {
      const iiitEmailRegex = /@iiit\.ac\.in$/i;
      if (!iiitEmailRegex.test(email)) {
        return res.status(400).json({ message: 'IIIT participants must use IIIT-issued email (@iiit.ac.in)' });
      }
    }

    // Check if participant already exists
    const existingParticipant = await Participant.findOne({ email });
    if (existingParticipant) {
      return res.status(400).json({ message: 'Email already registered' });
    }

    // Create new participant
    const participant = new Participant({
      firstName,
      lastName,
      email,
      password,
      contactNumber,
      collegeName,
      participantType
    });

    await participant.save();

    // Generate token
    const token = generateToken(participant._id, 'participant');

    res.status(201).json({
      message: 'Participant registered successfully',
      token,
      user: {
        id: participant._id,
        firstName: participant.firstName,
        lastName: participant.lastName,
        email: participant.email,
        role: 'participant',
        participantType: participant.participantType
      }
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Participant Login
router.post('/login/participant', async (req, res) => {
  try {
    const { email, password } = req.body;

    // Find participant
    const participant = await Participant.findOne({ email });
    if (!participant || !participant.isActive) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Check password
    const isMatch = await participant.comparePassword(password);
    if (!isMatch) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Generate token
    const token = generateToken(participant._id, 'participant');

    res.json({
      message: 'Login successful',
      token,
      user: {
        id: participant._id,
        firstName: participant.firstName,
        lastName: participant.lastName,
        email: participant.email,
        role: 'participant',
        participantType: participant.participantType
      }
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Organizer Login
router.post('/login/organizer', async (req, res) => {
  try {
    const { email, password } = req.body;

    // Find organizer
    const organizer = await Organizer.findOne({ email });
    if (!organizer || !organizer.isActive) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Check password
    const isMatch = await organizer.comparePassword(password);
    if (!isMatch) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Generate token
    const token = generateToken(organizer._id, 'organizer');

    res.json({
      message: 'Login successful',
      token,
      user: {
        id: organizer._id,
        organizerName: organizer.organizerName,
        email: organizer.email,
        role: 'organizer',
        category: organizer.category
      }
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Admin Login
router.post('/login/admin', async (req, res) => {
  try {
    const { email, password } = req.body;

    // Find admin
    const admin = await Admin.findOne({ email });
    if (!admin || !admin.isActive) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Check password
    const isMatch = await admin.comparePassword(password);
    if (!isMatch) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Generate token
    const token = generateToken(admin._id, 'admin');

    res.json({
      message: 'Login successful',
      token,
      user: {
        id: admin._id,
        email: admin.email,
        role: 'admin'
      }
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

module.exports = router;
