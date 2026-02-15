const express = require('express');
const router = express.Router();
const { authenticate, isParticipant } = require('../middleware/auth');
const Participant = require('../models/Participant');
const Organizer = require('../models/Organizer');

// Get participant profile
router.get('/profile', authenticate, isParticipant, async (req, res) => {
  try {
    const participant = await Participant.findById(req.userId)
      .select('-password')
      .populate('followedClubs', 'organizerName category description');
    
    res.json(participant);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Update participant profile
router.put('/profile', authenticate, isParticipant, async (req, res) => {
  try {
    const { firstName, lastName, contactNumber, collegeName, areasOfInterest } = req.body;

    const participant = await Participant.findById(req.userId);
    
    if (firstName) participant.firstName = firstName;
    if (lastName) participant.lastName = lastName;
    if (contactNumber) participant.contactNumber = contactNumber;
    if (collegeName) participant.collegeName = collegeName;
    if (areasOfInterest) participant.areasOfInterest = areasOfInterest;

    await participant.save();

    res.json({
      message: 'Profile updated successfully',
      participant: await Participant.findById(req.userId).select('-password')
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Set/Update preferences (onboarding)
router.post('/preferences', authenticate, isParticipant, async (req, res) => {
  try {
    const { areasOfInterest, followedClubs } = req.body;

    const participant = await Participant.findById(req.userId);
    
    if (areasOfInterest) participant.areasOfInterest = areasOfInterest;
    if (followedClubs) participant.followedClubs = followedClubs;

    await participant.save();

    res.json({
      message: 'Preferences updated successfully',
      participant: await Participant.findById(req.userId).select('-password')
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Follow/Unfollow a club
router.post('/follow/:organizerId', authenticate, isParticipant, async (req, res) => {
  try {
    const { organizerId } = req.params;
    const participant = await Participant.findById(req.userId);
    const organizer = await Organizer.findById(organizerId);

    if (!organizer) {
      return res.status(404).json({ message: 'Organizer not found' });
    }

    const isFollowing = participant.followedClubs.includes(organizerId);

    if (isFollowing) {
      // Unfollow
      participant.followedClubs = participant.followedClubs.filter(
        id => id.toString() !== organizerId
      );
      organizer.followers = organizer.followers.filter(
        id => id.toString() !== req.userId
      );
    } else {
      // Follow
      participant.followedClubs.push(organizerId);
      organizer.followers.push(req.userId);
    }

    await participant.save();
    await organizer.save();

    res.json({
      message: isFollowing ? 'Unfollowed successfully' : 'Followed successfully',
      isFollowing: !isFollowing
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

// Get my registered events
router.get('/my-events', authenticate, isParticipant, async (req, res) => {
  try {
    const participant = await Participant.findById(req.userId)
      .populate({
        path: 'registeredEvents',
        populate: {
          path: 'organizer',
          select: 'organizerName category'
        }
      });

    res.json(participant.registeredEvents);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

module.exports = router;
