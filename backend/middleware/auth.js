const jwt = require('jsonwebtoken');
const Participant = require('../models/Participant');
const Organizer = require('../models/Organizer');
const Admin = require('../models/Admin');

// Verify JWT token
exports.authenticate = async (req, res, next) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({ message: 'No token, authorization denied' });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.userId = decoded.userId;
    req.userRole = decoded.role;
    
    next();
  } catch (error) {
    res.status(401).json({ message: 'Token is not valid' });
  }
};

// Check if user is a participant
exports.isParticipant = async (req, res, next) => {
  try {
    if (req.userRole !== 'participant') {
      return res.status(403).json({ message: 'Access denied. Participants only.' });
    }
    
    const participant = await Participant.findById(req.userId);
    if (!participant || !participant.isActive) {
      return res.status(404).json({ message: 'Participant not found or inactive' });
    }
    
    req.user = participant;
    next();
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// Check if user is an organizer
exports.isOrganizer = async (req, res, next) => {
  try {
    if (req.userRole !== 'organizer') {
      return res.status(403).json({ message: 'Access denied. Organizers only.' });
    }
    
    const organizer = await Organizer.findById(req.userId);
    if (!organizer || !organizer.isActive) {
      return res.status(404).json({ message: 'Organizer not found or inactive' });
    }
    
    req.user = organizer;
    next();
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// Check if user is an admin
exports.isAdmin = async (req, res, next) => {
  try {
    if (req.userRole !== 'admin') {
      return res.status(403).json({ message: 'Access denied. Admins only.' });
    }
    
    const admin = await Admin.findById(req.userId);
    if (!admin || !admin.isActive) {
      return res.status(404).json({ message: 'Admin not found or inactive' });
    }
    
    req.user = admin;
    next();
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};
