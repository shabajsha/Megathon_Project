const express = require('express');
const router = express.Router();
const { authenticate, isOrganizer } = require('../middleware/auth');
const Organizer = require('../models/Organizer');

// Get organizer profile
router.get('/profile', authenticate, isOrganizer, async (req, res) => {
  try {
    const organizer = await Organizer.findById(req.userId)
      .select('-password')
      .populate('eventsCreated');
    
    res.json(organizer);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Update organizer profile
router.put('/profile', authenticate, isOrganizer, async (req, res) => {
  try {
    const { organizerName, category, description, contactEmail, contactNumber, discordWebhook } = req.body;

    const organizer = await Organizer.findById(req.userId);
    
    if (organizerName) organizer.organizerName = organizerName;
    if (category) organizer.category = category;
    if (description) organizer.description = description;
    if (contactEmail) organizer.contactEmail = contactEmail;
    if (contactNumber) organizer.contactNumber = contactNumber;
    if (discordWebhook !== undefined) organizer.discordWebhook = discordWebhook;

    await organizer.save();

    res.json({
      message: 'Profile updated successfully',
      organizer: await Organizer.findById(req.userId).select('-password')
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Get all organizers (public)
router.get('/list', async (req, res) => {
  try {
    const organizers = await Organizer.find({ isActive: true })
      .select('organizerName category description contactEmail followers')
      .populate('eventsCreated', 'eventName eventType status eventStartDate');

    res.json(organizers);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Get organizer by ID (public)
router.get('/:organizerId', async (req, res) => {
  try {
    const organizer = await Organizer.findById(req.params.organizerId)
      .select('-password')
      .populate('eventsCreated', 'eventName eventType status eventStartDate eventEndDate');

    if (!organizer) {
      return res.status(404).json({ message: 'Organizer not found' });
    }

    res.json(organizer);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

module.exports = router;
